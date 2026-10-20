#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT v6 Morfolojik Özellik Katmanı
quran-morphology.txt içindeki ve şimdiye kadar kullanılmayan tüm özellikleri
(şahıs, cinsiyet, sayı, kip, çatı, i'rab, fiil babı, mod) ayrıştırır ve
nüzul sırası / Mekkî-Medenî bilgisiyle birleştirir.

Asıl külliyat veritabanına (mirat_corpus.db) DOKUNMAZ; isteğe bağlı olarak
ayrı bir veriler/mirat_features.db dosyasına yazar.
"""

import os
import re
import sqlite3
import sys
from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))

MORPH_PATH = os.path.join(PROJECT_ROOT, "veriler", "quran-morphology.txt")
FEATURES_DB_PATH = os.path.join(PROJECT_ROOT, "veriler", "mirat_features.db")

# Şahıs/cinsiyet/sayı etiketleri: 3MS, 2MP, 1P, 1S, MS, FP, M, F, MD, 2D ...
# Not: tek başına 'P' edat etiketidir, bu yüzden hariç tutulur.
PGN_RE = re.compile(r'^(?:([123])([MF])?([SDP])|([MF])([SDP])?)$')
ASPECTS = {'PERF', 'IMPF', 'IMPV'}
CASES = {'NOM', 'ACC', 'GEN'}


@dataclass
class Segment:
    surah: int
    ayah: int
    word: int
    seg: int
    form: str
    tag: str
    root: str = None
    lemma: str = None
    person: str = None   # '1', '2', '3'
    gender: str = None   # 'M', 'F'
    number: str = None   # 'S', 'D', 'P'
    aspect: str = None   # PERF / IMPF / IMPV
    voice: str = 'ACT'   # ACT / PASS
    case: str = None
    verb_form: str = None
    mood: str = None
    flags: frozenset = field(default_factory=frozenset)


def parse_features(feat_str):
    out = {'flags': set()}
    for tok in feat_str.split('|'):
        if tok.startswith('ROOT:'):
            out['root'] = tok[5:]
        elif tok.startswith('LEM:'):
            out['lemma'] = tok[4:]
        elif tok.startswith('VF:'):
            out['verb_form'] = tok[3:]
        elif tok.startswith('MOOD:'):
            out['mood'] = tok[5:]
        elif tok in ASPECTS:
            out['aspect'] = tok
        elif tok == 'PASS':
            out['voice'] = 'PASS'
        elif tok in CASES:
            out['case'] = tok
        else:
            m = PGN_RE.match(tok)
            if m and ('number' not in out and 'gender' not in out and 'person' not in out):
                if m.group(1):
                    out['person'], out['gender'], out['number'] = m.group(1), m.group(2), m.group(3)
                else:
                    out['gender'], out['number'] = m.group(4), m.group(5)
            else:
                out['flags'].add(tok)
    out['flags'] = frozenset(out['flags'])
    return out


class Corpus:
    """Bellek içi morfolojik külliyat. Tüm keşif motorlarının ortak veri kaynağı."""

    def __init__(self, morph_path=MORPH_PATH):
        from build_quran_markdown import SURAH_METADATA
        self.meta = SURAH_METADATA
        self.segments = []
        with open(morph_path, encoding='utf-8') as f:
            for line in f:
                parts = line.rstrip('\n').split('\t')
                if len(parts) < 4 or line.startswith('#'):
                    continue
                loc = parts[0].split(':')
                if len(loc) != 4:
                    continue
                s, a, w, g = map(int, loc)
                feats = parse_features(parts[3])
                self.segments.append(Segment(
                    surah=s, ayah=a, word=w, seg=g, form=parts[1], tag=parts[2],
                    root=feats.get('root'), lemma=feats.get('lemma'),
                    person=feats.get('person'), gender=feats.get('gender'), number=feats.get('number'),
                    aspect=feats.get('aspect'), voice=feats.get('voice', 'ACT'), case=feats.get('case'),
                    verb_form=feats.get('verb_form'), mood=feats.get('mood'), flags=feats['flags']
                ))
        self._by_ayah = defaultdict(list)
        for sg in self.segments:
            self._by_ayah[(sg.surah, sg.ayah)].append(sg)
        self.ayah_keys = sorted(self._by_ayah)

    # ---------------- Yardımcılar ----------------
    def ayah_segments(self, surah, ayah):
        return self._by_ayah.get((surah, ayah), [])

    def surah_ayahs(self, surah):
        return [k for k in self.ayah_keys if k[0] == surah]

    def ayah_word_count(self, surah, ayah):
        return len({sg.word for sg in self._by_ayah.get((surah, ayah), [])})

    def ayah_content_lemmas(self, surah, ayah):
        """Edatlar hariç (tag != 'P') lemma dizisi."""
        return [sg.lemma for sg in self._by_ayah.get((surah, ayah), []) if sg.lemma and sg.tag != 'P']

    def ayah_roots(self, surah, ayah):
        return [sg.root for sg in self._by_ayah.get((surah, ayah), []) if sg.root]

    def ayah_verbs(self, surah, ayah):
        return [sg for sg in self._by_ayah.get((surah, ayah), []) if sg.tag == 'V']

    def revelation_order(self, surah):
        return self.meta[surah]['order']

    def is_meccan(self, surah):
        return self.meta[surah]['place'] == 'Mekke'

    def surahs_by(self, order='mushaf'):
        nums = list(range(1, 115))
        if order == 'nuzul':
            nums.sort(key=self.revelation_order)
        return nums

    def root_frequencies(self):
        freq = defaultdict(int)
        for sg in self.segments:
            if sg.root:
                freq[sg.root] += 1
        return dict(freq)


@lru_cache(maxsize=1)
def get_corpus():
    return Corpus()


def build_features_db(db_path=FEATURES_DB_PATH):
    """Özellik tablosunu ayrı bir SQLite dosyasına yazar (inceleme ve web için)."""
    corpus = get_corpus()
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.executescript("""
    CREATE TABLE segment_features (
        surah INTEGER, ayah INTEGER, word INTEGER, seg INTEGER, form TEXT, tag TEXT,
        root TEXT, lemma TEXT, person TEXT, gender TEXT, number TEXT, aspect TEXT,
        voice TEXT, gcase TEXT, verb_form TEXT, mood TEXT, flags TEXT
    );
    CREATE TABLE surah_meta (surah INTEGER PRIMARY KEY, revelation_order INTEGER, place TEXT, verses INTEGER);
    """)
    c.executemany("INSERT INTO segment_features VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", [
        (s.surah, s.ayah, s.word, s.seg, s.form, s.tag, s.root, s.lemma, s.person, s.gender, s.number,
         s.aspect, s.voice, s.case, s.verb_form, s.mood, '|'.join(sorted(s.flags))) for s in corpus.segments
    ])
    c.executemany("INSERT INTO surah_meta VALUES (?,?,?,?)", [
        (n, corpus.meta[n]['order'], corpus.meta[n]['place'], corpus.meta[n]['verses']) for n in range(1, 115)
    ])
    c.executescript("""
    CREATE INDEX idx_sf_loc ON segment_features(surah, ayah);
    CREATE INDEX idx_sf_root ON segment_features(root);
    CREATE INDEX idx_sf_lemma ON segment_features(lemma);
    """)
    conn.commit()
    conn.close()
    return db_path


if __name__ == "__main__":
    corp = get_corpus()
    print("Segment:", len(corp.segments), "| Ayet:", len(corp.ayah_keys))
    print("1:5 fiiller:", [(v.form, v.person, v.number, v.aspect) for v in corp.ayah_verbs(1, 5)])
    print("Yazıldı:", build_features_db())
