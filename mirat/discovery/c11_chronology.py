#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kategori 11: Kronolojik Evrim (Nüzul Sırası)

Yöntemler:
  A. Üslup göstergeleri ~ nüzul sırası: Spearman rho + permütasyon p-değeri (114 sure)
  B. Tek kırılma noktası: her gösterge için nüzul sırasında en güçlü ikili bölünme
     (Welch t), permütasyonla anlamlılık; bulunan noktanın Mekke→Medine sınırıyla örtüşmesi
  C. Kök eğilimleri: frekansı >= 30 olan her kökün sure içi oranı ~ nüzul sırası
     (asimptotik Spearman p, BH-FDR); en güçlü yükselen/düşen kökler
"""

import math
import random
from collections import Counter, defaultdict

from mirat.features import get_corpus
from mirat.discovery.finding import Finding, spearman, permutation_p, two_sided_p_from_z, bh_adjust
from mirat.discovery import glossary

CATEGORY = "11. Kronolojik Evrim (Nüzul Sırası)"
N_PERM = 2000


def surah_profiles(corpus):
    """Her sure için üslup göstergeleri."""
    prof = {}
    for s in range(1, 115):
        keys = corpus.surah_ayahs(s)
        words = sum(corpus.ayah_word_count(*k) for k in keys)
        segs = [sg for k in keys for sg in corpus.ayah_segments(*k)]
        verbs = [sg for sg in segs if sg.tag == 'V']
        nv = max(1, len(verbs))
        lemmas = [sg.lemma for sg in segs if sg.lemma and sg.tag != 'P']
        pc = Counter((sg.person or '') + (sg.number or '') for sg in verbs)
        flags = Counter(f for sg in segs for f in sg.flags)
        prof[s] = {
            'Ortalama ayet uzunluğu (kelime)': words / len(keys),
            'Ayet sayısı': len(keys),
            'Yeni lemma oranı (ilk 60 içerik kelimesinde tekil lemma)': len(set(lemmas[:60])) / max(1, min(60, len(lemmas))),
            '"Biz" kipi fiil oranı (1P, ‰ fiil)': 1000 * pc['1P'] / nv,
            '"Ben" kipi fiil oranı (1S, ‰ fiil)': 1000 * pc['1S'] / nv,
            'Peygambere tekil hitap (2. tekil, ‰ fiil)': 1000 * pc['2S'] / nv,
            'Topluluğa hitap (2. çoğul, ‰ fiil)': 1000 * pc['2P'] / nv,
            'Emir kipi oranı (‰ fiil)': 1000 * sum(1 for v in verbs if v.aspect == 'IMPV') / nv,
            'Edilgen çatı oranı (‰ fiil)': 1000 * sum(1 for v in verbs if v.voice == 'PASS') / nv,
            'Geçmiş zaman (PERF) oranı (‰ fiil)': 1000 * sum(1 for v in verbs if v.aspect == 'PERF') / nv,
            'Soru edatı yoğunluğu (‰ kelime)': 1000 * flags['INTG'] / max(1, words),
            'Şart edatı yoğunluğu (‰ kelime)': 1000 * flags['COND'] / max(1, words),
            'Olumsuzluk edatı yoğunluğu (‰ kelime)': 1000 * flags['NEG'] / max(1, words),
            'Nida (ey!) yoğunluğu (‰ kelime)': 1000 * flags['VOC'] / max(1, words),
            'Tekit/vurgu edatı yoğunluğu (‰ kelime)': 1000 * (flags['EMPH'] + flags['CERT']) / max(1, words),
        }
    return prof


def welch_t(a, b):
    na, nb = len(a), len(b)
    ma, mb = sum(a) / na, sum(b) / nb
    va = sum((x - ma) ** 2 for x in a) / (na - 1) if na > 1 else 0
    vb = sum((x - mb) ** 2 for x in b) / (nb - 1) if nb > 1 else 0
    se = math.sqrt(va / na + vb / nb)
    return (mb - ma) / se if se > 0 else 0.0


def best_split(series, min_seg=10):
    best = (0.0, None)
    for k in range(min_seg, len(series) - min_seg + 1):
        t = abs(welch_t(series[:k], series[k:]))
        if t > best[0]:
            best = (t, k)
    return best


def run(corpus=None, seed=42):
    corpus = corpus or get_corpus()
    findings = []
    prof = surah_profiles(corpus)
    nuzul = corpus.surahs_by('nuzul')
    order_vals = [corpus.revelation_order(s) for s in range(1, 115)]
    # Mekke→Medine sınırı: nüzul sırasında ilk Medenî surenin konumu
    first_medinan_pos = next(i for i, s in enumerate(nuzul) if not corpus.is_meccan(s))

    # ---------------- A + B: üslup göstergeleri
    rng = random.Random(seed)
    for i, metric in enumerate(prof[1].keys()):
        vals = [prof[s][metric] for s in range(1, 115)]
        rho, p = permutation_p(spearman, order_vals, vals, n_perm=N_PERM, seed=seed + i)
        mk = [prof[s][metric] for s in range(1, 115) if corpus.is_meccan(s)]
        md = [prof[s][metric] for s in range(1, 115) if not corpus.is_meccan(s)]
        mmk, mmd = sum(mk) / len(mk), sum(md) / len(md)
        direction = "artıyor" if rho > 0 else "azalıyor"
        findings.append(Finding(
            id=f"c11_trend_{i:02d}", category=CATEGORY,
            title=f"{metric}: nüzul sırası ilerledikçe {direction}",
            method="Spearman rho, nüzul sırası (114 sure), 2000 permütasyon",
            metric="Spearman rho", value=rho, null_p=p, effect_size=rho,
            detail=f"Mekkî ort. {mmk:.2f} | Medenî ort. {mmd:.2f} (oran {mmd / mmk if mmk else float('nan'):.2f}x)"))

        # Kırılma noktası (nüzul sırasındaki dizi)
        series = [prof[s][metric] for s in nuzul]
        t_obs, k = best_split(series)
        hits = 0
        sh = list(series)
        for _ in range(300):  # kırılma taraması pahalı; 300 permütasyon
            rng.shuffle(sh)
            if best_split(sh)[0] >= t_obs:
                hits += 1
        p_cp = (hits + 1) / 301
        near = abs(k - first_medinan_pos) <= 3
        findings.append(Finding(
            id=f"c11_cp_{i:02d}", category=CATEGORY,
            title=f"{metric}: nüzul sırasında kırılma noktası {k}. sure civarında"
                  + (" (Mekke→Medine sınırıyla örtüşüyor)" if near else ""),
            method="En güçlü tek ikili bölünme (|Welch t|), 300 permütasyon",
            metric="|t| (bölünme)", value=t_obs, null_p=p_cp,
            evidence=[f"nüzul#{k}: {corpus.meta[nuzul[k]]['name_tr']}"],
            detail=f"Bulunan kırılma: nüzul sırası {k} | gerçek ilk Medenî sure konumu: {first_medinan_pos}"))

    # ---------------- C: kök eğilimleri
    # Not: sure içi oran ~ nüzul Spearman testi, kısa erken surelerde köklerin çoğu 0 olduğu için
    # uzunluk yanlılığı üretir (her kök "yükselir"). Bunun yerine her kökün Medenî token payı,
    # Medenî kelime payına karşı binom z ile test edilir; tokenlar ayet/sure içinde kümelendiği
    # için z'ler köklerden kestirilen aşırı yayılım katsayısıyla (quasi-binom, phi) düzeltilir.
    rf = corpus.root_frequencies()
    surah_words = {s: sum(corpus.ayah_word_count(*k) for k in corpus.surah_ayahs(s)) for s in range(1, 115)}
    total_words = sum(surah_words.values())
    md_share = sum(w for s, w in surah_words.items() if not corpus.is_meccan(s)) / total_words
    mean_order_all = sum(corpus.revelation_order(s) * w for s, w in surah_words.items()) / total_words
    root_counts = defaultdict(Counter)
    root_ayahs = defaultdict(list)
    for sg in corpus.segments:
        if sg.root and rf[sg.root] >= 30:
            root_counts[sg.root][sg.surah] += 1
            root_ayahs[sg.root].append((corpus.revelation_order(sg.surah), f"{sg.surah}:{sg.ayah}"))
    raw = []
    for root, cnt in root_counts.items():
        n_tok = sum(cnt.values())
        k_md = sum(c for s, c in cnt.items() if not corpus.is_meccan(s))
        z = (k_md - n_tok * md_share) / math.sqrt(n_tok * md_share * (1 - md_share))
        mean_order = sum(corpus.revelation_order(s) * c for s, c in cnt.items()) / n_tok
        raw.append((root, n_tok, k_md, z, mean_order))
    # Aşırı yayılım: medyan(z^2)/0.455 (ki-kare(1) medyanı) — uç değerlere dayanıklı kestirim
    z2 = sorted(r[3] ** 2 for r in raw)
    phi = max(1.0, z2[len(z2) // 2] / 0.4549)
    root_findings = []
    for root, n_tok, k_md, z, mean_order in raw:
        z_adj = z / math.sqrt(phi)
        p = two_sided_p_from_z(z_adj)
        share = k_md / n_tok
        log_ratio = math.log2(((k_md + 0.5) / (n_tok - k_md + 0.5)) / (md_share / (1 - md_share)))
        ev = sorted(root_ayahs[root], reverse=(z > 0))[:5]
        root_findings.append(Finding(
            id=f"c11_root_{root}", category=CATEGORY,
            title=f"Kök {glossary.label(root)}: {'Medenî dönemde yoğunlaşıyor' if z > 0 else 'Mekkî dönemde yoğunlaşıyor'}",
            method=f"Medenî token payı vs Medenî kelime payı ({md_share:.3f}), binom z / sqrt(phi={phi:.2f}), BH-FDR",
            metric="düzeltilmiş z", value=z_adj, null_p=p, effect_size=log_ratio,
            evidence=[e[1] for e in ev],
            detail=(f"Frekans {n_tok} | Medenî pay {share:.2f} (beklenen {md_share:.2f}) | "
                    f"token ağırlıklı ort. nüzul sırası {mean_order:.1f} (genel {mean_order_all:.1f})")))
    bh_adjust(root_findings)
    sig = sorted([f for f in root_findings if f.q_value is not None and f.q_value < 0.05], key=lambda f: f.value)
    keep = sig[:20] + sig[-20:] if len(sig) > 40 else sig
    findings.extend(keep)
    findings.append(Finding(
        id="c11_root_summary", category=CATEGORY,
        title=f"{len(root_findings)} sık kökün {len(sig)} tanesi Mekkî/Medenî dönemlerden birinde anlamlı yoğunlaşıyor (q<0.05)",
        method="Kök dönem taraması özeti (quasi-binom)", metric="anlamlı kök sayısı", value=len(sig),
        kind="descriptive",
        detail=(f"Medenî yoğunlaşan: {sum(1 for f in sig if f.value > 0)} | Mekkî yoğunlaşan: "
                f"{sum(1 for f in sig if f.value < 0)} | aşırı yayılım phi={phi:.2f}")))
    # Betimsel: phi muhafazakâr olduğundan etki büyüklüğüne (log2 oran) göre en uç kökler (frekans >= 50)
    big = sorted([f for f in root_findings if rf[f.id[len('c11_root_'):]] >= 50], key=lambda f: f.effect_size)
    for tag, group in (("Mekkî", big[:15]), ("Medenî", big[-15:][::-1])):
        findings.append(Finding(
            id=f"c11_toproots_{'mk' if tag == 'Mekkî' else 'md'}", category=CATEGORY,
            title=f"En belirgin {tag} kökler (etki büyüklüğü sıralaması, frekans>=50)",
            method="log2(Medenî/Mekkî token oranı ÷ kelime oranı); betimsel, test değil",
            metric="log2 oran", value=group[0].effect_size if group else 0.0, kind="descriptive",
            evidence=[f"{glossary.label(f.id[len('c11_root_'):])} ({f.effect_size:+.2f})" for f in group]))

    bh_adjust([f for f in findings if not f.id.startswith('c11_root_')])
    return findings, {'profiles': prof, 'first_medinan_pos': first_medinan_pos}


if __name__ == '__main__':
    fs, _ = run()
    for f in fs:
        if f.id.startswith('c11_trend') or f.id.startswith('c11_cp') or f.id == 'c11_root_summary':
            print(f"{f.id:14} {f.value:+.3f} p={f.null_p} q={f.q_value} | {f.title} | {f.detail}")
