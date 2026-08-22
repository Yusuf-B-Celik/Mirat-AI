#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Külliyat ve Morfolojik Veritabanı Modülü
Quranic Arabic Corpus morfolojik verilerini SQLite veritabanında yapılandırır ve sorgular.
"""

import sqlite3
import urllib.request
import os
import re
import json
import time
from contextlib import contextmanager

DB_PATH = "mirat_corpus.db"
MORPHOLOGY_URL = "https://raw.githubusercontent.com/mustafa0x/quran-morphology/master/quran-morphology.txt"
LOCAL_MORPH_FILE = "quran-morphology.txt"

def download_morphology_file():
    if not os.path.exists(LOCAL_MORPH_FILE) or os.path.getsize(LOCAL_MORPH_FILE) < 1000000:
        print("Quranic morphology veri seti indiriliyor...")
        req = urllib.request.Request(MORPHOLOGY_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read()
        with open(LOCAL_MORPH_FILE, "wb") as f:
            f.write(content)
        print(f"Veri seti kaydedildi: {LOCAL_MORPH_FILE} ({os.path.getsize(LOCAL_MORPH_FILE):,} byte)")
    else:
        pass

def clean_arabic_diacritics(text):
    if not text:
        return ""
    text = re.sub(r'[\u0617-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED]', '', text)
    text = re.sub(r'[إأآٱ]', 'ا', text)
    text = re.sub(r'[ى]', 'ي', text)
    text = re.sub(r'[ة]', 'ه', text)
    return text.strip()

def init_db(force_recreate=False):
    if os.path.exists(DB_PATH) and not force_recreate:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT count(*) FROM segments")
        cnt = c.fetchone()[0]
        conn.close()
        if cnt >= 120000:
            return

    download_morphology_file()
    
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.executescript("""
    DROP TABLE IF EXISTS segments;
    DROP TABLE IF EXISTS words;
    DROP TABLE IF EXISTS roots;
    DROP TABLE IF EXISTS lemmas;

    CREATE TABLE segments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT NOT NULL,
        surah INTEGER NOT NULL,
        ayah INTEGER NOT NULL,
        word INTEGER NOT NULL,
        segment INTEGER NOT NULL,
        form TEXT NOT NULL,
        clean_form TEXT,
        pos TEXT NOT NULL,
        root TEXT,
        lemma TEXT,
        features TEXT
    );

    CREATE TABLE words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT UNIQUE NOT NULL,
        surah INTEGER NOT NULL,
        ayah INTEGER NOT NULL,
        word INTEGER NOT NULL,
        arabic_text TEXT NOT NULL,
        clean_text TEXT NOT NULL,
        primary_root TEXT,
        primary_lemma TEXT,
        primary_pos TEXT,
        segment_count INTEGER
    );

    CREATE TABLE roots (
        root TEXT PRIMARY KEY,
        frequency INTEGER,
        surah_count INTEGER,
        first_occurrence TEXT
    );

    CREATE TABLE lemmas (
        lemma TEXT PRIMARY KEY,
        root TEXT,
        pos TEXT,
        frequency INTEGER
    );
    """)

    with open(LOCAL_MORPH_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    segments_data = []
    words_map = {}
    root_counts = {}
    root_surahs = {}
    root_first = {}
    lemma_counts = {}
    lemma_meta = {}

    for line in lines:
        if line.startswith("#") or not line.strip():
            continue
        parts = line.strip().split("\t")
        if len(parts) < 4:
            continue
        
        loc, form, pos, feats = parts[0], parts[1], parts[2], parts[3]
        loc_parts = [int(x) for x in loc.split(":")]
        s_num, a_num, w_num, seg_num = loc_parts[0], loc_parts[1], loc_parts[2], loc_parts[3]
        
        clean_form = clean_arabic_diacritics(form)
        
        feat_dict = {}
        root = None
        lemma = None
        for f_item in feats.split("|"):
            if ":" in f_item:
                k, v = f_item.split(":", 1)
                feat_dict[k] = v
                if k == "ROOT":
                    root = v
                elif k == "LEM":
                    lemma = v
            else:
                feat_dict[f_item] = True

        segments_data.append((
            loc, s_num, a_num, w_num, seg_num, form, clean_form, pos, root, lemma, json.dumps(feat_dict, ensure_ascii=False)
        ))

        w_loc = f"{s_num}:{a_num}:{w_num}"
        if w_loc not in words_map:
            words_map[w_loc] = {
                'surah': s_num,
                'ayah': a_num,
                'word': w_num,
                'forms': [],
                'roots': [],
                'lemmas': [],
                'poses': []
            }
        words_map[w_loc]['forms'].append(form)
        if root: words_map[w_loc]['roots'].append(root)
        if lemma: words_map[w_loc]['lemmas'].append(lemma)
        words_map[w_loc]['poses'].append(pos)

        if root:
            root_counts[root] = root_counts.get(root, 0) + 1
            if root not in root_surahs:
                root_surahs[root] = set()
                root_first[root] = f"{s_num}:{a_num}"
            root_surahs[root].add(s_num)

        if lemma:
            lemma_counts[lemma] = lemma_counts.get(lemma, 0) + 1
            if lemma not in lemma_meta:
                lemma_meta[lemma] = (root, pos)

    c.executemany("""
    INSERT INTO segments (location, surah, ayah, word, segment, form, clean_form, pos, root, lemma, features)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, segments_data)

    words_data = []
    for w_loc, w_info in words_map.items():
        ar_text = "".join(w_info['forms'])
        cl_text = clean_arabic_diacritics(ar_text)
        p_root = w_info['roots'][0] if w_info['roots'] else None
        p_lem = w_info['lemmas'][0] if w_info['lemmas'] else None
        p_pos = w_info['poses'][0] if w_info['poses'] else None
        seg_count = len(w_info['forms'])
        words_data.append((
            w_loc, w_info['surah'], w_info['ayah'], w_info['word'], ar_text, cl_text, p_root, p_lem, p_pos, seg_count
        ))

    c.executemany("""
    INSERT INTO words (location, surah, ayah, word, arabic_text, clean_text, primary_root, primary_lemma, primary_pos, segment_count)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, words_data)

    roots_data = []
    for r, freq in root_counts.items():
        roots_data.append((r, freq, len(root_surahs[r]), root_first[r]))
    c.executemany("INSERT INTO roots VALUES (?, ?, ?, ?)", roots_data)

    lemmas_data = []
    for lem, freq in lemma_counts.items():
        r, p = lemma_meta.get(lem, (None, None))
        lemmas_data.append((lem, r, p, freq))
    c.executemany("INSERT INTO lemmas VALUES (?, ?, ?, ?)", lemmas_data)

    c.executescript("""
    CREATE INDEX idx_seg_loc ON segments(location);
    CREATE INDEX idx_seg_surah_ayah ON segments(surah, ayah);
    CREATE INDEX idx_seg_root ON segments(root);
    CREATE INDEX idx_seg_lemma ON segments(lemma);
    CREATE INDEX idx_seg_pos ON segments(pos);
    CREATE INDEX idx_words_loc ON words(location);
    CREATE INDEX idx_words_surah_ayah ON words(surah, ayah);
    CREATE INDEX idx_words_root ON words(primary_root);
    CREATE INDEX idx_words_lemma ON words(primary_lemma);
    """)

    conn.commit()
    conn.close()

class MiratDB:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        if not os.path.exists(db_path):
            init_db()

    @contextmanager
    def get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
        finally:
            conn.close()

    def search_root(self, root):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("""
            SELECT s.location, s.surah, s.ayah, s.word, s.form, s.clean_form, s.pos, s.root, s.lemma, s.features
            FROM segments s
            WHERE s.root = ?
            ORDER BY s.surah, s.ayah, s.word, s.segment
            """, (root,))
            return [dict(r) for r in c.fetchall()]

    def search_lemma(self, lemma):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("""
            SELECT s.location, s.surah, s.ayah, s.word, s.form, s.clean_form, s.pos, s.root, s.lemma, s.features
            FROM segments s
            WHERE s.lemma = ?
            ORDER BY s.surah, s.ayah, s.word, s.segment
            """, (lemma,))
            return [dict(r) for r in c.fetchall()]

    def search_clean_text(self, text_pattern):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("""
            SELECT * FROM words WHERE clean_text LIKE ?
            ORDER BY surah, ayah, word
            """, (f"%{text_pattern}%",))
            return [dict(r) for r in c.fetchall()]

    def count_by_root_and_pos(self, root, pos=None):
        with self.get_connection() as conn:
            c = conn.cursor()
            if pos:
                c.execute("SELECT count(*) FROM segments WHERE root = ? AND pos = ?", (root, pos))
            else:
                c.execute("SELECT count(*) FROM segments WHERE root = ?", (root,))
            return c.fetchone()[0]

    def get_surah_ayah_words(self, surah, ayah):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("""
            SELECT * FROM words WHERE surah = ? AND ayah = ? ORDER BY word
            """, (surah, ayah))
            return [dict(r) for r in c.fetchall()]

if __name__ == "__main__":
    init_db(force_recreate=True)
