#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kategori 16: Zıt Anlam (Tıbâk) Sayımı — LLM etiketli, deterministik test edilen

Girdi: veriler/lexicon/root_lexicon.json içindeki, İKİ bağımsız modelin uzlaştığı zıt-kök çiftleri.
LLM yalnızca "hangi kökler zıttır" etiketini verir; tüm sayımlar ve testler aşağıda deterministiktir.

Testler:
  A. Eşbulunma (tıbâk): zıt çiftler aynı ayette, (i) partnerleri rastgele yeniden eşlenmiş zıt-kök
     havuzuna ve (ii) frekansı eşleştirilmiş rastgele kök çiftlerine göre daha sık mı birlikte geçiyor?
  B. Frekans dengesi (sistematik simetri testi): zıt çiftlerin frekans oranı |log2(fa/fb)|, partnerler
     rastgele yeniden eşlendiğinde beklenenden daha mı dengeli? Bu test, tek tek seçilmiş "eşit sayı"
     iddialarının aksine TÜM uzlaşılmış çiftleri kapsar (seçim yanlılığı yoktur).
  C. Tam eşit frekanslı zıt çiftler: gözlenen sayı vs aynı yeniden eşleme null'unda beklenen.
"""

import math
import random
from collections import Counter, defaultdict

from mirat.features import get_corpus
from mirat.discovery.finding import Finding, bh_adjust, mann_whitney_z, two_sided_p_from_z
from mirat.discovery import glossary
from mirat.discovery.lexicon import load_merged

CATEGORY = "16. Zıt Anlam (Tıbâk) Sayımı"
N_PERM = 10000
MIN_FREQ = 5


def run(corpus=None, seed=42, merged=None):
    corpus = corpus or get_corpus()
    merged = merged if merged is not None else load_merged()
    if not merged or not merged.get("agreed_pairs"):
        return [Finding(id="c16_unavailable", category=CATEGORY, kind="descriptive", value=0,
                        title="Zıt-anlam sözlüğü bulunamadı (LLM etiketleme henüz çalıştırılmadı)",
                        method="python3 -m mirat.discovery.lexicon --model ... && --merge", metric="-")], {}
    rng = random.Random(seed)
    freq = corpus.root_frequencies()
    root_ayahs = defaultdict(set)
    for sg in corpus.segments:
        if sg.root:
            root_ayahs[sg.root].add((sg.surah, sg.ayah))
    n_ay = len(corpus.ayah_keys)
    pairs = [(a, b) for a, b in merged["agreed_pairs"] if freq.get(a, 0) >= MIN_FREQ and freq.get(b, 0) >= MIN_FREQ]
    findings = []
    findings.append(Finding(
        id="c16_lexicon_agreement", category=CATEGORY, llm_assisted=True, kind="descriptive",
        title=(f"İki model {merged['n_common']} kökü etiketledi: zıt-kök varlığında Cohen κ={merged['kappa_has_antonym']:.2f}, "
               f"anlam alanında κ={merged['kappa_field']:.2f}; {len(merged['agreed_pairs'])} çiftte birebir uzlaşı"),
        method=f"Modeller: {', '.join(merged['models'])}; aynı istem, sıcaklık 0", metric="kappa",
        value=merged['kappa_has_antonym'] or 0.0,
        evidence=[f"{glossary.label(a)} ↔ {glossary.label(b)}" for a, b in merged["agreed_pairs"][:40]],
        detail=f"Model A çift: {merged['pairs_model_a']} | Model B çift: {merged['pairs_model_b']} | "
               f"testlere giren (her iki kök frekansı >= {MIN_FREQ}): {len(pairs)}"))
    if len(pairs) < 8:
        return findings, {}

    A = [a for a, _ in pairs]
    B = [b for _, b in pairs]

    _cooc_cache = {}

    def cooc(a, b):
        key = (a, b) if a < b else (b, a)
        v = _cooc_cache.get(key)
        if v is None:
            v = _cooc_cache[key] = len(root_ayahs[a] & root_ayahs[b])
        return v

    def lift(a, b):
        return (cooc(a, b) + 0.5) * n_ay / (len(root_ayahs[a]) * len(root_ayahs[b]) + 0.5)

    def mean_loglift(As, Bs):
        return sum(math.log2(lift(a, b)) for a, b in zip(As, Bs)) / len(As)

    def mean_balance(As, Bs):
        return sum(abs(math.log2(freq[a] / freq[b])) for a, b in zip(As, Bs)) / len(As)

    obs_lift = mean_loglift(A, B)
    obs_bal = mean_balance(A, B)
    obs_eq = sum(1 for a, b in zip(A, B) if freq[a] == freq[b])
    hits_l = hits_b = 0
    eq_null = []
    BB = list(B)
    for _ in range(N_PERM):
        rng.shuffle(BB)
        ok = [(a, b) for a, b in zip(A, BB) if a != b]
        As, Bs = [x[0] for x in ok], [x[1] for x in ok]
        hits_l += mean_loglift(As, Bs) >= obs_lift
        hits_b += mean_balance(As, Bs) <= obs_bal
        eq_null.append(sum(1 for a, b in ok if freq[a] == freq[b]))
    # Frekans eşleştirilmiş rastgele kök çiftleri (log-frekans kutuları)
    bins = defaultdict(list)
    for r, f in freq.items():
        if f >= MIN_FREQ:
            bins[int(math.log2(f) * 2)].append(r)
    hits_fm = 0
    n_fm = 2000
    for _ in range(n_fm):
        As = [rng.choice(bins[int(math.log2(freq[a]) * 2)]) for a in A]
        Bs = [rng.choice(bins[int(math.log2(freq[b]) * 2)]) for b in B]
        hits_fm += mean_loglift(As, Bs) >= obs_lift
    co_pairs = sorted(pairs, key=lambda p: -lift(*p))
    findings.append(Finding(
        id="c16_tibaq_cooccurrence", category=CATEGORY, llm_assisted=True,
        title=f"Zıt kavramlar aynı ayette rastlantıdan {2 ** obs_lift:.1f} kat (geometrik ort.) sık birlikte geçiyor (tıbâk)",
        method=f"{len(pairs)} uzlaşılmış zıt çift; ort. log2(lift); null: partnerler yeniden eşlenir ({N_PERM} perm.)",
        metric="ort. log2 lift", value=obs_lift, null_p=(hits_l + 1) / (N_PERM + 1), effect_size=2 ** obs_lift,
        evidence=[f"{glossary.label(a)} ↔ {glossary.label(b)}: {cooc(a, b)} ayet (lift {lift(a, b):.1f})" for a, b in co_pairs[:20]]))
    findings.append(Finding(
        id="c16_tibaq_cooccurrence_freqmatched", category=CATEGORY, llm_assisted=True,
        title="Tıbâk etkisi frekansı eşleştirilmiş rastgele kök çiftlerine karşı da " +
              ("korunuyor" if hits_fm < 0.05 * n_fm else "KORUNMUYOR"),
        method=f"Her kök aynı log-frekans kutusundan rastgele bir kökle değiştirilir ({n_fm} tekrar)",
        metric="ort. log2 lift", value=obs_lift, null_p=(hits_fm + 1) / (n_fm + 1), effect_size=2 ** obs_lift))
    exp_eq = sum(eq_null) / len(eq_null)
    p_eq = (sum(1 for x in eq_null if x >= obs_eq) + 1) / (N_PERM + 1)
    findings.append(Finding(
        id="c16_frequency_balance", category=CATEGORY, llm_assisted=True,
        title=(f"Sistematik simetri testi: zıt çiftler frekans bakımından rastgele eşleşmelerden "
               + ("DAHA DENGELİ" if hits_b < 0.05 * N_PERM else "daha dengeli DEĞİL")
               + f" (ort. |log2 oran| {obs_bal:.2f} vs null)"),
        method=f"Tüm uzlaşılmış çiftler (seçim yok); |log2(fa/fb)|; null: partnerler yeniden eşlenir ({N_PERM} perm.)",
        metric="ort. |log2 oran|", value=obs_bal, null_p=(hits_b + 1) / (N_PERM + 1),
        evidence=[f"{glossary.label(a)} {freq[a]} ↔ {glossary.label(b)} {freq[b]}"
                  for a, b in sorted(pairs, key=lambda p: abs(math.log2(freq[p[0]] / freq[p[1]])))[:20]],
        detail=(f"Tam eşit frekanslı zıt çift: {obs_eq} (yeniden eşleme beklentisi {exp_eq:.2f}, p={p_eq:.4f}). "
                "Bu, projenin önceki tekil 'eşit sayı' iddialarının sistematik ve seçimsiz karşılığıdır.")))

    # Mekkî vs Medenî tıbâk yoğunluğu
    pair_set = [(root_ayahs[a], root_ayahs[b]) for a, b in pairs]
    tib = Counter()
    for sa, sb in pair_set:
        for k in sa & sb:
            tib[k[0]] += 1
    dens = {s: tib[s] / len(corpus.surah_ayahs(s)) for s in range(1, 115)}
    mk = [dens[s] for s in range(1, 115) if corpus.is_meccan(s)]
    md = [dens[s] for s in range(1, 115) if not corpus.is_meccan(s)]
    z = mann_whitney_z(a=md, b=mk)
    findings.append(Finding(
        id="c16_tibaq_period", category=CATEGORY, llm_assisted=True,
        title=f"Ayet başına tıbâk yoğunluğu: Mekkî {sum(mk) / len(mk):.3f}, Medenî {sum(md) / len(md):.3f}",
        method="Sure başına (zıt çift eşbulunması / ayet sayısı), Mann-Whitney U", metric="z (Medenî>Mekkî)",
        value=z, null_p=two_sided_p_from_z(z),
        evidence=[f"{corpus.meta[s]['name_tr']} {dens[s]:.2f}" for s in sorted(dens, key=lambda s: -dens[s])[:10]]))
    bh_adjust([f for f in findings if f.null_p is not None])
    return findings, {'pairs': pairs}


if __name__ == '__main__':
    fs, _ = run()
    for f in fs:
        q = f"{f.q_value:.4f}" if f.q_value is not None else "-"
        print(f"{f.id:36} {f.value:+.3f} q={q} | {f.title} | {f.detail[:200]} | {f.evidence[:6]}")
