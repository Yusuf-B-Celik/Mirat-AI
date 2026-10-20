#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
MİRAT Matematiksel ve İstatistiksel Analiz Motoru
Ki-Kare (\chi^2), Z-Skoru, Co-occurrence, Linearity ve Monte Carlo testlerini içerir.
r"""

import math
import random

def norm_cdf(x):
    r"""Standart normal dağılım kümülatif yoğunluk fonksiyonu (CDF)."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))

def norm_p_value(z):
    r"""İki yönlü (two-tailed) Z-testi p-değeri."""
    return 2.0 * (1.0 - norm_cdf(abs(z)))

def gamma_inc_lower(s, x):
    r"""Tamamlanmamış alt Gamma fonksiyonu (Incomplete lower gamma) serisi."""
    if x < 0.0:
        return 0.0
    if x == 0.0:
        return 0.0
    sum_val = 1.0 / s
    term = 1.0 / s
    for k in range(1, 200):
        term = term * x / (s + k)
        sum_val += term
        if abs(term) < 1e-12:
            break
    return sum_val * math.pow(x, s) * math.exp(-x)

def chi2_cdf(chi2_val, df):
    r"""Ki-Kare Kümülatif Dağılım Fonksiyonu (CDF)."""
    if chi2_val <= 0 or df <= 0:
        return 0.0
    k = df / 2.0
    x = chi2_val / 2.0
    try:
        gamma_total = math.gamma(k)
        lower_gamma = gamma_inc_lower(k, x)
        return min(1.0, max(0.0, lower_gamma / gamma_total))
    except OverflowError:
        return 1.0

def chi2_p_value(chi2_val, df):
    r"""Ki-Kare sağ kuyruk (upper tail) p-değeri (uygunluk testi p-değeri)."""
    return max(0.0, min(1.0, 1.0 - chi2_cdf(chi2_val, df)))

def chi_square_goodness_of_fit(observed, expected_props):
    r"""
    Ki-Kare (\chi^2) Uygunluk Testi
    observed: [O1, O2, ...] (Gözlemlenen frekanslar)
    expected_props: [P1, P2, ...] (Beklenen teorik oranlar, toplamı 1.0 olmalı)
    r"""
    total_n = sum(observed)
    expected = [total_n * p for p in expected_props]
    
    chi2 = 0.0
    details = []
    for o, e, p in zip(observed, expected, expected_props):
        component = ((o - e) ** 2) / e if e > 0 else 0
        chi2 += component
        details.append({
            'observed': o,
            'expected': e,
            'prop_expected': p,
            'prop_observed': o / total_n if total_n > 0 else 0,
            'chi2_component': component
        })
        
    df = len(observed) - 1
    p_val = chi2_p_value(chi2, df)
    
    return {
        'total_n': total_n,
        'chi2': chi2,
        'df': df,
        'p_value': p_val,
        'is_significant_at_05': p_val < 0.05,
        'details': details
    }

def z_test_equal_frequencies(count1, count2):
    r"""
    İki frekansın eşitliği için Binom / Z-Skoru Eşitlik Testi (H0: p1 = p2 = 0.5)
    r"""
    total = count1 + count2
    if total == 0:
        return {'z': 0.0, 'p_value': 1.0, 'ratio': 0.5, 'ci_95': (0.0, 0.0)}
        
    p_hat = count1 / total
    p0 = 0.5
    se0 = math.sqrt(p0 * (1 - p0) / total)
    z = (p_hat - p0) / se0
    p_val = norm_p_value(z)
    
    # 95% Güven aralığı
    se_sample = math.sqrt(p_hat * (1 - p_hat) / total) if total > 0 else 0
    ci_low = max(0.0, p_hat - 1.96 * se_sample)
    ci_high = min(1.0, p_hat + 1.96 * se_sample)
    
    return {
        'count1': count1,
        'count2': count2,
        'total': total,
        'p_observed': p_hat,
        'z_score': z,
        'p_value': p_val,
        'is_symmetric': p_val >= 0.05,
        'ci_95': (ci_low, ci_high)
    }

def co_occurrence_metrics(ayah_set_a, ayah_set_b, total_ayahs=6236):
    r"""
    İki kavramın ayet düzeyinde birlikte görünme (Co-occurrence) metrikleri.
    ayah_set_a: Birinci kavramın geçtiği ayetler kümesi {(surah, ayah), ...}
    ayah_set_b: İkinci kavramın geçtiği ayetler kümesi
    r"""
    set_a = set(ayah_set_a)
    set_b = set(ayah_set_b)
    
    both = set_a.intersection(set_b)
    n_a = len(set_a)
    n_b = len(set_b)
    n_both = len(both)
    
    # Jaccard katsayısı
    union_len = len(set_a.union(set_b))
    jaccard = n_both / union_len if union_len > 0 else 0.0
    
    # Pointwise Mutual Information (PMI)
    p_a = n_a / total_ayahs if total_ayahs > 0 else 0.0001
    p_b = n_b / total_ayahs if total_ayahs > 0 else 0.0001
    p_both = n_both / total_ayahs
    
    pmi = math.log2(p_both / (p_a * p_b)) if p_both > 0 else 0.0
    
    # Odds Ratio
    n11 = n_both
    n10 = n_a - n_both
    n01 = n_b - n_both
    n00 = total_ayahs - (n_a + n_b - n_both)
    
    odds_ratio = ((n11 * n00) / (n10 * n01)) if (n10 * n01) > 0 else float('inf')
    
    return {
        'count_a': n_a,
        'count_b': n_b,
        'count_both': n_both,
        'co_occurring_ayahs': sorted(list(both)),
        'jaccard_similarity': jaccard,
        'pmi': pmi,
        'odds_ratio': odds_ratio
    }

def linearity_rank_test(observed_orders, ideal_order):
    r"""
    Doğrusallık / Sıralı Kronoloji Testi (Linearity Test)
    observed_orders: Ayetlerde geçen sıralamalar listesi (örn: [['nutfe', 'alaka', 'mudga'], ...])
    ideal_order: Hedeflenen kronolojik sıra (örn: ['nutfe', 'alaka', 'mudga', 'kemik', 'et'])
    r"""
    order_map = {item: i for i, item in enumerate(ideal_order)}
    
    concordant = 0
    discordant = 0
    ties = 0
    total_pairs = 0
    
    perfect_matches = 0
    
    for seq in observed_orders:
        ranks = [order_map[item] for item in seq if item in order_map]
        if len(ranks) >= 2:
            # Check if strictly increasing
            if ranks == sorted(ranks) and len(ranks) == len(set(ranks)):
                perfect_matches += 1
            for i in range(len(ranks)):
                for j in range(i + 1, len(ranks)):
                    total_pairs += 1
                    if ranks[i] < ranks[j]:
                        concordant += 1
                    elif ranks[i] > ranks[j]:
                        discordant += 1
                    else:
                        ties += 1
                        
    tau = (concordant - discordant) / total_pairs if total_pairs > 0 else 1.0
    
    return {
        'total_sequences': len(observed_orders),
        'perfect_chronological_matches': perfect_matches,
        'concordant_pairs': concordant,
        'discordant_pairs': discordant,
        'kendall_tau': tau,
        'is_perfectly_linear': discordant == 0 and total_pairs > 0
    }

def benjamini_hochberg(p_values, fdr_level=0.05):
    r"""
    Benjamini-Hochberg (BH) Çoklu Hipotez Düzeltmesi (False Discovery Rate - FDR).
    p_values: [p1, p2, ...] veya {'id1': p1, 'id2': p2, ...}
    Dönen: q-değerleri ve anlamlılık bayrakları.
    """
    is_dict = isinstance(p_values, dict)
    if is_dict:
        keys = list(p_values.keys())
        raw_p = [float(p_values[k]) for k in keys]
    else:
        keys = list(range(len(p_values)))
        raw_p = [float(p) for p in p_values]

    m = len(raw_p)
    if m == 0:
        return {} if is_dict else []

    # p-değerlerini küçükten büyüğe sırala
    sorted_indices = sorted(range(m), key=lambda i: raw_p[i])
    
    # Adım adım q-değeri hesapla: q_(i) = min_{k >= i} (m / k * p_(k))
    q_values = [0.0] * m
    min_so_far = 1.0
    for rank in range(m, 0, -1):
        idx = sorted_indices[rank - 1]
        p_val = raw_p[idx]
        q_raw = (m / rank) * p_val
        min_so_far = min(min_so_far, q_raw)
        q_values[idx] = min(1.0, max(0.0, min_so_far))

    results = []
    for i in range(m):
        res_item = {
            'id': keys[i],
            'raw_p': raw_p[i],
            'q_value': round(q_values[i], 6),
            'is_significant_fdr': q_values[i] <= fdr_level
        }
        results.append(res_item)

    if is_dict:
        return {r['id']: r for r in results}
    return results

def equivalence_test_tost(count1, count2, margin=0.05, alpha=0.05):
    r"""
    Two One-Sided Tests (TOST) Biyoistatistiksel Denklik Testi.
    H0: |p - 0.5| >= margin (Frekanslar denk değil)
    H1: |p - 0.5| < margin  (Frekanslar margin aralığında denk)
    c1, c2: İki kavramın gözlenen frekansları.
    margin: İzin verilen denklik marjı (varsayılan ±%5 sapma = 0.05).
    """
    total = count1 + count2
    if total == 0:
        return {
            'is_equivalent': False,
            'p_tost': 1.0,
            'p1': 1.0,
            'p2': 1.0,
            'p_hat': 0.5,
            'margin': margin,
            'confidence_interval_90': (0.0, 0.0)
        }

    p_hat = count1 / total
    # Standart hata
    se = math.sqrt(p_hat * (1.0 - p_hat) / total) if 0.0 < p_hat < 1.0 else math.sqrt(0.25 / total)
    if se == 0:
        se = 1e-9

    # Alt sınır testi: H01: p <= 0.5 - margin vs H11: p > 0.5 - margin
    bound_lower = 0.5 - margin
    z1 = (p_hat - bound_lower) / se
    p1 = 1.0 - norm_cdf(z1)

    # Üst sınır testi: H02: p >= 0.5 + margin vs H12: p < 0.5 + margin
    bound_upper = 0.5 + margin
    z2 = (p_hat - bound_upper) / se
    p2 = norm_cdf(z2)

    p_tost = max(p1, p2)
    is_equivalent = (p_tost < alpha)

    # %90 Güven Aralığı (TOST alpha=0.05 için 1 - 2*alpha = %90 CI)
    z_crit_90 = 1.6448536269514722
    ci_low = max(0.0, p_hat - z_crit_90 * se)
    ci_high = min(1.0, p_hat + z_crit_90 * se)

    return {
        'count1': count1,
        'count2': count2,
        'total': total,
        'p_hat': round(p_hat, 4),
        'margin': margin,
        'bound_lower': bound_lower,
        'bound_upper': bound_upper,
        'z1': round(z1, 4),
        'p1': round(p1, 6),
        'z2': round(z2, 4),
        'p2': round(p2, 6),
        'p_tost': round(p_tost, 6),
        'alpha': alpha,
        'is_equivalent': is_equivalent,
        'ci_90': (round(ci_low, 4), round(ci_high, 4))
    }

def bayes_factor_binomial(count1, count2, p0=0.5):
    r"""
    Noktasal Eşitlik Hipotezi için Bayes Faktörü (BF_01).
    H0: p = 0.5 (Tam eşitlik)
    H1: p ~ Uniform(0, 1) (Beta(1, 1))
    BF_01 = (N + 1) * C(N, k) * (0.5)^N
    log(BF_01) = log(N + 1) + lgamma(N+1) - lgamma(k+1) - lgamma(N-k+1) - N * log(2)
    """
    n = count1 + count2
    k = count1
    if n == 0:
        return {'bf01': 1.0, 'log_bf01': 0.0, 'interpretation': 'Yetersiz Veri'}

    log_comb = math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    log_bf01 = math.log(n + 1) + log_comb - n * math.log(2.0)
    
    # Güvenli exp
    if log_bf01 > 700:
        bf01 = float('inf')
    elif log_bf01 < -700:
        bf01 = 0.0
    else:
        bf01 = math.exp(log_bf01)

    # Jeffreys yorum ölçeği
    if bf01 > 100:
        interp = 'H0 lehine belirleyici (decisive) kanıt'
    elif bf01 > 30:
        interp = 'H0 lehine çok güçlü (very strong) kanıt'
    elif bf01 > 10:
        interp = 'H0 lehine güçlü (strong) kanıt'
    elif bf01 > 3:
        interp = 'H0 lehine orta (moderate) kanıt'
    elif bf01 > 1:
        interp = 'H0 lehine zayıf/anekdotal (anecdotal) kanıt'
    elif bf01 == 1:
        interp = 'Eşit kanıt (nötr)'
    else:
        interp = 'H1 lehine kanıt (H0 aleyhine)'

    return {
        'count1': count1,
        'count2': count2,
        'total': n,
        'log_bf01': round(log_bf01, 4),
        'bf01': round(bf01, 4) if bf01 != float('inf') else 'inf',
        'interpretation': interp
    }

if __name__ == "__main__":
    # Quick self-test
    chi = chi_square_goodness_of_fit([32, 13], [0.711, 0.289])
    print("Chi2 test Deniz/Kara sample:", chi)
    z = z_test_equal_frequencies(115, 115)
    print("Z test Dunya/Ahirat:", z)
    tost = equivalence_test_tost(115, 115, margin=0.05)
    print("TOST test Dunya/Ahirat:", tost)
    bf = bayes_factor_binomial(115, 115)
    print("Bayes Factor Dunya/Ahirat:", bf)
    bh = benjamini_hochberg([0.001, 0.02, 0.04, 0.07, 0.15])
    print("BH FDR:", bh)
