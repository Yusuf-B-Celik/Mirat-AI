#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kategori 14: Tekrar ve Formül Yapıları

Yöntemler:
  A. Nakarat (refrain) tespiti: aynı sure içinde birebir tekrar eden ayetler
     (ör. Rahmân 55: "Febi-eyyi âlâi rabbikümâ tükezzibân" ×31).
  B. Müteşâbih (benzer) ayet ağı: içerik lemma kümeleri Jaccard >= 0.7 olan ayet çiftleri;
     sureler arası benzer çiftlerin nüzul sırası yakınlığı, etiket permütasyonuna karşı.
  C. Formül n-gramları: >= 2 farklı surede geçen 3-6'lı içerik lemma dizileri (maksimal olanlar);
     sure formül yoğunluğu ~ nüzul sırası (Spearman, permütasyon).
  D. Fâsıla-anlam uyumu: ayet sonu ilahî isim çiftleri (ör. غفور رحيم) ile ayet içi kökler
     arasındaki ilişki (karşılıklı bilgi, ayet sonlarının karıştırılmasına karşı) + en güçlü
     çift↔kök eşleşmeleri (Fisher, BH-FDR).
"""

import math
import random
from collections import Counter, defaultdict

from mirat.features import get_corpus
from mirat.discovery.finding import Finding, spearman, permutation_p, bh_adjust, jaccard, strip_diacritics
from mirat.discovery import glossary

CATEGORY = "14. Tekrar ve Formül Yapıları"
STOP_LEMMA_POSTINGS = 400   # çok sık lemmalar aday üretiminde atlanır (Jaccard'a dahildir)


def ayah_text(corpus, key):
    words = defaultdict(str)
    for sg in corpus.ayah_segments(*key):
        words[sg.word] += sg.form
    return " ".join(strip_diacritics(words[w]) for w in sorted(words))


def _fisher_greater(a, b, c, d):
    def lc(n, k):
        return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    r1, c1, n = a + b, a + c, a + b + c + d
    denom = lc(n, c1)
    return min(1.0, sum(math.exp(lc(r1, x) + lc(n - r1, c1 - x) - denom) for x in range(a, min(r1, c1) + 1)))


def ending_pair(corpus, key):
    """Ayet son iki kelimesi ilahî sıfat (ADJ, eril tekil) ise lemma çifti döner."""
    by_word = defaultdict(list)
    for sg in corpus.ayah_segments(*key):
        by_word[sg.word].append(sg)
    ws = sorted(by_word)
    if len(ws) < 3:
        return None
    out = []
    # Korpus ADJ etiketini yalnızca ikinci kelimeye koyar (غَفُورٌ رَحِيمٌ → yalnızca رَحِيم ADJ);
    # bu yüzden son kelime ADJ eril tekil, bir önceki kelime eril tekil (MS) kökü olan isim olmalıdır.
    w_prev, w_last = ws[-2], ws[-1]
    last = [sg for sg in by_word[w_last] if sg.tag == 'N' and 'ADJ' in sg.flags and sg.gender == 'M' and sg.root]
    prev = [sg for sg in by_word[w_prev] if sg.tag == 'N' and sg.gender == 'M' and sg.number == 'S'
            and sg.root and 'PN' not in sg.flags and 'PRON' not in sg.flags]
    if not last or not prev:
        return None
    out = [prev[0].lemma, last[0].lemma]
    return tuple(out)


def run(corpus=None, seed=42):
    corpus = corpus or get_corpus()
    rng = random.Random(seed)
    findings = []
    keys = corpus.ayah_keys

    # ============ A. Nakaratlar
    texts = {k: ayah_text(corpus, k) for k in keys}
    refrains = []
    for s in range(1, 115):
        c = Counter(texts[k] for k in corpus.surah_ayahs(s) if len(texts[k].split()) >= 3)
        for t, n in c.items():
            if n >= 3:
                first = next(k for k in corpus.surah_ayahs(s) if texts[k] == t)
                refrains.append((s, n, t, first))
    refrains.sort(key=lambda x: -x[1])
    for s, n, t, first in refrains[:12]:
        poss = [k[1] for k in corpus.surah_ayahs(s) if texts[k] == t]
        gaps = [b - a for a, b in zip(poss, poss[1:])]
        findings.append(Finding(
            id=f"c14_refrain_{s}_{first[1]}", category=CATEGORY,
            title=f"{corpus.meta[s]['name_tr']} suresinde nakarat: '{t}' ×{n}",
            method="Aynı sure içinde harekesiz metni birebir tekrar eden ayetler (>= 3 kelime, >= 3 tekrar)",
            metric="tekrar", value=n, kind="descriptive",
            evidence=[f"{s}:{p}" for p in poss][:40],
            detail=f"Konumlar arası aralıklar: {gaps[:40]}"))
    findings.append(Finding(
        id="c14_refrain_summary", category=CATEGORY,
        title=f"{len(refrains)} nakarat örüntüsü {len({r[0] for r in refrains})} surede bulundu",
        method="Nakarat taraması özeti", metric="nakarat sayısı", value=len(refrains), kind="descriptive",
        evidence=[f"{corpus.meta[s]['name_tr']} ×{n}" for s, n, _, _ in refrains]))

    # ============ B. Müteşâbih ayet ağı
    lemsets = {k: set(corpus.ayah_content_lemmas(*k)) for k in keys}
    postings = defaultdict(list)
    for k, ls in lemsets.items():
        for l in ls:
            postings[l].append(k)
    pairs = []
    for k in keys:
        ls = lemsets[k]
        if len(ls) < 4:
            continue
        cand = Counter()
        for l in ls:
            p = postings[l]
            if len(p) > STOP_LEMMA_POSTINGS:
                continue
            for o in p:
                if o > k:
                    cand[o] += 1
        for o, shared in cand.items():
            if shared < 2 or len(lemsets[o]) < 4:
                continue
            j = jaccard(ls, lemsets[o])
            if j >= 0.7:
                pairs.append((k, o, j))
    cross = [(a, b, j) for a, b, j in pairs if a[0] != b[0]]
    within = len(pairs) - len(cross)

    def mean_order_gap(pp, lab):
        return sum(abs(corpus.revelation_order(lab[a]) - corpus.revelation_order(lab[b])) for a, b, _ in pp) / len(pp)
    nodes = sorted({x for a, b, _ in cross for x in (a, b)})
    lab = {n: n[0] for n in nodes}
    obs_gap = mean_order_gap(cross, lab)
    vals = list(lab.values())
    hits, null = 0, []
    for _ in range(1000):
        rng.shuffle(vals)
        perm = dict(zip(nodes, vals))
        g = mean_order_gap(cross, perm)
        null.append(g)
        hits += g <= obs_gap
    mu = sum(null) / len(null)
    surah_pair = Counter(tuple(sorted((a[0], b[0]))) for a, b, _ in cross)
    findings.append(Finding(
        id="c14_mutashabih_chronology", category=CATEGORY,
        title=(f"{len(cross)} sureler arası benzer ayet çifti, nüzul sırasında birbirine yakın surelerde yoğunlaşıyor "
               f"(ort. mesafe {obs_gap:.1f} vs rastgele {mu:.1f})" if obs_gap < mu else
               f"{len(cross)} sureler arası benzer ayet çifti nüzul yakınlığı göstermiyor ({obs_gap:.1f} vs {mu:.1f})"),
        method="Jaccard(içerik lemma) >= 0.7 çiftler; sure etiketleri ayetler arasında karıştırılır (1000 permütasyon)",
        metric="ort. nüzul sırası mesafesi", value=obs_gap, null_p=(hits + 1) / 1001, effect_size=obs_gap / mu,
        evidence=[f"{a[0]}:{a[1]} ~ {b[0]}:{b[1]} (J={j:.2f})" for a, b, j in sorted(cross, key=lambda x: -x[2])[:20]],
        detail=f"Toplam benzer çift {len(pairs)} (sure içi {within}). En çok paylaşan sure çiftleri: "
               + ", ".join(f"{corpus.meta[x]['name_tr']}-{corpus.meta[y]['name_tr']} ({c})" for (x, y), c in surah_pair.most_common(8))))

    # ============ C. Formül n-gramları
    seqs = {k: corpus.ayah_content_lemmas(*k) for k in keys}
    formulas = {}
    for n in range(6, 2, -1):
        occ = defaultdict(list)
        for k, seq in seqs.items():
            for i in range(len(seq) - n + 1):
                occ[tuple(seq[i:i + n])].append(k)
        for g, ks in occ.items():
            if len(ks) >= 3 and len({x[0] for x in ks}) >= 2:
                # maksimal: daha uzun bir formülün parçası değilse
                if not any(len(G) > n and any(G[i:i + n] == g for i in range(len(G) - n + 1)) and
                           len(formulas[G]) >= 0.85 * len(ks) for G in formulas):
                    formulas[g] = ks
    top = sorted(formulas.items(), key=lambda x: (-len(x[1]), -len(x[0])))
    for i, (g, ks) in enumerate(top[:10]):
        findings.append(Finding(
            id=f"c14_formula_{i:02d}", category=CATEGORY,
            title=f"Formül: '{' '.join(g)}' — {len(ks)} kez, {len({x[0] for x in ks})} surede",
            method="Maksimal içerik-lemma n-gramı (3-6), >= 3 geçiş, >= 2 sure", metric="geçiş", value=len(ks),
            kind="descriptive", evidence=[f"{a}:{b}" for a, b in ks[:25]]))
    # Formül yoğunluğu: 4-gram'ı başka bir surede de geçen içerik tokenlarının oranı
    occ4 = defaultdict(set)
    for k, seq in seqs.items():
        for i in range(len(seq) - 3):
            occ4[tuple(seq[i:i + 4])].add(k[0])
    dens = {}
    dens_ctrl = {}   # uzunluk kontrolü: yalnızca >= 8 içerik lemmalı ayetler
    for s in range(1, 115):
        cov = tot = cov_c = tot_c = 0
        for k in corpus.surah_ayahs(s):
            seq = seqs[k]
            mark = [False] * len(seq)
            for i in range(len(seq) - 3):
                if len(occ4[tuple(seq[i:i + 4])] - {s}) >= 1:
                    for j in range(i, i + 4):
                        mark[j] = True
            cov += sum(mark)
            tot += len(seq)
            if len(seq) >= 8:
                cov_c += sum(mark)
                tot_c += len(seq)
        dens[s] = cov / max(1, tot)
        if tot_c >= 30:
            dens_ctrl[s] = cov_c / tot_c
    order_vals = [corpus.revelation_order(s) for s in range(1, 115)]
    rho, p = permutation_p(spearman, order_vals, [dens[s] for s in range(1, 115)], n_perm=2000, seed=seed)
    cs = sorted(dens_ctrl)
    rho_c, p_c = permutation_p(spearman, [corpus.revelation_order(s) for s in cs], [dens_ctrl[s] for s in cs],
                               n_perm=2000, seed=seed + 1)
    findings.append(Finding(
        id="c14_formula_density_trend_ctrl", category=CATEGORY,
        title=(f"Uzunluk kontrolünde (yalnızca uzun ayetler) formül yoğunluğu–nüzul ilişkisi: rho={rho_c:+.2f}"
               + (" — eğilim uzunluktan bağımsız" if p_c < 0.05 else " — eğilim büyük ölçüde ayet uzunluğundan kaynaklanıyor")),
        method="Yalnızca >= 8 içerik lemmalı ayetler, >= 30 token olan sureler; Spearman, 2000 permütasyon",
        metric="Spearman rho", value=rho_c, null_p=p_c, effect_size=rho_c, detail=f"{len(cs)} sure"))
    mk = [dens[s] for s in range(1, 115) if corpus.is_meccan(s)]
    md = [dens[s] for s in range(1, 115) if not corpus.is_meccan(s)]
    findings.append(Finding(
        id="c14_formula_density_trend", category=CATEGORY,
        title=f"Sure formül yoğunluğu nüzul sırasıyla {'artıyor' if rho > 0 else 'azalıyor'} (rho={rho:+.2f})",
        method="İçerik tokenlarının başka surelerle paylaşılan 4-gram içinde kalma oranı; Spearman, 2000 permütasyon",
        metric="Spearman rho", value=rho, null_p=p, effect_size=rho,
        evidence=[f"{corpus.meta[s]['name_tr']} %{100 * dens[s]:.0f}" for s in sorted(dens, key=lambda x: -dens[x])[:10]],
        detail=f"Mekkî ort. %{100 * sum(mk) / len(mk):.1f} | Medenî ort. %{100 * sum(md) / len(md):.1f} | "
               f"toplam maksimal formül: {len(formulas)}"))

    # ============ D. Fâsıla-anlam uyumu
    endings = {k: ending_pair(corpus, k) for k in keys}
    endings = {k: v for k, v in endings.items() if v}
    pair_freq = Counter(endings.values())
    common = {p for p, c in pair_freq.items() if c >= 8}
    ek = [k for k in endings if endings[k] in common]
    # ayet içi kökler, son iki kelime hariç
    def body_roots(k):
        segs = corpus.ayah_segments(*k)
        last_words = sorted({sg.word for sg in segs})[-2:]
        return {sg.root for sg in segs if sg.root and sg.word not in last_words}
    broots = {k: body_roots(k) for k in ek}
    root_df = Counter(r for k in ek for r in broots[k])
    roots_ok = {r for r, c in root_df.items() if c >= 5}

    def mutual_info(labels):
        n = len(ek)
        pc = Counter(labels)
        joint = Counter()
        for k, lb in zip(ek, labels):
            for r in broots[k] & roots_ok:
                joint[(lb, r)] += 1
        mi = 0.0
        for (lb, r), c in joint.items():
            mi += (c / n) * math.log2(c * n / (pc[lb] * root_df[r]))
        return mi
    labels = [endings[k] for k in ek]
    mi_obs = mutual_info(labels)
    sh = list(labels)
    hits, null = 0, []
    for _ in range(300):
        rng.shuffle(sh)
        m = mutual_info(sh)
        null.append(m)
        hits += m >= mi_obs
    mu = sum(null) / len(null)
    # Daha katı null: sonlar yalnızca aynı sure içinde karıştırılır (sure konusu karıştırıcısı dışlanır)
    groups = defaultdict(list)
    for i, k in enumerate(ek):
        groups[k[0]].append(i)
    hits_w, null_w = 0, []
    for _ in range(300):
        sw = list(labels)
        for idx in groups.values():
            vals = [labels[i] for i in idx]
            rng.shuffle(vals)
            for i, v in zip(idx, vals):
                sw[i] = v
        m = mutual_info(sw)
        null_w.append(m)
        hits_w += m >= mi_obs
    mu_w = sum(null_w) / len(null_w)
    findings.append(Finding(
        id="c14_fasila_semantic_coherence", category=CATEGORY,
        title=f"Ayet sonu ilahî isim çiftleri ayetin içeriğiyle uyumlu: karşılıklı bilgi rastlantının {mi_obs / mu:.2f} katı",
        method=f"{len(common)} sık sonlanma çifti (>= 8), {len(ek)} ayet; sonlar ayetler arasında karıştırılır (300 permütasyon)",
        metric="karşılıklı bilgi (bit)", value=mi_obs, null_p=(hits + 1) / 301, effect_size=mi_obs / mu,
        evidence=[f"{a} {b} ×{c}" for (a, b), c in pair_freq.most_common(12)],
        detail=f"Gözlenen MI {mi_obs:.4f} | null ort. {mu:.4f}"))
    findings.append(Finding(
        id="c14_fasila_semantic_coherence_within", category=CATEGORY,
        title=(f"Sure içi karıştırmada da fâsıla-içerik uyumu {'korunuyor' if hits_w < 15 else 'KORUNMUYOR'} "
               f"(MI rastlantının {mi_obs / mu_w:.2f} katı)"),
        method="Aynı sonlanma-kök MI istatistiği; sonlar yalnızca aynı sure içinde karıştırılır (300 permütasyon)",
        metric="karşılıklı bilgi (bit)", value=mi_obs, null_p=(hits_w + 1) / 301, effect_size=mi_obs / mu_w,
        detail=f"Sure içi null ort. {mu_w:.4f}. Bu test, uyumun sure konusundan değil ayet düzeyinden geldiğini sınar."))
    assoc = []
    for pr in common:
        ks = [k for k in ek if endings[k] == pr]
        for r in roots_ok:
            a = sum(1 for k in ks if r in broots[k])
            if a < 3:
                continue
            b = len(ks) - a
            c = root_df[r] - a
            d = len(ek) - len(ks) - c
            pv = _fisher_greater(a, b, c, d)
            lift = (a / len(ks)) / (root_df[r] / len(ek))
            assoc.append(Finding(
                id=f"c14_fasila_{pr[0]}_{pr[1]}_{r}", category=CATEGORY,
                title=f"'{pr[0]} {pr[1]}' ile biten ayetlerde kök {glossary.label(r)} {lift:.1f} kat sık",
                method="Sonlanma çifti × gövde kökü, tek yönlü Fisher, BH-FDR", metric="lift", value=lift,
                null_p=pv, effect_size=lift,
                evidence=[f"{k[0]}:{k[1]}" for k in ks if r in broots[k]][:10], detail=f"{a}/{len(ks)} ayet"))
    bh_adjust(assoc)
    sig = sorted([f for f in assoc if f.q_value < 0.05], key=lambda f: f.null_p)
    findings.extend(sig[:20])
    findings.append(Finding(
        id="c14_fasila_assoc_summary", category=CATEGORY,
        title=f"{len(assoc)} sonlanma-kök eşleşmesinin {len(sig)} tanesi anlamlı (q<0.05)",
        method="Fâsıla-anlam taraması özeti", metric="anlamlı eşleşme", value=len(sig), kind="descriptive"))

    bh_adjust([f for f in findings if not f.id.startswith('c14_fasila_')
               or f.id.startswith('c14_fasila_semantic_coherence')])
    return findings, {'refrains': refrains, 'near_duplicates': pairs, 'formulas': len(formulas)}


if __name__ == '__main__':
    fs, ex = run()
    for f in fs:
        q = f"{f.q_value:.4f}" if f.q_value is not None else "-"
        print(f"{f.id:34} {f.value:+.3f} q={q} | {f.title} | {f.detail[:160]}")
