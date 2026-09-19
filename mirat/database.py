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

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
POSSIBLE_DB_PATHS = [
    os.path.join(PROJECT_ROOT, "veriler", "mirat_corpus.db"),
    os.path.join(PROJECT_ROOT, "mirat_corpus.db"),
    os.environ.get("MIRAT_DB_PATH", "")
]

def get_db_path():
    for p in POSSIBLE_DB_PATHS:
        if p and os.path.exists(p):
            return p
    # Default fallback
    target_dir = os.path.join(PROJECT_ROOT, "veriler")
    os.makedirs(target_dir, exist_ok=True)
    return os.path.join(target_dir, "mirat_corpus.db")

MORPHOLOGY_URL = "https://raw.githubusercontent.com/mustafa0x/quran-morphology/master/quran-morphology.txt"

def get_morph_file_path():
    p1 = os.path.join(PROJECT_ROOT, "veriler", "quran-morphology.txt")
    p2 = os.path.join(PROJECT_ROOT, "quran-morphology.txt")
    if os.path.exists(p1):
        return p1
    if os.path.exists(p2):
        return p2
    return p1

def download_morphology_file():
    target = get_morph_file_path()
    if not os.path.exists(target) or os.path.getsize(target) < 1000000:
        print("Quranic morphology veri seti indiriliyor...")
        req = urllib.request.Request(MORPHOLOGY_URL, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=30) as resp:
            content = resp.read()
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "wb") as f:
            f.write(content)
        print(f"Veri seti kaydedildi: {target} ({os.path.getsize(target):,} byte)")

def clean_arabic_diacritics(text):
    if not text:
        return ""
    text = re.sub(r'[\u0617-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u06DF-\u06E4\u06E7\u06E8\u06EA-\u06ED]', '', text)
    text = re.sub(r'[إأآٱ]', 'ا', text)
    text = re.sub(r'[ى]', 'ي', text)
    text = re.sub(r'[ة]', 'ه', text)
    return text.strip()

def init_db(force_recreate=False):
    db_path = get_db_path()
    if os.path.exists(db_path) and not force_recreate:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute("SELECT count(*) FROM segments")
        cnt = c.fetchone()[0]
        conn.close()
        if cnt >= 120000:
            return

    download_morphology_file()
    morph_path = get_morph_file_path()
    
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.executescript("""
    DROP TABLE IF EXISTS segments;
    DROP TABLE IF EXISTS words;
    DROP TABLE IF EXISTS roots;
    DROP TABLE IF EXISTS lemmas;

    CREATE TABLE segments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT,
        surah INTEGER,
        ayah INTEGER,
        word_num INTEGER,
        segment_num INTEGER,
        form TEXT,
        tag TEXT,
        pos TEXT,
        root TEXT,
        lemma TEXT,
        clean_form TEXT
    );

    CREATE TABLE words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        surah INTEGER,
        ayah INTEGER,
        word_num INTEGER,
        text TEXT,
        clean_text TEXT
    );

    CREATE TABLE roots (
        root TEXT PRIMARY KEY,
        frequency INTEGER,
        unique_words INTEGER
    );

    CREATE TABLE lemmas (
        lemma TEXT PRIMARY KEY,
        frequency INTEGER,
        root TEXT
    );
    """)
    
    print("Morfoloji satırları ayrıştırılıyor...")
    segments_to_insert = []
    words_dict = {}
    roots_counter = {}
    lemmas_counter = {}
    
    with open(morph_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split("\t")
            if len(parts) < 4:
                continue
            
            loc = parts[0]
            form = parts[1]
            tag = parts[2]
            features = parts[3]
            
            loc_parts = loc.split(":")
            if len(loc_parts) != 4:
                continue
            surah, ayah, word_num, seg_num = map(int, loc_parts)
            
            root_m = re.search(r'ROOT:([^|]+)', features)
            root = root_m.group(1) if root_m else None
            
            lemma_m = re.search(r'LEM:([^|]+)', features)
            lemma = lemma_m.group(1) if lemma_m else None
            
            pos = tag
            clean_f = clean_arabic_diacritics(form)
            
            segments_to_insert.append((
                loc, surah, ayah, word_num, seg_num,
                form, tag, pos, root, lemma, clean_f
            ))
            
            w_key = (surah, ayah, word_num)
            if w_key not in words_dict:
                words_dict[w_key] = []
            words_dict[w_key].append(form)
            
            if root:
                roots_counter[root] = roots_counter.get(root, 0) + 1
            if lemma:
                lemmas_counter[lemma] = (lemmas_counter.get(lemma, (0, root))[0] + 1, root)
    
    print(f"Toplam {len(segments_to_insert):,} segment veritabanına yazılıyor...")
    c.executemany("""
    INSERT INTO segments (location, surah, ayah, word_num, segment_num, form, tag, pos, root, lemma, clean_form)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, segments_to_insert)
    
    words_to_insert = []
    for (surah, ayah, word_num), seg_forms in words_dict.items():
        w_text = "".join(seg_forms)
        w_clean = clean_arabic_diacritics(w_text)
        words_to_insert.append((surah, ayah, word_num, w_text, w_clean))
        
    print(f"Toplam {len(words_to_insert):,} kelime yazılıyor...")
    c.executemany("""
    INSERT INTO words (surah, ayah, word_num, text, clean_text)
    VALUES (?, ?, ?, ?, ?)
    """, words_to_insert)
    
    roots_to_insert = [(r, freq, 0) for r, freq in roots_counter.items()]
    c.executemany("""
    INSERT INTO roots (root, frequency, unique_words)
    VALUES (?, ?, ?)
    """, roots_to_insert)
    
    lemmas_to_insert = [(lem, data[0], data[1]) for lem, data in lemmas_counter.items()]
    c.executemany("""
    INSERT INTO lemmas (lemma, frequency, root)
    VALUES (?, ?, ?)
    """, lemmas_to_insert)
    
    print("İndeksler oluşturuluyor...")
    c.executescript("""
    CREATE INDEX idx_seg_loc ON segments(location);
    CREATE INDEX idx_seg_surah_ayah ON segments(surah, ayah);
    CREATE INDEX idx_seg_root ON segments(root);
    CREATE INDEX idx_seg_lemma ON segments(lemma);
    CREATE INDEX idx_seg_pos ON segments(pos);
    CREATE INDEX idx_seg_clean ON segments(clean_form);
    CREATE INDEX idx_words_surah_ayah ON words(surah, ayah);
    CREATE INDEX idx_words_clean ON words(clean_text);
    """)
    
    conn.commit()
    conn.close()
    print("MİRAT Veritabanı Hazır!")

class MiratDB:
    def __init__(self, db_path=None):
        self.db_path = db_path if db_path is not None else get_db_path()
        if not os.path.exists(self.db_path):
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
            c.execute("SELECT * FROM segments WHERE root = ?", (root,))
            return [dict(r) for r in c.fetchall()]

    def search_lemma(self, lemma):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM segments WHERE lemma = ?", (lemma,))
            return [dict(r) for r in c.fetchall()]

    def search_clean_form(self, clean_form):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM segments WHERE clean_form = ?", (clean_form,))
            return [dict(r) for r in c.fetchall()]

    def search_words_pattern(self, pattern):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM words WHERE clean_text LIKE ?", (f"%{pattern}%",))
            return [dict(r) for r in c.fetchall()]

    def get_surah_words(self, surah_num):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM words WHERE surah = ? ORDER BY id", (surah_num,))
            return [dict(r) for r in c.fetchall()]

    def get_surah_ayah_words(self, surah_num, ayah_num):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM words WHERE surah = ? AND ayah = ? ORDER BY id", (surah_num, ayah_num))
            return [dict(r) for r in c.fetchall()]

    def get_root_frequencies(self):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT root, frequency FROM roots WHERE root IS NOT NULL ORDER BY frequency DESC")
            return [dict(r) for r in c.fetchall()]

    def get_pos_distribution_for_root(self, root):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("""
            SELECT pos, count(*) as count 
            FROM segments 
            WHERE root = ? 
            GROUP BY pos 
            ORDER BY count DESC
            """, (root,))
            return {r['pos']: r['count'] for r in c.fetchall()}

    def get_cooccurrence_in_ayahs(self, root1, root2):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("""
            SELECT DISTINCT s1.surah, s1.ayah 
            FROM segments s1
            JOIN segments s2 ON s1.surah = s2.surah AND s1.ayah = s2.ayah
            WHERE s1.root = ? AND s2.root = ?
            """, (root1, root2))
            return [dict(r) for r in c.fetchall()]

    def get_total_counts(self):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT count(*) FROM segments")
            total_segments = c.fetchone()[0]
            c.execute("SELECT count(*) FROM words")
            total_words = c.fetchone()[0]
            c.execute("SELECT count(*) FROM roots")
            total_roots = c.fetchone()[0]
            c.execute("SELECT count(*) FROM lemmas")
            total_lemmas = c.fetchone()[0]
            return {
                'segments': total_segments,
                'words': total_words,
                'roots': total_roots,
                'lemmas': total_lemmas
            }

if __name__ == "__main__":
    init_db()
    db = MiratDB()
    counts = db.get_total_counts()
    print(f"MİRAT Veritabanı İstatistikleri: {counts}")
