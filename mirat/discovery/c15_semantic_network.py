#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kategori 15: Kavram Ağı ve Anlam Alanları

Girdi: kök eşbulunma grafiği (deterministik) + iki modelin UZLAŞTIĞI anlam alanı etiketleri (LLM).
Yöntemler:
  A. PPMI kök ağı + etiket yayılımı (label propagation) ile kavram kümeleri (tamamen deterministik).
  B. Yakınsak geçerlilik: deterministik kümeler ile LLM anlam alanları arasındaki normalleştirilmiş
     karşılıklı bilgi (NMI), alan etiketlerinin karıştırılmasına karşı (1000 permütasyon).
     → Metnin kendi eşbulunma yapısı, insan/LLM anlam kategorilerini ne ölçüde geri üretiyor?
  C. Anlam alanlarının kronolojik evrimi: her alanın sure içi token payı ~ nüzul sırası (Spearman, BH).
  D. Kümeler arası köprü kökler: en çok farklı kümeye bağlanan kökler (betimsel).
"""

import math
import random
from collections import Counter, defaultdict

from mirat.features import get_corpus
from mirat.discovery.finding import Finding, spearman, permutation_p, bh_adjust
from mirat.discovery import glossary
from mirat.discovery.lexicon import load_merged

CATEGORY = "15. Kavram Ağı ve Anlam Alanları"
MIN_ROOT_FREQ = 10
MIN_COOC = 3
TOP_K = 5


def nmi(x, y):
    n = len(x)
    cx, cy, cxy = Counter(x), Counter(y), Counter(zip(x, y))
    mi = sum(c / n * math.log((c * n) / (cx[a] * cy[b])) for (a, b), c in cxy.items())
    hx = -sum(c / n * math.log(c / n) for c in cx.values())
    hy = -sum(c / n * math.log(c / n) for c in cy.values())
    return 2 * mi / (hx + hy) if (hx + hy) > 0 else 0.0


def build_graph(corpus):
    freq = corpus.root_frequencies()
    roots = {r for r, f in freq.items() if f >= MIN_ROOT_FREQ}
    ay_roots = [set(r for r in corpus.ayah_roots(*k) if r in roots) for k in corpus.ayah_keys]
    df = Counter(r for s in ay_roots for r in s)
    co = Counter()
    for s in ay_roots:
        lst = sorted(s)
        for i in range(len(lst)):
            for j in range(i + 1, len(lst)):
                co[(lst[i], lst[j])] += 1
    n = len(ay_roots)
    full = defaultdict(dict)
    for (a, b), c in co.items():
        if c < MIN_COOC:
            continue
        pmi = math.log2(c * n / (df[a] * df[b]))
        if pmi > 0:
            w = pmi * math.log2(1 + c)      # nadir-kök şişmesini dengelemek için eşbulunma sayısıyla ağırlık
            full[a][b] = full[b][a] = w
    # kNN seyreltme: her kökün en güçlü TOP_K bağı (birleşim) — yoğun grafta dev küme oluşmasını önler
    g = defaultdict(dict)
    for a, nb in full.items():
        for b, w in sorted(nb.items(), key=lambda x: -x[1])[:TOP_K]:
            g[a][b] = g[b][a] = w
    return g, df


def label_propagation(g, seed=42, max_iter=50):
    rng = random.Random(seed)
    lab = {v: v for v in g}
    nodes = sorted(g)
    for _ in range(max_iter):
        rng.shuffle(nodes)
        changed = 0
        for v in nodes:
            score = defaultdict(float)
            for u, w in g[v].items():
                score[lab[u]] += w
            if not score:
                continue
            best = max(score.values())
            cands = sorted(l for l, s in score.items() if s == best)
            new = lab[v] if lab[v] in cands else cands[0]
            if new != lab[v]:
                lab[v] = new
                changed += 1
        if changed == 0:
            break
    return lab


def run(corpus=None, seed=42, merged=None):
    corpus = corpus or get_corpus()
    rng = random.Random(seed)
    merged = merged if merged is not None else load_merged()
    findings = []
    g, df = build_graph(corpus)
    lab = label_propagation(g, seed=seed)
    clusters = defaultdict(list)
    for v, l in lab.items():
        clusters[l].append(v)
    big = sorted([c for c in clusters.values() if len(c) >= 5], key=len, reverse=True)
    fields = {}
    if merged:
        fields = {r: v['field'] for r, v in merged['roots'].items() if v.get('field_agreed')}

    def describe(c):
        top = sorted(c, key=lambda r: -df[r])[:8]
        fc = Counter(fields[r] for r in c if r in fields)
        name = f"{fc.most_common(1)[0][0]} (%{100 * fc.most_common(1)[0][1] / max(1, sum(fc.values())):.0f})" if fc else "?"
        return name, top
    findings.append(Finding(
        id="c15_clusters", category=CATEGORY, llm_assisted=bool(fields), kind="descriptive",
        title=f"Kök eşbulunma ağı: {len(g)} kök, {sum(len(v) for v in g.values()) // 2} PPMI bağı; "
              f"etiket yayılımı {len(big)} kavram kümesi (>= 5 kök) buldu",
        method=f"Ayet düzeyi eşbulunma (>= {MIN_COOC}), PPMI ağırlıklı graf, deterministik etiket yayılımı",
        metric="küme sayısı", value=len(big),
        evidence=[f"[{describe(c)[0]}] " + ", ".join(glossary.label(r) for r in describe(c)[1][:5]) + f" … ({len(c)} kök)"
                  for c in big[:15]],
        detail="Küme adı: kümedeki köklerin iki modelce uzlaşılmış anlam alanlarının çoğunluğu (LLM yalnızca etiket verir)."))

    # ============ B. Yakınsak geçerlilik (NMI)
    if fields:
        nodes = [v for v in lab if v in fields and len(clusters[lab[v]]) >= 5]
        x = [lab[v] for v in nodes]
        y = [fields[v] for v in nodes]
        obs = nmi(x, y)
        yy = list(y)
        null = []
        for _ in range(1000):
            rng.shuffle(yy)
            null.append(nmi(x, yy))
        mu = sum(null) / len(null)
        findings.append(Finding(
            id="c15_convergent_validity", category=CATEGORY, llm_assisted=True,
            title=f"Metnin kendi eşbulunma yapısı anlam alanlarını geri üretiyor: NMI={obs:.3f} (rastgele {mu:.3f})",
            method="Deterministik kümeler vs uzlaşılmış LLM anlam alanları; NMI, alan etiketleri karıştırılır (1000 perm.)",
            metric="NMI", value=obs, null_p=(sum(1 for v in null if v >= obs) + 1) / 1001, effect_size=obs / mu if mu else None,
            detail=f"{len(nodes)} kök. Uzlaşılmış alan etiketi oranı: {len(fields)}/{len(merged['roots'])}."))

        # ============ C. Anlam alanlarının kronolojik evrimi
        order_vals = [corpus.revelation_order(s) for s in range(1, 115)]
        tok_by_s = defaultdict(Counter)
        for sg in corpus.segments:
            if sg.root in fields:
                tok_by_s[sg.surah][fields[sg.root]] += 1
        trend = []
        for i, fld in enumerate(sorted({*fields.values()})):
            share = [tok_by_s[s][fld] / max(1, sum(tok_by_s[s].values())) for s in range(1, 115)]
            if sum(tok_by_s[s][fld] for s in range(1, 115)) < 50:
                continue
            rho, p = permutation_p(spearman, order_vals, share, n_perm=2000, seed=seed + i)
            mk = [share[s - 1] for s in range(1, 115) if corpus.is_meccan(s)]
            md = [share[s - 1] for s in range(1, 115) if not corpus.is_meccan(s)]
            trend.append(Finding(
                id=f"c15_field_trend_{i:02d}", category=CATEGORY, llm_assisted=True,
                title=f"Anlam alanı '{fld}' nüzul sırasıyla {'artıyor' if rho > 0 else 'azalıyor'} (rho={rho:+.2f})",
                method="Sure içi alan token payı ~ nüzul sırası; Spearman, 2000 permütasyon, BH-FDR",
                metric="Spearman rho", value=rho, null_p=p, effect_size=rho,
                detail=f"Mekkî ort. %{100 * sum(mk) / len(mk):.1f} | Medenî ort. %{100 * sum(md) / len(md):.1f}"))
        bh_adjust(trend)
        findings.extend(sorted(trend, key=lambda f: f.null_p))

    # ============ D. Köprü kökler
    bridge = []
    for v in g:
        cl = {lab[u] for u in g[v] if len(clusters[lab[u]]) >= 5}
        bridge.append((len(cl), v))
    bridge.sort(reverse=True)
    findings.append(Finding(
        id="c15_bridges", category=CATEGORY, kind="descriptive",
        title="Kavram kümeleri arasında köprü kuran kökler: " + ", ".join(glossary.label(v) for _, v in bridge[:5]),
        method="Bir kökün PPMI komşularının ait olduğu farklı küme sayısı", metric="küme sayısı",
        value=bridge[0][0] if bridge else 0,
        evidence=[f"{glossary.label(v)}: {n} küme" for n, v in bridge[:15]]))
    bh_adjust([f for f in findings if f.null_p is not None and not f.id.startswith('c15_field_trend_')])
    return findings, {'clusters': {k: v for k, v in clusters.items() if len(v) >= 5}}


if __name__ == '__main__':
    fs, _ = run()
    for f in fs:
        q = f"{f.q_value:.4f}" if f.q_value is not None else "-"
        print(f"{f.id:26} {f.value:+.3f} q={q} | {f.title} | {f.detail[:160]} | {f.evidence[:5]}")
