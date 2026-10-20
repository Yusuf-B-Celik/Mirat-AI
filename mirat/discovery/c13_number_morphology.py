#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kategori 13: Sayı Morfolojisi (Tekil / İkil / Çoğul) ve Fiil Babları

Yöntemler:
  A. Lemma sayı tercihi: >= 30 tokenlı her isim lemmasının S/D/P dağılımı; hiç çoğul
     kullanılmayan ve çoğulu baskın lemmalar (betimsel).
  B. Tekil-çoğul asimetrik eşdizimli çiftler: aynı ayette >= 5 kez birlikte geçen, biri
     >= %90 tekil, diğeri >= %60 çoğul lemma çiftleri (ör. سَمْع tekil — قَلْب/بَصَر çoğul).
     Ortak ayetlerdeki sayı dağılımı farkı Fisher kesin testiyle.
  C. İkil (dual) envanteri: tüm ikil isimler, ikil yoğunluğu en yüksek sureler ve
     ikil hitap (2D) yoğunlaşması.
  D. Fiil babları (VF:1-12): her babın Mekkî/Medenî sure yoğunluğu (Mann-Whitney, BH).
"""

import math
from collections import Counter, defaultdict

from mirat.features import get_corpus
from mirat.discovery.finding import Finding, mann_whitney_z, two_sided_p_from_z, bh_adjust

CATEGORY = "13. Sayı Morfolojisi (Tekil-İkil-Çoğul) ve Fiil Babları"
EXCLUDE = {'PRON', 'PN', 'DEM', 'REL', 'ADJ'}
VF_NAMES = {'1': 'I (fe\'ale)', '2': 'II (tef\'îl)', '3': 'III (müfâale)', '4': 'IV (if\'âl)', '5': 'V (tefa\'\'ul)',
            '6': 'VI (tefâ\'ul)', '7': 'VII (infi\'âl)', '8': 'VIII (ifti\'âl)', '9': 'IX (if\'ilâl)',
            '10': 'X (istif\'âl)', '11': 'XI', '12': 'XII'}


def _fisher_two_sided(a, b, c, d):
    def lc(n, k):
        return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    r1, c1, n = a + b, a + c, a + b + c + d
    denom = lc(n, c1)

    def pr(x):
        return math.exp(lc(r1, x) + lc(n - r1, c1 - x) - denom)
    p_obs = pr(a)
    lo, hi = max(0, c1 - (n - r1)), min(r1, c1)
    return min(1.0, sum(pr(x) for x in range(lo, hi + 1) if pr(x) <= p_obs * (1 + 1e-9)))


def noun_number(sg):
    if sg.tag != 'N' or not sg.lemma or (EXCLUDE & sg.flags):
        return None
    if sg.number:
        return sg.number
    return 'S' if sg.gender else None


def run(corpus=None, seed=42):
    corpus = corpus or get_corpus()
    findings = []

    # ============ A. Lemma sayı tercihi
    dist = defaultdict(Counter)
    ayahs_of = defaultdict(set)
    num_in_ayah = defaultdict(Counter)   # (lemma, ayah) -> number counts
    for sg in corpus.segments:
        nb = noun_number(sg)
        if nb:
            dist[sg.lemma][nb] += 1
            ayahs_of[sg.lemma].add((sg.surah, sg.ayah))
            num_in_ayah[(sg.lemma, (sg.surah, sg.ayah))][nb] += 1
    tot = Counter()
    for c in dist.values():
        tot.update(c)
    n_all = sum(tot.values())
    freq = {l: sum(c.values()) for l, c in dist.items()}
    big = [l for l in dist if freq[l] >= 30]
    sing_only = sorted([l for l in big if dist[l]['P'] == 0 and dist[l]['D'] == 0], key=lambda l: -freq[l])
    plural_dom = sorted([l for l in big if dist[l]['P'] / freq[l] >= 0.6], key=lambda l: -dist[l]['P'] / freq[l])
    findings.append(Finding(
        id="c13_singular_only", category=CATEGORY,
        title=f"{len(big)} sık isim lemmasının {len(sing_only)} tanesi Kur'an'da hiç çoğul/ikil kullanılmıyor",
        method="İsim lemmaları (>= 30 token), sayı etiketi; sayısız eril/dişil etiket tekil sayılır",
        metric="yalnız tekil lemma", value=len(sing_only), kind="descriptive",
        evidence=[f"{l} ({freq[l]})" for l in sing_only[:30]],
        detail=f"Genel dağılım: tekil %{100 * tot['S'] / n_all:.1f}, ikil %{100 * tot['D'] / n_all:.1f}, çoğul %{100 * tot['P'] / n_all:.1f}. "
               f"Not: kırık çoğulların bir kısmı korpus tarafından ayrı lemma olarak kaydedilmiş olabilir."))
    findings.append(Finding(
        id="c13_plural_dominant", category=CATEGORY,
        title=f"{len(plural_dom)} sık isim lemması ağırlıkla (>= %60) çoğul kullanılıyor",
        method="İsim lemmaları (>= 30 token), çoğul payı", metric="çoğul baskın lemma", value=len(plural_dom),
        kind="descriptive",
        evidence=[f"{l} (%{100 * dist[l]['P'] / freq[l]:.0f} çoğul, n={freq[l]})" for l in plural_dom[:30]]))

    # ============ B. Eşdizim etkisi: bir lemmanın varlığı diğerinin tekil/çoğul seçimini değiştiriyor mu?
    # (Döngüsel olmayan tasarım: b'nin ortak ayetlerdeki çoğul oranı, b'nin DİĞER ayetlerdeki oranıyla
    #  karşılaştırılır; b'nin genel tercihi testin konusu değildir.)
    variable = [l for l in dist if freq[l] >= 20 and 0.15 <= (dist[l]['P'] + dist[l]['D']) / freq[l] <= 0.85]
    partners = [l for l in dist if freq[l] >= 15]
    pair_tests = []
    for b in variable:
        for a in partners:
            if a == b:
                continue
            shared = ayahs_of[a] & ayahs_of[b]
            if len(shared) < 8:
                continue
            sb_in = sum(num_in_ayah[(b, k)]['S'] for k in shared)
            pb_in = sum(num_in_ayah[(b, k)]['P'] + num_in_ayah[(b, k)]['D'] for k in shared)
            sb_out = dist[b]['S'] - sb_in
            pb_out = dist[b]['P'] + dist[b]['D'] - pb_in
            p = _fisher_two_sided(pb_in, sb_in, pb_out, sb_out)
            r_in = pb_in / max(1, pb_in + sb_in)
            r_out = pb_out / max(1, pb_out + sb_out)
            pair_tests.append(Finding(
                id=f"c13_pair_{a}_{b}", category=CATEGORY,
                title=f"'{b}' yanında '{a}' varken %{100 * r_in:.0f} çoğul, yokken %{100 * r_out:.0f} çoğul",
                method="b'nin ortak ayetlerdeki vs diğer ayetlerdeki tekil/çoğul sayımı; iki yönlü Fisher, BH-FDR",
                metric="çoğul oranı farkı", value=r_in - r_out, null_p=p, effect_size=r_in - r_out,
                evidence=[f"{k[0]}:{k[1]}" for k in sorted(shared)[:12]],
                detail=f"Ortak {len(shared)} ayet | '{b}' ortak: {pb_in} çoğul/{sb_in} tekil | diğer: {pb_out} çoğul/{sb_out} tekil | "
                       f"'{a}' çoğul payı genel %{100 * (dist[a]['P'] + dist[a]['D']) / freq[a]:.0f}"))
    bh_adjust(pair_tests)
    sig = sorted([f for f in pair_tests if f.q_value < 0.05], key=lambda f: f.null_p)
    findings.extend(sig[:15])
    findings.append(Finding(
        id="c13_pair_summary", category=CATEGORY,
        title=f"{len(pair_tests)} eşdizim çiftinin {len(sig)} tanesinde ortak lemma tekil/çoğul seçimini anlamlı değiştiriyor (q<0.05)",
        method="Eşdizim-sayı etkisi taraması özeti", metric="anlamlı çift", value=len(sig), kind="descriptive",
        evidence=[f.title for f in sig[:20]]))

    # ============ C. İkil envanteri
    dual_l = Counter()
    dual_ev = defaultdict(list)
    dual_by_surah = Counter()
    addr_2d = Counter()
    for sg in corpus.segments:
        if noun_number(sg) == 'D':
            dual_l[sg.lemma] += 1
            dual_ev[sg.lemma].append(f"{sg.surah}:{sg.ayah}")
        if sg.number == 'D':
            dual_by_surah[sg.surah] += 1
        if sg.person == '2' and sg.number == 'D':
            addr_2d[sg.surah] += 1
    findings.append(Finding(
        id="c13_dual_inventory", category=CATEGORY,
        title=f"İkil envanteri: {len(dual_l)} farklı isim lemması ikil biçimde, toplam {sum(dual_l.values())} kez",
        method="İsim segmentlerinde sayı etiketi D", metric="ikil lemma", value=len(dual_l), kind="descriptive",
        evidence=[f"{l} ×{c} ({', '.join(dual_ev[l][:3])})" for l, c in dual_l.most_common(25)]))
    words = {s: sum(corpus.ayah_word_count(*k) for k in corpus.surah_ayahs(s)) for s in range(1, 115)}
    dens = {s: 1000 * dual_by_surah[s] / words[s] for s in range(1, 115)}
    top = sorted(dens, key=lambda s: -dens[s])[:10]
    mean_d = sum(dual_by_surah.values()) / sum(words.values()) * 1000
    findings.append(Finding(
        id="c13_dual_surahs", category=CATEGORY,
        title=(f"İkil yoğunluğu en yüksek sure {corpus.meta[top[0]]['name_tr']} ({dens[top[0]]:.0f}‰, genel {mean_d:.1f}‰); "
               f"2. şahıs ikil hitabın %{100 * addr_2d[55] / max(1, sum(addr_2d.values())):.0f}'i Rahmân suresinde"),
        method="Tüm ikil segmentler (isim, fiil, zamir) / sure kelime sayısı", metric="‰ kelime", value=dens[top[0]],
        kind="descriptive", evidence=[f"{corpus.meta[s]['name_tr']} {dens[s]:.1f}‰" for s in top],
        detail="Rahmân suresinin ikil hitabı (insan ve cin: 'ikiniz') klasik tefsirde bilinir; burada tüm sureler "
               "arasında nicel sıralaması verilir."))

    # ============ D. Fiil babları Mekkî vs Medenî
    vf = defaultdict(Counter)
    nverbs = Counter()
    for sg in corpus.segments:
        if sg.tag == 'V':
            nverbs[sg.surah] += 1
            if sg.verb_form:
                vf[sg.surah][sg.verb_form] += 1
    vf_tests = []
    for form, name in VF_NAMES.items():
        total = sum(vf[s][form] for s in range(1, 115))
        if total < 30:
            continue
        d = {s: 1000 * vf[s][form] / max(1, nverbs[s]) for s in range(1, 115)}
        mk = [d[s] for s in range(1, 115) if corpus.is_meccan(s)]
        md = [d[s] for s in range(1, 115) if not corpus.is_meccan(s)]
        z = mann_whitney_z(a=md, b=mk)
        tmk = sum(vf[s][form] for s in range(1, 115) if corpus.is_meccan(s))
        vmk = sum(nverbs[s] for s in range(1, 115) if corpus.is_meccan(s))
        tmd, vmd = total - tmk, sum(nverbs.values()) - vmk
        ratio = (tmd / vmd) / (tmk / vmk) if tmk else float('inf')
        vf_tests.append(Finding(
            id=f"c13_vf_{form}", category=CATEGORY,
            title=f"Fiil babı {name}: Medenî/Mekkî oranı {ratio:.2f}x",
            method="Sure bazında ‰ fiil yoğunluğu, Mann-Whitney U (Medenî > Mekkî pozitif)", metric="z", value=z,
            null_p=two_sided_p_from_z(z), effect_size=ratio,
            detail=f"Toplam {total} | Mekkî {1000 * tmk / vmk:.1f}‰ | Medenî {1000 * tmd / vmd:.1f}‰"))
    findings.extend(vf_tests)
    bh_adjust([f for f in findings if f.id.startswith('c13_vf_')])
    return findings, {'dual_inventory': dict(dual_l), 'singular_only': sing_only}


if __name__ == '__main__':
    fs, ex = run()
    for f in fs:
        q = f"{f.q_value:.4f}" if f.q_value is not None else "-"
        print(f"{f.id:30} {f.value:+.3f} q={q} | {f.title} | {f.detail[:150]} | {f.evidence[:8]}")
