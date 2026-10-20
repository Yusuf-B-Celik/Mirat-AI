#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kategori 17: Halka (Ring / Ayna) Kompozisyon Taraması

Hipotez: Bir surenin baş ve son kısımları birbirini "ayna" gibi yansıtır
(ayet i ↔ ayet n+1-i ya da blok j ↔ blok B+1-j).

Yöntem:
  - Ayet düzeyi: içerik-lemma vektörlerinin kosinüs benzerliği; ayna çiftlerinin ortalaması.
  - Blok düzeyi (>= 40 ayetli sureler): sure B=8 eşit ayet bloğuna bölünür; ayna blok çiftleri.
  - Null model: DÖNGÜSEL KAYDIRMA (rotasyon). Ayet sırası n farklı biçimde döndürülür; bu yerel
    bağdaşıklığı (komşu ayet benzerliği) korur, yalnızca "ayna merkezini" rastgele konuma taşır.
    Böylece "merkeze yakın ayna çiftleri zaten komşu" yanlılığı kontrol edilir.
  - Her sure için p = (gözlenene eşit/üstün rotasyon sayısı) / n; sureler arası BH-FDR.
  - Küresel test: p-değerlerinin uniform dağılımdan sapması (anlamlı sure sayısı vs beklenen %5).
"""

import math
from collections import Counter

from mirat.features import get_corpus
from mirat.discovery.finding import Finding, bh_adjust, binom_z, two_sided_p_from_z

CATEGORY = "17. Halka (Ayna) Kompozisyon Taraması"
N_BLOCKS = 8


def cosine(a, b):
    if not a or not b:
        return 0.0
    if len(a) > len(b):
        a, b = b, a
    dot = sum(v * b.get(k, 0) for k, v in a.items())
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def mirror_score_from_matrix(sim, order):
    n = len(order)
    pairs = [(order[i], order[n - 1 - i]) for i in range(n // 2)]
    return sum(sim[a][b] for a, b in pairs) / len(pairs) if pairs else 0.0


def ayah_level(vectors):
    """vectors: ayet sırasıyla Counter listesi. (gözlenen skor, rotasyon p, rotasyon skorları)"""
    n = len(vectors)
    sim = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            sim[i][j] = sim[j][i] = cosine(vectors[i], vectors[j])
    base = list(range(n))
    obs = mirror_score_from_matrix(sim, base)
    rot = [mirror_score_from_matrix(sim, base[r:] + base[:r]) for r in range(1, n)]
    p = (sum(1 for x in rot if x >= obs) + 1) / n
    return obs, p, rot


def block_level(vectors, B=N_BLOCKS):
    n = len(vectors)

    def score(order):
        blocks = []
        for j in range(B):
            lo, hi = round(j * n / B), round((j + 1) * n / B)
            c = Counter()
            for idx in order[lo:hi]:
                c.update(vectors[idx])
            blocks.append(c)
        return sum(cosine(blocks[j], blocks[B - 1 - j]) for j in range(B // 2)) / (B // 2), blocks
    base = list(range(n))
    obs, blocks = score(base)
    rot = [score(base[r:] + base[:r])[0] for r in range(1, n)]
    p = (sum(1 for x in rot if x >= obs) + 1) / n
    return obs, p, rot, blocks


def run(corpus=None, seed=42, min_ayahs=12):
    corpus = corpus or get_corpus()
    findings = []
    per_surah = []
    for s in range(1, 115):
        keys = corpus.surah_ayahs(s)
        if len(keys) < min_ayahs:
            continue
        vecs = [Counter(corpus.ayah_content_lemmas(*k)) for k in keys]
        obs, p, rot = ayah_level(vecs)
        mu = sum(rot) / len(rot)
        f = Finding(
            id=f"c17_ayah_{s}", category=CATEGORY,
            title=f"{corpus.meta[s]['name_tr']} ({s}): ayet düzeyi ayna skoru {obs:.3f} (rotasyon ort. {mu:.3f})",
            method="Ayna çiftleri (i, n+1-i) kosinüs ortalaması; döngüsel kaydırma null modeli (n rotasyon)",
            metric="ayna skoru", value=obs, null_p=p, effect_size=obs / mu if mu else None,
            detail=f"{len(keys)} ayet | rotasyonlar arası sıra: {sum(1 for x in rot if x >= obs) + 1}/{len(keys)}")
        per_surah.append(f)
        if len(keys) >= 40:
            bobs, bp, brot, blocks = block_level(vecs)
            bmu = sum(brot) / len(brot)
            pair_sims = [cosine(blocks[j], blocks[N_BLOCKS - 1 - j]) for j in range(N_BLOCKS // 2)]
            per_surah.append(Finding(
                id=f"c17_block_{s}", category=CATEGORY,
                title=f"{corpus.meta[s]['name_tr']} ({s}): {N_BLOCKS}-blok ayna skoru {bobs:.3f} (rotasyon ort. {bmu:.3f})",
                method=f"{N_BLOCKS} eşit ayet bloğu, ayna blok çiftleri kosinüs; döngüsel kaydırma null modeli",
                metric="blok ayna skoru", value=bobs, null_p=bp, effect_size=bobs / bmu if bmu else None,
                detail="Ayna blok çifti benzerlikleri (dış→iç): " + ", ".join(f"{x:.2f}" for x in pair_sims)))
    bh_adjust(per_surah)
    ayah_f = [f for f in per_surah if f.id.startswith('c17_ayah_')]
    block_f = [f for f in per_surah if f.id.startswith('c17_block_')]
    global_findings = []
    for lvl, group in (("ayet", ayah_f), ("blok", block_f)):
        m = len(group)
        k05 = sum(1 for f in group if f.null_p < 0.05)
        z = binom_z(k05, m, 0.05)
        sig = [f for f in group if f.q_value < 0.05]
        global_findings.append(Finding(
            id=f"c17_global_{'ayah' if lvl == 'ayet' else 'block'}", category=CATEGORY,
            title=(f"{lvl.capitalize()} düzeyinde {m} surenin {k05}'inde p<0.05 (rastlantı beklentisi {0.05 * m:.1f}); "
                   f"FDR sonrası {len(sig)} sure anlamlı"),
            method="Sure başına rotasyon p-değerleri; p<0.05 sayısı için binom z (H0: %5)",
            metric="binom z", value=z, null_p=two_sided_p_from_z(z) if z > 0 else 1.0,
            evidence=[f.title for f in sorted(group, key=lambda f: f.null_p)[:10]],
            detail="Negatif sonuç da raporlanır: rastlantı düzeyinde bir oran, sistematik bir halka yapısı "
                   "iddiasını DESTEKLEMEZ."))
    # Global bulgular da aynı kategori içi BH düzeltmesinden geçmeli; aksi hâlde
    # q_value=None kalır ve CLI (--findings) ile site ihracı bozulur.
    bh_adjust(global_findings)
    findings.extend(global_findings)
    findings.extend(sorted(per_surah, key=lambda f: f.null_p)[:15])
    return findings, {'per_surah': [f.to_dict() for f in per_surah]}


if __name__ == '__main__':
    fs, _ = run()
    for f in fs:
        q = f"{f.q_value:.4f}" if f.q_value is not None else "-"
        print(f"{f.id:16} {f.value:+.3f} p={f.null_p:.4f} q={q} | {f.title} | {f.detail[:110]}")
