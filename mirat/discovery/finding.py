#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT v6 Keşif Katmanı: Ortak bulgu şeması ve istatistik yardımcıları.
Tüm sayılar deterministik koddan gelir; LLM yalnızca etiket/isim/gloss üretir.
"""

import math
import random
from dataclasses import dataclass, field, asdict
from typing import List, Optional


@dataclass
class Finding:
    id: str
    category: str
    title: str
    method: str
    metric: str
    value: float
    null_p: Optional[float] = None
    q_value: Optional[float] = None
    effect_size: Optional[float] = None
    evidence: List[str] = field(default_factory=list)
    detail: str = ""
    llm_assisted: bool = False
    kind: str = "test"          # "test" (p-değeri var) | "descriptive" (envanter/liste)

    def to_dict(self):
        d = asdict(self)
        for k in ('value', 'null_p', 'q_value', 'effect_size'):
            if isinstance(d[k], float):
                d[k] = round(d[k], 6)
        return d


# ---------------------------------------------------------------- istatistik
def rankdata(x):
    """Bağları ortalama sıra ile çözen sıralama."""
    order = sorted(range(len(x)), key=lambda i: x[i])
    ranks = [0.0] * len(x)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and x[order[j + 1]] == x[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks


def pearson(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    sxx = sum((a - mx) ** 2 for a in x)
    syy = sum((b - my) ** 2 for b in y)
    return sxy / math.sqrt(sxx * syy) if sxx > 0 and syy > 0 else 0.0


def spearman(x, y):
    return pearson(rankdata(x), rankdata(y))


def permutation_p(stat_fn, x, y, n_perm=5000, seed=42, two_sided=True):
    """y'yi karıştırarak stat_fn(x, y) için empirik p-değeri."""
    rng = random.Random(seed)
    obs = stat_fn(x, y)
    yy = list(y)
    hits = 0
    for _ in range(n_perm):
        rng.shuffle(yy)
        s = stat_fn(x, yy)
        if (abs(s) >= abs(obs)) if two_sided else (s >= obs):
            hits += 1
    return obs, (hits + 1) / (n_perm + 1)


def norm_sf(z):
    return 0.5 * math.erfc(z / math.sqrt(2))


def two_sided_p_from_z(z):
    return 2 * norm_sf(abs(z))


def mann_whitney_z(sample=None, population_sorted_ranks=None, a=None, b=None):
    """İki örneklem a, b için Mann-Whitney U normal yaklaşımı z skoru (a > b ise pozitif)."""
    n1, n2 = len(a), len(b)
    combined = a + b
    r = rankdata(combined)
    r1 = sum(r[:n1])
    u1 = r1 - n1 * (n1 + 1) / 2
    mu = n1 * n2 / 2
    sigma = math.sqrt(n1 * n2 * (n1 + n2 + 1) / 12)
    return (u1 - mu) / sigma if sigma > 0 else 0.0


def binom_z(k, n, p0):
    if n == 0 or p0 <= 0 or p0 >= 1:
        return 0.0
    return (k - n * p0) / math.sqrt(n * p0 * (1 - p0))


def bh_adjust(findings):
    """Kategori içi Benjamini-Hochberg: null_p'si olan bulgulara q_value yazar."""
    tested = [f for f in findings if f.null_p is not None]
    m = len(tested)
    if m == 0:
        return findings
    tested.sort(key=lambda f: f.null_p)
    running = 1.0
    for rank in range(m, 0, -1):
        f = tested[rank - 1]
        running = min(running, f.null_p * m / rank)
        f.q_value = min(1.0, running)
    return findings


def jaccard(a, b):
    if not a and not b:
        return 0.0
    return len(a & b) / len(a | b)


def strip_diacritics(text):
    import re
    text = re.sub(r'[\u0610-\u061A\u064B-\u065F\u0670\u06D6-\u06ED\u0640]', '', text or '')
    text = re.sub(r'[إأآٱ]', 'ا', text)
    text = text.replace('ى', 'ي').replace('ة', 'ه')
    return text
