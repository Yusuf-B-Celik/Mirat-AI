#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kategori 19: Kıssa (Anlatı) Ağı

Tamamen deterministik: korpustaki özel isim (PN) etiketlerinden.
Yöntemler:
  A. Kıssa epizotları: bir figürün sure içinde <= 5 ayet arayla süren anılış blokları;
     figür başına epizot sayısı ve surelere dağılım (kıssa haritası).
  B. Helak edilen kavimler döngüsü: Nuh → Âd → Semûd → Lût → Medyen → Firavun dizisinin
     sureler içinde ilk anılış sırası, tarihî/kanonik sırayla Kendall tau; rastgele sıralama
     permütasyonu (sure başına bağımsız) ile toplu test.
  C. Figür eşanılma ağı: aynı ayette birlikte anılma; Fisher kesin testi ile en güçlü çiftler (BH-FDR).
  D. Anlatı yoğunluğu ~ nüzul dönemi: kıssa epizotlarında yer alan ayet oranı; erken/orta/geç Mekkî
     ve Medenî dönemler arasında Kruskal-Wallis.
"""

import math
import random
from collections import Counter, defaultdict

from mirat.features import get_corpus
from mirat.discovery.finding import Finding, bh_adjust, rankdata

CATEGORY = "19. Kıssa (Anlatı) Ağı"

FIGURES = {
    'مُوسَى': 'Mûsâ', 'فِرْعَوْن': 'Firavun', 'إِبْراهِيم': 'İbrâhim', 'نُوح': 'Nûh', 'مَرْيَم': 'Meryem',
    'يُوسُف': 'Yûsuf', 'لُوط': 'Lût', 'ثَمُود': 'Semûd', 'آدَم': 'Âdem', 'عِيسَى': 'Îsâ', 'عاد': 'Âd',
    'هارُون': 'Hârûn', 'سُلَيْمان': 'Süleymân', 'إِسْحاق': 'İshâk', 'يَعْقُوب': 'Ya\'kûb', 'داوُد': 'Dâvûd',
    'إِسْماعِيل': 'İsmâil', 'إِبْلِيس': 'İblîs', 'شُعَيْب': 'Şuayb', 'هُود': 'Hûd', 'مَدْيَن': 'Medyen',
    'صالِح': 'Sâlih', 'زَكَرِيّا': 'Zekeriyyâ', 'هامان': 'Hâmân', 'يَحْيَى': 'Yahyâ', 'مُحَمَّد': 'Muhammed',
    'أَيُّوب': 'Eyyûb', 'يُونُس': 'Yûnus', 'قارُون': 'Kârûn', 'جالُوت': 'Câlût', 'طالُوت': 'Tâlût',
    'إِسْرائِيل': 'İsrâil(oğulları)', 'إِلْياس': 'İlyâs', 'إِدْرِيس': 'İdrîs', 'لُقْمان': 'Lokmân',
}
# Helak edilen kavimler döngüsü (kanonik/tarihî sıra); her halka birden fazla isimle temsil edilebilir
CYCLE = [('Nûh', {'نُوح'}), ('Âd', {'عاد', 'هُود'}), ('Semûd', {'ثَمُود', 'صالِح'}), ('Lût', {'لُوط'}),
         ('Medyen', {'مَدْيَن', 'شُعَيْب'}), ('Firavun/Mûsâ', {'فِرْعَوْن', 'مُوسَى'})]
EPISODE_GAP = 5


def kendall_tau(seq):
    """seq: kanonik sıra indekslerinin gözlenen sırası. tau = (uyumlu - uyumsuz) / çift sayısı."""
    n = len(seq)
    c = d = 0
    for i in range(n):
        for j in range(i + 1, n):
            if seq[i] < seq[j]:
                c += 1
            elif seq[i] > seq[j]:
                d += 1
    return (c - d) / (n * (n - 1) / 2) if n > 1 else 0.0


def kruskal_wallis(groups):
    allv = [v for g in groups for v in g]
    r = rankdata(allv)
    n = len(allv)
    h, i = 0.0, 0
    for g in groups:
        rs = sum(r[i:i + len(g)])
        h += rs * rs / len(g)
        i += len(g)
    h = 12 / (n * (n + 1)) * h - 3 * (n + 1)
    df = len(groups) - 1
    # ki-kare sağ kuyruk (df küçük; seri açılımı yerine Wilson-Hilferty yaklaşımı)
    z = ((h / df) ** (1 / 3) - (1 - 2 / (9 * df))) / math.sqrt(2 / (9 * df))
    p = 0.5 * math.erfc(z / math.sqrt(2))
    return h, p


def _fisher_greater(a, b, c, d):
    def lc(n, k):
        return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    r1, c1, n = a + b, a + c, a + b + c + d
    denom = lc(n, c1)
    return min(1.0, sum(math.exp(lc(r1, x) + lc(n - r1, c1 - x) - denom) for x in range(a, min(r1, c1) + 1)))


def run(corpus=None, seed=42):
    corpus = corpus or get_corpus()
    rng = random.Random(seed)
    findings = []
    mentions = defaultdict(list)        # figür -> [(surah, ayah, word)]
    ayah_figs = defaultdict(set)
    for sg in corpus.segments:
        if 'PN' in sg.flags and sg.lemma in FIGURES:
            mentions[sg.lemma].append((sg.surah, sg.ayah, sg.word))
            ayah_figs[(sg.surah, sg.ayah)].add(sg.lemma)

    # ============ A. Epizotlar
    episodes = defaultdict(list)        # figür -> [(surah, start, end, n_mentions)]
    for fig, ms in mentions.items():
        by_s = defaultdict(list)
        for s, a, _ in ms:
            by_s[s].append(a)
        for s, ays in by_s.items():
            ays = sorted(set(ays))
            start = prev = ays[0]
            cnt = 1
            for a in ays[1:]:
                if a - prev <= EPISODE_GAP:
                    cnt += 1
                else:
                    episodes[fig].append((s, start, prev, cnt))
                    start, cnt = a, 1
                prev = a
            episodes[fig].append((s, start, prev, cnt))
    ranked = sorted(episodes, key=lambda f: -len(episodes[f]))
    findings.append(Finding(
        id="c19_episode_map", category=CATEGORY,
        title=f"Kıssa haritası: {len(mentions)} figür, {sum(len(v) for v in episodes.values())} anlatı epizodu; "
              f"en çok epizot {FIGURES[ranked[0]]} ({len(episodes[ranked[0]])} epizot, {len({e[0] for e in episodes[ranked[0]]})} sure)",
        method=f"Özel isim (PN) anılışları; aynı surede <= {EPISODE_GAP} ayet arayla süren anılışlar tek epizot",
        metric="epizot sayısı", value=sum(len(v) for v in episodes.values()), kind="descriptive",
        evidence=[f"{FIGURES[f]}: {len(episodes[f])} epizot / {len({e[0] for e in episodes[f]})} sure / {len(mentions[f])} anılış"
                  for f in ranked[:20]]))
    longest = sorted(((f, e) for f in episodes for e in episodes[f]), key=lambda x: -(x[1][2] - x[1][1]))[:10]
    findings.append(Finding(
        id="c19_longest_episodes", category=CATEGORY,
        title=f"En uzun kesintisiz kıssa: {FIGURES[longest[0][0]]}, {corpus.meta[longest[0][1][0]]['name_tr']} "
              f"{longest[0][1][1]}-{longest[0][1][2]}",
        method="Epizot uzunluğu (ilk ve son anılış arası ayet sayısı)", metric="ayet", kind="descriptive",
        value=longest[0][1][2] - longest[0][1][1] + 1,
        evidence=[f"{FIGURES[f]}: {e[0]}:{e[1]}-{e[2]} ({e[3]} anılış)" for f, e in longest]))

    # ============ B. Helak edilen kavimler döngüsü
    lem2idx = {}
    for i, (_, lems) in enumerate(CYCLE):
        for l in lems:
            lem2idx[l] = i
    first_pos = defaultdict(dict)       # surah -> {cycle_idx: (ayah, word)} — ana epizodun başlangıcı
    cyc_mentions = defaultdict(list)    # (surah, ci) -> [(ayah, word)]
    for fig, ms in mentions.items():
        if fig not in lem2idx:
            continue
        for s, a, w in ms:
            cyc_mentions[(s, lem2idx[fig])].append((a, w))
    for (s, ci), ms in cyc_mentions.items():
        ms.sort()
        blocks, cur = [], [ms[0]]
        for m in ms[1:]:
            if m[0] - cur[-1][0] <= EPISODE_GAP:
                cur.append(m)
            else:
                blocks.append(cur)
                cur = [m]
        blocks.append(cur)
        main = max(blocks, key=lambda b: (len(b), -b[0][0]))
        first_pos[s][ci] = main[0]
    seqs = {}
    for s, d in first_pos.items():
        if len(d) >= 3:
            seqs[s] = [ci for ci, _ in sorted(d.items(), key=lambda x: x[1])]
    taus = {s: kendall_tau(q) for s, q in seqs.items()}
    obs = sum(taus.values()) / len(taus) if taus else 0.0
    hits = 0
    n_perm = 10000
    for _ in range(n_perm):
        tot = 0.0
        for q in seqs.values():
            qq = list(q)
            rng.shuffle(qq)
            tot += kendall_tau(qq)
        hits += tot / len(seqs) >= obs
    perfect = [s for s, t in taus.items() if t == 1.0]
    findings.append(Finding(
        id="c19_punishment_cycle_order", category=CATEGORY,
        title=(f"Helak edilen kavimler {len(seqs)} surede anlatılıyor; anlatım sırası kanonik "
               f"Nûh→Âd→Semûd→Lût→Medyen→Firavun sırasına ort. Kendall τ={obs:.2f} ile uyuyor, "
               f"{len(perfect)} surede birebir"),
        method="Sure içi her halkanın ANA epizodunun (en çok anılan blok) başlangıç sırası; >= 3 halka içeren sureler; sure başına bağımsız "
               "rastgele sıralama, 10000 permütasyon",
        metric="ort. Kendall tau", value=obs, null_p=(hits + 1) / (n_perm + 1), effect_size=obs,
        evidence=[f"{corpus.meta[s]['name_tr']}: {' → '.join(CYCLE[i][0] for i in q)} (τ={taus[s]:.2f})"
                  for s, q in sorted(seqs.items(), key=lambda x: -taus[x[0]])][:20],
        detail=f"Birebir kanonik sırada anlatan sureler: {', '.join(corpus.meta[s]['name_tr'] for s in perfect)}. "
               f"Sırayı bozan sureler: {', '.join(corpus.meta[s]['name_tr'] for s, t in taus.items() if t < 0.5) or 'yok'}"))

    # ============ C. Eşanılma ağı
    n_ay = len(corpus.ayah_keys)
    fig_ayahs = defaultdict(set)
    for k, fs in ayah_figs.items():
        for f in fs:
            fig_ayahs[f].add(k)
    # Sıralı liste: `defaultdict(set)` üzerinden kurulan key sırası hash seed'ine
    # bağlıdır ve aynı veriyle farklı id üretebilir (örn. c19_co_عِيسَى_مَرْيâm).
    # Deterministik kalmak için figürler adlarına göre sabit sıralanır.
    figs = sorted(f for f in fig_ayahs if len(fig_ayahs[f]) >= 4)
    co = []
    for i, a in enumerate(figs):
        for b in figs[i + 1:]:
            both = len(fig_ayahs[a] & fig_ayahs[b])
            if both < 2:
                continue
            na, nb = len(fig_ayahs[a]), len(fig_ayahs[b])
            p = _fisher_greater(both, na - both, nb - both, n_ay - na - nb + both)
            lift = both * n_ay / (na * nb)
            co.append(Finding(
                id=f"c19_co_{a}_{b}", category=CATEGORY,
                title=f"{FIGURES[a]} – {FIGURES[b]}: {both} ayette birlikte (beklenenin {lift:.0f} katı)",
                method="Aynı ayette eşanılma, tek yönlü Fisher, BH-FDR", metric="lift", value=lift, null_p=p,
                effect_size=lift, evidence=[f"{k[0]}:{k[1]}" for k in sorted(fig_ayahs[a] & fig_ayahs[b])[:10]]))
    bh_adjust(co)
    sig = sorted([f for f in co if f.q_value < 0.05], key=lambda f: f.null_p)
    findings.append(Finding(
        id="c19_co_network", category=CATEGORY,
        title=f"Figür eşanılma ağı: {len(figs)} düğüm, {len(sig)} anlamlı bağ (q<0.05)",
        method="Ayet düzeyi eşanılma, Fisher + BH-FDR", metric="anlamlı bağ", value=len(sig), kind="descriptive",
        evidence=[f.title for f in sig[:25]]))
    findings.extend(sig[:12])

    # ============ D. Anlatı yoğunluğu ~ nüzul dönemi
    narr = set()
    for f, eps in episodes.items():
        if f == 'مُحَمَّد':
            continue
        for s, a0, a1, _ in eps:
            for a in range(a0, a1 + 1):
                narr.add((s, a))
    share = {s: sum(1 for k in corpus.surah_ayahs(s) if k in narr) / len(corpus.surah_ayahs(s)) for s in range(1, 115)}
    mk = sorted([s for s in range(1, 115) if corpus.is_meccan(s)], key=corpus.revelation_order)
    t = len(mk) // 3
    groups = {'Erken Mekkî': mk[:t], 'Orta Mekkî': mk[t:2 * t], 'Geç Mekkî': mk[2 * t:],
              'Medenî': [s for s in range(1, 115) if not corpus.is_meccan(s)]}
    h, p = kruskal_wallis([[share[s] for s in g] for g in groups.values()])
    means = {k: sum(share[s] for s in g) / len(g) for k, g in groups.items()}
    peak = max(means, key=means.get)
    findings.append(Finding(
        id="c19_narrative_period", category=CATEGORY,
        title=f"Anlatı (kıssa) yoğunluğu dönemlere göre farklı; zirve: {peak} (%{100 * means[peak]:.0f} ayet)",
        method="Sure başına kıssa epizodu içindeki ayet oranı; nüzul sırasına göre Mekkî üçte birlikler + Medenî; Kruskal-Wallis",
        metric="H", value=h, null_p=p,
        evidence=[f"{k}: %{100 * v:.1f}" for k, v in means.items()],
        detail="Nüzul sırası geleneksel (Mısır/Ezher) listeye dayanır; dönem sınırları eşit sayılı üçte birliklerdir."))

    bh_adjust([f for f in findings if f.null_p is not None and not f.id.startswith('c19_co_')])
    return findings, {'episodes': {FIGURES[f]: v for f, v in episodes.items()}, 'cycle_sequences': seqs}


if __name__ == '__main__':
    fs, _ = run()
    for f in fs:
        q = f"{f.q_value:.4f}" if f.q_value is not None else "-"
        print(f"{f.id:26} {f.value:+.3f} q={q} | {f.title} | {f.detail[:160]} | {f.evidence[:6]}")
