#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kategori 18: Bilgi Kuramı ve Metin Dinamiği

Yöntemler:
  A. Zipf ve Heaps yasaları (lemma ve kök düzeyinde) — betimsel üsler.
  B. Kök patlamalılığı (burstiness): ardışık geçişler arası mesafenin B=(σ-μ)/(σ+μ) katsayısı;
     tüm token dizisi karıştırılarak (50 kez) kök bazında null; en "konu-bağımlı" kökler.
  C. Uzun menzilli bellek: ayet uzunluğu dizisinde (mushaf sırası) DFA üssü α;
     null: ayetler yalnızca sure İÇİNDE karıştırılır (sure düzeyi farklar korunur).
  D. Fâsıla (ayet sonu harfi) dinamiği: kafiye değişim noktaları ile konu sınırlarının örtüşmesi —
     kafiye değişen geçişlerde ardışık ayetlerin sözcüksel benzerliği vs değişmeyenler
     (sure içi permütasyon); sure kafiye entropisi ~ nüzul sırası.
"""

import math
import random
from collections import Counter, defaultdict

from mirat.features import get_corpus
from mirat.discovery.finding import Finding, spearman, permutation_p, bh_adjust, strip_diacritics, pearson
from mirat.discovery import glossary

CATEGORY = "18. Bilgi Kuramı ve Metin Dinamiği"


def loglog_slope(xs, ys):
    lx = [math.log(x) for x in xs]
    ly = [math.log(y) for y in ys]
    n = len(lx)
    mx, my = sum(lx) / n, sum(ly) / n
    sxx = sum((a - mx) ** 2 for a in lx)
    return sum((a - mx) * (b - my) for a, b in zip(lx, ly)) / sxx if sxx else 0.0


def zipf_exponent(counts, top=1000):
    freqs = sorted(counts.values(), reverse=True)[:top]
    return -loglog_slope(range(1, len(freqs) + 1), freqs)


def heaps_exponent(tokens):
    seen, xs, ys = set(), [], []
    step = max(1, len(tokens) // 200)
    for i, t in enumerate(tokens, 1):
        seen.add(t)
        if i % step == 0 and i >= 1000:
            xs.append(i)
            ys.append(len(seen))
    return loglog_slope(xs, ys)


def burstiness(positions):
    if len(positions) < 3:
        return None
    gaps = [b - a for a, b in zip(positions, positions[1:])]
    mu = sum(gaps) / len(gaps)
    sd = math.sqrt(sum((g - mu) ** 2 for g in gaps) / len(gaps))
    return (sd - mu) / (sd + mu) if (sd + mu) else 0.0


def dfa_alpha(series, scales=None):
    n = len(series)
    m = sum(series) / n
    prof, acc = [], 0.0
    for x in series:
        acc += x - m
        prof.append(acc)
    if scales is None:
        scales = sorted({int(round(4 * (n / 16) ** (i / 14))) for i in range(15)})
    Fs, used = [], []
    for s in scales:
        nseg = n // s
        if nseg < 4:
            continue
        tot = 0.0
        xs = list(range(s))
        mx = (s - 1) / 2
        sxx = sum((x - mx) ** 2 for x in xs)
        for k in range(nseg):
            seg = prof[k * s:(k + 1) * s]
            my = sum(seg) / s
            b = sum((x - mx) * (y - my) for x, y in zip(xs, seg)) / sxx
            a = my - b * mx
            tot += sum((y - (a + b * x)) ** 2 for x, y in zip(xs, seg))
        Fs.append(math.sqrt(tot / (nseg * s)))
        used.append(s)
    return loglog_slope(used, Fs)


def ayah_rhyme(corpus, key):
    words = defaultdict(str)
    for sg in corpus.ayah_segments(*key):
        words[sg.word] += sg.form
    if not words:
        return None
    last = strip_diacritics(words[max(words)])
    last = ''.join(ch for ch in last if '\u0621' <= ch <= '\u064A')
    return last[-1] if last else None


def entropy(counter):
    n = sum(counter.values())
    return max(0.0, -sum(c / n * math.log2(c / n) for c in counter.values() if c))


def run(corpus=None, seed=42):
    corpus = corpus or get_corpus()
    rng = random.Random(seed)
    findings = []
    keys = corpus.ayah_keys

    # ============ A. Zipf / Heaps
    lem_tokens = [sg.lemma for k in keys for sg in corpus.ayah_segments(*k) if sg.lemma and sg.tag != 'P']
    root_tokens = [sg.root for k in keys for sg in corpus.ayah_segments(*k) if sg.root]
    zl, zr = zipf_exponent(Counter(lem_tokens)), zipf_exponent(Counter(root_tokens))
    hl, hr = heaps_exponent(lem_tokens), heaps_exponent(root_tokens)
    findings.append(Finding(
        id="c18_zipf_heaps", category=CATEGORY,
        title=f"Zipf üssü: lemma {zl:.2f}, kök {zr:.2f} | Heaps üssü: lemma {hl:.2f}, kök {hr:.2f}",
        method="İlk 1000 sıra log-log eğimi (Zipf); kümülatif kelime dağarcığı büyümesi (Heaps)",
        metric="Zipf üssü (lemma)", value=zl, kind="descriptive",
        detail=f"{len(lem_tokens)} içerik lemma tokenı, {len(set(lem_tokens))} farklı lemma; {len(set(root_tokens))} farklı kök. "
               "Doğal dillerde Zipf üssü tipik olarak ~1, Heaps üssü 0.4-0.7 aralığındadır."))

    # ============ B. Kök patlamalılığı
    pos = defaultdict(list)
    for i, r in enumerate(root_tokens):
        pos[r].append(i)
    cand = [r for r, p in pos.items() if len(p) >= 40]
    obs_b = {r: burstiness(pos[r]) for r in cand}
    null_b = defaultdict(list)
    sh = list(root_tokens)
    for _ in range(50):
        rng.shuffle(sh)
        pp = defaultdict(list)
        for i, r in enumerate(sh):
            pp[r].append(i)
        for r in cand:
            null_b[r].append(burstiness(pp[r]))
    burst = []
    for r in cand:
        nb = null_b[r]
        mu = sum(nb) / len(nb)
        sd = math.sqrt(sum((x - mu) ** 2 for x in nb) / (len(nb) - 1)) or 1e-9
        burst.append((r, obs_b[r], (obs_b[r] - mu) / sd, len(pos[r])))
    burst.sort(key=lambda x: -x[1])
    n_sig = sum(1 for b in burst if b[2] > 3)
    findings.append(Finding(
        id="c18_burstiness", category=CATEGORY,
        title=f"{len(burst)} sık kökün {n_sig}'i rastlantıdan belirgin biçimde kümeleniyor (z>3); en patlamalı: "
              + ", ".join(glossary.label(b[0]) for b in burst[:5]),
        method="Geçişler arası mesafe B=(σ-μ)/(σ+μ); null: tüm kök dizisi 50 kez karıştırılır",
        metric="kümelenen kök oranı", value=n_sig / len(burst), kind="descriptive",
        evidence=[f"{glossary.label(r)} B={b:.2f} (n={n})" for r, b, z, n in burst[:20]],
        detail="En düzenli (homojen dağılan) kökler: " + ", ".join(f"{glossary.label(r)} B={b:.2f}" for r, b, z, n in burst[-8:])))

    # ============ C. DFA uzun menzilli bellek
    series = [corpus.ayah_word_count(*k) for k in keys]
    alpha = dfa_alpha(series)
    by_s = defaultdict(list)
    for i, k in enumerate(keys):
        by_s[k[0]].append(i)
    null_a = []
    for _ in range(40):
        ss = list(series)
        for idx in by_s.values():
            vals = [series[i] for i in idx]
            rng.shuffle(vals)
            for i, v in zip(idx, vals):
                ss[i] = v
        null_a.append(dfa_alpha(ss))
    mu_a = sum(null_a) / len(null_a)
    p_a = (sum(1 for x in null_a if x >= alpha) + 1) / (len(null_a) + 1)
    full_shuffle = list(series)
    rng.shuffle(full_shuffle)
    alpha_full = dfa_alpha(full_shuffle)
    findings.append(Finding(
        id="c18_dfa_ayah_length", category=CATEGORY,
        title=(f"Ayet uzunluğu dizisinde DFA α={alpha:.3f} (tam karıştırma {alpha_full:.3f}, sure içi karıştırma {mu_a:.3f}): "
               f"uzun menzilli belleğin %{100 * (alpha - mu_a) / max(1e-9, alpha - alpha_full):.0f}'i sure İÇİ sıralamadan, "
               f"geri kalanı sureler arası farklardan geliyor"),
        method="Detrended Fluctuation Analysis (mushaf sırası, 6236 ayet); null: sure içi karıştırma (40 kez)",
        metric="DFA α", value=alpha, null_p=p_a, effect_size=alpha - mu_a,
        detail="α=0.5 belleksiz, α>0.5 kalıcı korelasyon. Sure içi null sure düzeyi farkları korur; "
               "α'nın bu null'u aşması, sure İÇİNDE de ayet uzunluklarının düzenli (rastgele olmayan) ilerlediğini gösterir."))

    # ============ D. Fâsıla dinamiği
    rhyme = {k: ayah_rhyme(corpus, k) for k in keys}
    vec = {k: set(corpus.ayah_content_lemmas(*k)) for k in keys}

    def jac(a, b):
        return len(a & b) / len(a | b) if (a or b) else 0.0
    trans = []   # (surah, changed, sim)
    for s in range(1, 115):
        ks = corpus.surah_ayahs(s)
        for a, b in zip(ks, ks[1:]):
            trans.append((s, rhyme[a] != rhyme[b], jac(vec[a], vec[b])))

    def stat(tr):
        ch = [x[2] for x in tr if x[1]]
        nc = [x[2] for x in tr if not x[1]]
        return (sum(nc) / len(nc)) - (sum(ch) / len(ch)) if ch and nc else 0.0
    obs = stat(trans)
    by_s_tr = defaultdict(list)
    for t in trans:
        by_s_tr[t[0]].append(t)
    hits = 0
    for _ in range(1000):
        perm = []
        for s, tr in by_s_tr.items():
            flags = [t[1] for t in tr]
            rng.shuffle(flags)
            perm.extend((s, f, t[2]) for f, t in zip(flags, tr))
        hits += stat(perm) >= obs
    n_ch = sum(1 for t in trans if t[1])
    ch_sims = [t[2] for t in trans if t[1]]
    nc_sims = [t[2] for t in trans if not t[1]]
    findings.append(Finding(
        id="c18_rhyme_boundary", category=CATEGORY,
        title=(f"Kafiye (fâsıla harfi) değiştiğinde ardışık ayetlerin sözcüksel benzerliği düşüyor: "
               f"{sum(ch_sims) / len(ch_sims):.3f} vs {sum(nc_sims) / len(nc_sims):.3f} (etki küçük ama tutarlı: kafiye kısmen konu sınırı işaretidir)"
               if obs > 0 else "Kafiye değişimi konu sınırlarıyla örtüşmüyor"),
        method="Ardışık ayet çiftlerinin içerik-lemma Jaccard benzerliği, kafiye değişen vs değişmeyen; sure içi etiket permütasyonu (1000)",
        metric="benzerlik farkı", value=obs, null_p=(hits + 1) / 1001,
        effect_size=(sum(nc_sims) / len(nc_sims)) / max(1e-9, sum(ch_sims) / len(ch_sims)),
        detail=f"{len(trans)} geçiş, {n_ch} kafiye değişimi"))
    ent = {}
    for s in range(1, 115):
        c = Counter(rhyme[k] for k in corpus.surah_ayahs(s) if rhyme[k])
        if sum(c.values()) >= 10:
            ent[s] = entropy(c)
    ss = sorted(ent)
    rho, p = permutation_p(spearman, [corpus.revelation_order(s) for s in ss], [ent[s] for s in ss], n_perm=2000, seed=seed)
    persist = sum(1 for t in trans if not t[1]) / len(trans)
    findings.append(Finding(
        id="c18_rhyme_entropy_trend", category=CATEGORY,
        title=f"Sure kafiye entropisi nüzul sırasıyla {'artıyor' if rho > 0 else 'azalıyor'} (rho={rho:+.2f})",
        method="Ayet sonu harfi dağılımının Shannon entropisi (>= 10 ayetli sureler); Spearman, 2000 permütasyon",
        metric="Spearman rho", value=rho, null_p=p, effect_size=rho,
        evidence=[f"{corpus.meta[s]['name_tr']} H={ent[s]:.2f}" for s in sorted(ent, key=lambda x: ent[x])[:8]],
        detail=f"Genel kafiye sürekliliği (ardışık ayetlerde aynı harf): %{100 * persist:.1f}. "
               "Kanıt: en tek-kafiyeli sureler."))

    bh_adjust(findings)
    return findings, {'dfa_alpha': alpha, 'zipf': (zl, zr)}


if __name__ == '__main__':
    fs, _ = run()
    for f in fs:
        q = f"{f.q_value:.4f}" if f.q_value is not None else "-"
        print(f"{f.id:24} {f.value:+.3f} q={q} | {f.title} | {f.detail[:160]} | {f.evidence[:6]}")
