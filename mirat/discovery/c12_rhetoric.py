#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kategori 12: Belâgat Örüntüleri (İltifat, Edilgen Çatı, Açılışlar, Edat İşlevleri)

Yöntemler (tamamı deterministik morfoloji etiketlerine dayanır):
  A. Hitap iltifatı (gaibden muhataba): Allah'tan 3. şahısla söz edilen ayetten hemen sonra
     Allah'a doğrudan 2. şahısla hitap eden ayete geçiş (ör. Fâtiha 1:4 → 1:5).
     İlahî referans kayması (Allah/Rab ↔ "Biz"): ardışık ayetlerde kayma sayısı, sure içi
     ayet sırası karıştırma (1000 permütasyon) null modeline karşı.
  B. Edilgen çatı: ahiret bağlamındaki ayetlerde edilgen fiil oranı vs diğer ayetler
     (ayet etiketi permütasyonu); edilgene yatkın kökler (quasi-binom, BH-FDR).
  C. Sure açılışları: yemin, hurûf-ı mukattaa, nida, hamd/tesbih, soru açılışlarının nüzul
     sırası (Mann-Whitney); mukattaa'yı izleyen ayetlerde "Kitap/indirme" atfı (Fisher kesin testi).
  D. Edat işlevleri profili: hasr (RES), istisna (EXP), şaşırtma (SUR), sakındırma (AVR),
     teşvik (EXH), iptal/istidrak (RET) vb. Mekkî/Medenî sure yoğunluk farkı (Mann-Whitney, BH).
"""

import math
import random
from collections import Counter, defaultdict

from mirat.features import get_corpus
from mirat.discovery.finding import Finding, mann_whitney_z, two_sided_p_from_z, bh_adjust, binom_z
from mirat.discovery import glossary

CATEGORY = "12. Belâgat Örüntüleri (İltifat, Edilgen, Açılış, Edat İşlevleri)"

DIVINE_LEMMAS = {'اللَّه', 'رَبّ', 'رَحْمٰن'}
ESCHATOLOGY_LEMMAS = {'قِيامَة', 'آخِرَة', 'جَهَنَّم', 'جَنَّة', 'نار', 'صُور', 'حِساب', 'جَحِيم', 'سَعِير'}
BOOK_ROOTS = {'كتب', 'نزل', 'قرأ', 'ذكر', 'وحي', 'آيي'}
PARTICLE_FLAGS = {
    'RES': 'Hasr/sınırlama (innemâ vb.)', 'EXP': 'İstisna (illâ)', 'SUR': 'Şaşırtma (izâ el-fucâiyye)',
    'AVR': 'Sakındırma/kınama (kellâ)', 'EXH': 'Teşvik (hallâ, levlâ)', 'RET': 'İstidrak/iptal (bel)',
    'ANS': 'Cevap (neam, belâ)', 'INC': 'Başlangıç (ellâ, emâ)', 'PRP': 'Amaç (li, key)',
    'CAUS': 'Sebep', 'CIRC': 'Hâl vavı', 'RSLT': 'Netice fâsı', 'EQ': 'Denklik', 'INT': 'Tefsir/açıklama',
    'AMD': 'Düzeltme (lâkin)', 'SUP': 'Ek/zâid edat', 'PREV': 'Engelleme', 'FUT': 'Gelecek (se/sevfe)',
    'PRO': 'Yasaklama (lâ nâhiye)', 'CERT': 'Tahkik (kad)', 'EMPH': 'Tekit (le, inne)',
    'INTG': 'Soru', 'NEG': 'Olumsuzluk', 'COND': 'Şart', 'VOC': 'Nida', 'EXL': 'Açıklama/ayrıntı (emmâ)',
}


# ---------------------------------------------------------------- yardımcılar
def _ayah_info(corpus):
    """Her ayet için şahıs/ilahî referans/hitap bilgisi."""
    info = {}
    for key in corpus.ayah_keys:
        segs = corpus.ayah_segments(*key)
        lemmas = {sg.lemma for sg in segs if sg.lemma}
        persons = Counter((sg.person or '') + (sg.number or '') for sg in segs
                          if sg.person and (sg.tag == 'V' or 'PRON' in sg.flags))
        has_divine_name = bool(lemmas & DIVINE_LEMMAS)
        is_speech = any(sg.root == 'قول' and sg.tag == 'V' for sg in segs)
        # Allah'a açık hitap: "iyyâke" (إِيّا + 2MS) ya da "Rabbenâ/Rabbî" + aynı ayette 2MS fiil/zamir
        by_word = defaultdict(list)
        for sg in segs:
            by_word[sg.word].append(sg)
        rabb_voc = any(any(s.lemma == 'رَبّ' for s in w) and any('PRON' in s.flags and s.person == '1' for s in w)
                       for w in by_word.values())
        iyyaka = any(sg.lemma == 'إِيّا' and sg.person == '2' for sg in segs)
        addr_2ms = persons.get('2S', 0) > 0
        god_address = iyyaka or (rabb_voc and addr_2ms)
        divine_we = persons.get('1P', 0) > 0 and any(sg.tag == 'V' and sg.person == '1' and sg.number == 'P'
                                                     for sg in segs) and not is_speech and not god_address
        info[key] = {
            'divine3': has_divine_name and not god_address,
            'god_address': god_address,
            'divine_we': divine_we,
            'persons': persons,
            'verbs': [sg for sg in segs if sg.tag == 'V'],
            'lemmas': lemmas,
            'roots': {sg.root for sg in segs if sg.root},
        }
    return info


def _count_switches(seq):
    """seq: 'G' (Allah 3. şahıs), 'W' (Biz), None. Ardışık G↔W geçiş sayısı."""
    n = 0
    for a, b in zip(seq, seq[1:]):
        if a and b and a != b:
            n += 1
    return n


def _fisher_greater(a, b, c, d):
    """2x2 tablo [[a,b],[c,d]] için tek yönlü (a büyük) Fisher kesin testi."""
    def lc(n, k):
        return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    r1, c1, n = a + b, a + c, a + b + c + d
    denom = lc(n, c1)
    p = 0.0
    for x in range(a, min(r1, c1) + 1):
        p += math.exp(lc(r1, x) + lc(n - r1, c1 - x) - denom)
    return min(1.0, p)


# ---------------------------------------------------------------- motor
def run(corpus=None, seed=42):
    corpus = corpus or get_corpus()
    rng = random.Random(seed)
    info = _ayah_info(corpus)
    findings = []

    # ============ A1. Hitap iltifatı (gaib → muhatap)
    iltifat = []
    for s in range(1, 115):
        keys = corpus.surah_ayahs(s)
        for i in range(1, len(keys)):
            cur = info[keys[i]]
            if not cur['god_address']:
                continue
            prev = [info[k] for k in keys[max(0, i - 3):i]]
            if info[keys[i - 1]]['god_address']:
                continue
            if any(p['divine3'] for p in prev):
                iltifat.append(f"{keys[i - 1][0]}:{keys[i - 1][1]}→{keys[i][0]}:{keys[i][1]}")
    n_addr = sum(1 for v in info.values() if v['god_address'])
    findings.append(Finding(
        id="c12_iltifat_gaib_muhatap", category=CATEGORY,
        title=f"Gaibden muhataba iltifat: {len(iltifat)} geçiş tespit edildi (Allah'tan 3. şahısla söz → doğrudan hitap)",
        method="Önceki 1-3 ayette ilahî isim (Allah/Rab/Rahmân) + bu ayette 'iyyâke' ya da 'Rabbenâ/Rabbî'+2. tekil",
        metric="geçiş sayısı", value=len(iltifat), kind="descriptive", evidence=iltifat[:40],
        detail=f"Allah'a doğrudan hitap içeren toplam ayet: {n_addr}. Kural tabanlı aday listesidir; "
               f"Fâtiha 1:4→1:5 klasik örneği {'yakalandı' if '1:4→1:5' in iltifat else 'YAKALANAMADI'}."))

    # ============ A2. İlahî referans kayması (Allah/O ↔ Biz) — null modele karşı
    def label(k):
        v = info[k]
        if v['divine_we'] and not v['divine3']:
            return 'W'
        if v['divine3'] and not v['divine_we']:
            return 'G'
        return None
    seqs = {s: [label(k) for k in corpus.surah_ayahs(s)] for s in range(1, 115)}
    obs = sum(_count_switches(q) for q in seqs.values())
    within = sum(1 for v in info.values() if v['divine3'] and v['divine_we'])
    null = []
    for _ in range(1000):
        tot = 0
        for q in seqs.values():
            qq = list(q)
            rng.shuffle(qq)
            tot += _count_switches(qq)
        null.append(tot)
    mu = sum(null) / len(null)
    sd = math.sqrt(sum((x - mu) ** 2 for x in null) / (len(null) - 1))
    p_low = (sum(1 for x in null if x <= obs) + 1) / 1001
    p_high = (sum(1 for x in null if x >= obs) + 1) / 1001
    p2 = min(1.0, 2 * min(p_low, p_high))
    switch_examples = []
    for s, q in seqs.items():
        keys = corpus.surah_ayahs(s)
        for i in range(1, len(q)):
            if q[i - 1] and q[i] and q[i - 1] != q[i]:
                switch_examples.append(f"{keys[i - 1][0]}:{keys[i - 1][1]}({q[i - 1]})→{keys[i][1]}({q[i]})")
    findings.append(Finding(
        id="c12_divine_reference_shift", category=CATEGORY,
        title=(f"İlahî referans 'Allah/O' ↔ 'Biz' arasında ardışık ayetlerde {obs} kez kayıyor; "
               f"rastgele sıralamada beklenen {mu:.0f} — "
               + ("kayma rastlantıdan SIK (aktif iltifat)" if obs > mu else "kayma rastlantıdan SEYREK (referans kümeleniyor)")),
        method="Ayet etiketleri G (ilahî isim, 'Biz' yok) / W ('Biz' fiili, söz aktarımı yok); sure içi karıştırma, 1000 permütasyon",
        metric="z (gözlenen-null)", value=(obs - mu) / sd if sd else 0.0, null_p=p2, effect_size=obs / mu if mu else None,
        evidence=switch_examples[:25],
        detail=f"Gözlenen {obs} | null ort. {mu:.1f} ± {sd:.1f} | aynı ayet içinde hem ilahî isim hem 'Biz': {within} ayet. "
               f"'Biz' etiketi sezgiseldir (insan konuşması kısmen 'qâle' filtresiyle ayıklanır)."))

    # ============ B1. Ahiret bağlamında edilgen çatı
    keys_all = corpus.ayah_keys
    esch = [k for k in keys_all if info[k]['lemmas'] & ESCHATOLOGY_LEMMAS]
    esch_set = set(esch)

    def pass_rate(keyset):
        v = [vb for k in keyset for vb in info[k]['verbs']]
        return sum(1 for x in v if x.voice == 'PASS') / max(1, len(v)), len(v)
    r_e, n_e = pass_rate(esch)
    r_o, n_o = pass_rate([k for k in keys_all if k not in esch_set])
    diff_obs = r_e - r_o
    # Ayet etiketi permütasyonu (sure içinde, bağlam yoğunluğunu korur)
    by_surah = defaultdict(list)
    for k in keys_all:
        by_surah[k[0]].append(k)
    hits = 0
    n_perm = 1000
    for _ in range(n_perm):
        perm_e = []
        for s, ks in by_surah.items():
            m = sum(1 for k in ks if k in esch_set)
            if m:
                perm_e.extend(rng.sample(ks, m))
        pe = set(perm_e)
        a, _ = pass_rate(perm_e)
        b, _ = pass_rate([k for k in keys_all if k not in pe])
        if a - b >= diff_obs:
            hits += 1
    ex = [f"{k[0]}:{k[1]}" for k in esch if any(v.voice == 'PASS' for v in info[k]['verbs'])][:20]
    findings.append(Finding(
        id="c12_passive_eschatology", category=CATEGORY,
        title=f"Ahiret sahnelerinde edilgen çatı {r_e / r_o:.2f} kat daha sık (fail gizlenir: 'sûra üfürülür', 'defterler açılır')",
        method="Ahiret sözcüklü ayetler (kıyamet, ahiret, cehennem, cennet, ateş, sûr, hesap...) vs diğerleri; sure içi etiket permütasyonu (1000)",
        metric="edilgen oranı farkı", value=diff_obs, null_p=(hits + 1) / (n_perm + 1), effect_size=r_e / r_o if r_o else None,
        evidence=ex, detail=f"Ahiret ayetleri: {len(esch)} ayet, {n_e} fiil, edilgen %{100 * r_e:.1f} | Diğer: {n_o} fiil, %{100 * r_o:.1f}"))

    # ============ B2. Edilgene yatkın kökler
    root_v = defaultdict(lambda: [0, 0])
    for sg in corpus.segments:
        if sg.tag == 'V' and sg.root:
            root_v[sg.root][0] += 1
            root_v[sg.root][1] += sg.voice == 'PASS'
    tot_v = sum(v[0] for v in root_v.values())
    base = sum(v[1] for v in root_v.values()) / tot_v
    raw = [(r, n, k, binom_z(k, n, base)) for r, (n, k) in root_v.items() if n >= 20]
    z2 = sorted(x[3] ** 2 for x in raw)
    phi = max(1.0, z2[len(z2) // 2] / 0.4549)
    rf = []
    for r, n, k, z in raw:
        za = z / math.sqrt(phi)
        rf.append(Finding(id=f"c12_passroot_{r}", category=CATEGORY,
                          title=f"Kök {glossary.label(r)}: fiilleri %{100 * k / n:.0f} edilgen (genel %{100 * base:.1f})",
                          method=f"Kök bazında edilgen payı, binom z / sqrt(phi={phi:.2f}), BH-FDR",
                          metric="düzeltilmiş z", value=za, null_p=two_sided_p_from_z(za), effect_size=k / n / base,
                          detail=f"{k}/{n} edilgen"))
    bh_adjust(rf)
    sig = sorted([f for f in rf if f.q_value < 0.05 and f.value > 0], key=lambda f: -f.value)
    findings.extend(sig[:15])
    findings.append(Finding(
        id="c12_passroot_summary", category=CATEGORY,
        title=f"{len(rf)} fiil kökünün {len(sig)} tanesi anlamlı biçimde edilgene yatkın (q<0.05)",
        method="Kök bazında edilgen taraması özeti", metric="anlamlı kök", value=len(sig), kind="descriptive",
        evidence=[f"{glossary.label(f.id[len('c12_passroot_'):])} ({f.detail})" for f in sig[:15]]))

    # ============ C. Sure açılışları
    def opening_type(s):
        segs = corpus.ayah_segments(s, 1)
        w1 = [sg for sg in segs if sg.word == 1]
        w12 = [sg for sg in segs if sg.word <= 2]
        if any('INL' in sg.flags for sg in w1):
            return 'Hurûf-ı mukattaa'
        if any(sg.lemma == 'و' and 'P' in sg.flags for sg in w1) or any(sg.lemma == 'أَقْسَمُ' for sg in w12):
            return 'Yemin'
        if any('VOC' in sg.flags for sg in w1):
            return 'Nida (Ey ...)'
        if any(sg.root in ('حمد', 'سبح', 'برك') for sg in w12):
            return 'Hamd/Tesbih'
        if any('INTG' in sg.flags for sg in w1):
            return 'Soru'
        if any(sg.tag == 'V' and sg.aspect == 'IMPV' for sg in w1):
            return 'Emir (Kul/İkra)'
        return 'Diğer'
    otype = {s: opening_type(s) for s in range(1, 115)}
    counts = Counter(otype.values())
    open_tests = []
    for t, c in counts.items():
        if t == 'Diğer' or c < 3:
            continue
        a = [corpus.revelation_order(s) for s in range(1, 115) if otype[s] == t]
        b = [corpus.revelation_order(s) for s in range(1, 115) if otype[s] != t]
        z = mann_whitney_z(a=a, b=b)
        mk = sum(1 for s in range(1, 115) if otype[s] == t and corpus.is_meccan(s))
        open_tests.append(Finding(
            id=f"c12_open_{t}", category=CATEGORY,
            title=f"'{t}' açılışlı {c} sure: ort. nüzul sırası {sum(a) / len(a):.0f} (diğerleri {sum(b) / len(b):.0f}), {mk}/{c} Mekkî",
            method="Sure açılış türü vs nüzul sırası, Mann-Whitney U", metric="z", value=z,
            null_p=two_sided_p_from_z(z), evidence=[corpus.meta[s]['name_tr'] for s in range(1, 115) if otype[s] == t][:30]))
    findings.extend(open_tests)

    # Mukattaa'yı izleyen ayetlerde Kitap/vahiy atfı (ilk 2 ayet) vs diğer surelerin ilk 2 ayeti
    def book_ref(s):
        keys = corpus.surah_ayahs(s)
        span = keys[:3] if otype[s] == 'Hurûf-ı mukattaa' else keys[:2]
        return any(info[k]['roots'] & BOOK_ROOTS for k in span)
    inl = [s for s in range(1, 115) if otype[s] == 'Hurûf-ı mukattaa']
    oth = [s for s in range(1, 115) if otype[s] != 'Hurûf-ı mukattaa']
    a = sum(book_ref(s) for s in inl)
    c_ = sum(book_ref(s) for s in oth)
    p_f = _fisher_greater(a, len(inl) - a, c_, len(oth) - c_)
    findings.append(Finding(
        id="c12_muqattaa_book", category=CATEGORY,
        title=f"Hurûf-ı mukattaa ile açılan {len(inl)} surenin {a}'ü hemen ardından Kitap/vahye atıf yapıyor (diğer surelerde {c_}/{len(oth)})",
        method="Mukattaa sonrası ilk 2 ayet vs diğer surelerin ilk 2 ayeti; kökler: كتب نزل قرأ ذكر وحي آيي; tek yönlü Fisher",
        metric="oran farkı", value=a / len(inl) - c_ / len(oth), null_p=p_f, effect_size=(a / len(inl)) / max(1e-9, c_ / len(oth)),
        evidence=[corpus.meta[s]['name_tr'] for s in inl if not book_ref(s)],
        detail="Kanıt listesi: atıf YAPMAYAN mukattaa sureleri (istisnalar)."))

    # ============ D. Edat işlevleri: Mekkî vs Medenî
    surah_words = {s: sum(corpus.ayah_word_count(*k) for k in corpus.surah_ayahs(s)) for s in range(1, 115)}
    flag_counts = defaultdict(Counter)
    for sg in corpus.segments:
        for f in sg.flags:
            if f in PARTICLE_FLAGS:
                flag_counts[sg.surah][f] += 1
    part = []
    for f, name in PARTICLE_FLAGS.items():
        dens = {s: 1000 * flag_counts[s][f] / surah_words[s] for s in range(1, 115)}
        total = sum(flag_counts[s][f] for s in range(1, 115))
        if total < 20:
            continue
        mk = [dens[s] for s in range(1, 115) if corpus.is_meccan(s)]
        md = [dens[s] for s in range(1, 115) if not corpus.is_meccan(s)]
        z = mann_whitney_z(a=md, b=mk)
        tok_mk = sum(flag_counts[s][f] for s in range(1, 115) if corpus.is_meccan(s))
        w_mk = sum(surah_words[s] for s in range(1, 115) if corpus.is_meccan(s))
        tok_md, w_md = total - tok_mk, sum(surah_words.values()) - w_mk
        ratio = (tok_md / w_md) / (tok_mk / w_mk) if tok_mk else float('inf')
        part.append(Finding(
            id=f"c12_particle_{f}", category=CATEGORY,
            title=f"{name}: Medenî/Mekkî yoğunluk oranı {ratio:.2f}x",
            method="Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U",
            metric="z (Medenî>Mekkî)", value=z, null_p=two_sided_p_from_z(z), effect_size=ratio,
            detail=f"Toplam {total} | Mekkî {1000 * tok_mk / w_mk:.2f}‰ | Medenî {1000 * tok_md / w_md:.2f}‰"))
    findings.extend(part)

    bh_adjust([f for f in findings if not f.id.startswith('c12_passroot_') or f.id == 'c12_passroot_summary'])
    return findings, {'iltifat': iltifat, 'opening_types': otype}


if __name__ == '__main__':
    fs, ex = run()
    for f in fs:
        q = f"{f.q_value:.4f}" if f.q_value is not None else "-"
        print(f"{f.id:28} {f.value:+.3f} q={q} | {f.title} | {f.detail[:120]}")
