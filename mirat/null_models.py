#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Sıfır Modelleri ve Rastlantısallık Karşılaştırma Modülü (Null Models & Baselines)
Her matematiksel ve simetrik iddianın "rastlantısal bir metinde ne sıklıkla çıkacağını"
Monte Carlo permütasyonları, baz oran (base-rate) analizleri ve sıfır dağılımlarıyla ölçer.
"""

import collections
import math
import random
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'scripts'))
from mirat.database import MiratDB
from mirat.stats import linearity_rank_test

class MiratNullModel:
    def __init__(self, db=None):
        self.db = db if db is not None else MiratDB()

    def get_equal_frequency_base_rate(self, min_freq=20):
        """
        Korpus içerisindeki kökler arasında rastgele seçilen iki kökün
        birebir aynı frekansta olma (tam eşitlik) olasılığını hesaplar.
        """
        with self.db.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT frequency FROM roots WHERE frequency >= ? AND root IS NOT NULL", (min_freq,))
            freqs = [r[0] for r in c.fetchall()]

        total_roots = len(freqs)
        if total_roots < 2:
            return {'total_roots': total_roots, 'total_pairs': 0, 'equal_pairs': 0, 'base_rate': 0.0}

        total_pairs = total_roots * (total_roots - 1) // 2
        counter = collections.Counter(freqs)
        equal_pairs = sum(cnt * (cnt - 1) // 2 for cnt in counter.values() if cnt > 1)
        base_rate = equal_pairs / total_pairs if total_pairs > 0 else 0.0

        return {
            'min_frequency_threshold': min_freq,
            'total_qualifying_roots': total_roots,
            'total_possible_pairs': total_pairs,
            'exact_equal_frequency_pairs': equal_pairs,
            'base_rate_probability': round(base_rate, 6),
            'base_rate_percentage': round(base_rate * 100, 4),
            'scientific_context': f"Frekansı >={min_freq} olan {total_roots} kök arasından rastgele seçilen 2 kökün tam eşit frekansa sahip olma baz şansı %{round(base_rate*100, 2)}'dir ({equal_pairs:,}/{total_pairs:,} çift)."
        }

    def test_shuffled_chronology(self, observed_sequences, ideal_order, n_permutations=5000, seed=42):
        """
        Kronolojik/Doğrusal sıralama iddiaları (Örn: Embriyoloji aşamaları) için
        Monte Carlo permütasyon sıfır modeli testi.
        """
        rng = random.Random(seed)
        obs_res = linearity_rank_test(observed_sequences, ideal_order)
        obs_tau = obs_res['kendall_tau']
        obs_matches = obs_res['perfect_chronological_matches']

        stage_pool = list(ideal_order)
        greater_or_equal_count = 0
        perm_taus = []

        for _ in range(n_permutations):
            shuffled_stages = list(stage_pool)
            rng.shuffle(shuffled_stages)
            shuffled_map = {orig: shuf for orig, shuf in zip(stage_pool, shuffled_stages)}
            
            # Gözlemlenen dizileri karıştırılmış haritaya göre dönüştür
            shuffled_obs = []
            for seq in observed_sequences:
                shuffled_obs.append([shuffled_map.get(item, item) for item in seq])
                
            res = linearity_rank_test(shuffled_obs, ideal_order)
            perm_tau = res['kendall_tau']
            perm_taus.append(perm_tau)
            if perm_tau >= obs_tau:
                greater_or_equal_count += 1

        empirical_p = (greater_or_equal_count + 1) / (n_permutations + 1)
        mean_null_tau = sum(perm_taus) / len(perm_taus) if perm_taus else 0.0
        
        # Surprise score (Shannon bits: -log2(p))
        surprise_bits = -math.log2(empirical_p) if empirical_p > 0 else float('inf')

        return {
            'observed_tau': obs_tau,
            'observed_matches': obs_matches,
            'n_permutations': n_permutations,
            'greater_or_equal_count': greater_or_equal_count,
            'mean_null_tau': round(mean_null_tau, 4),
            'empirical_p_value': round(empirical_p, 6),
            'surprise_bits': round(surprise_bits, 2),
            'is_significant_null': empirical_p < 0.01,
            'interpretation': f"Rastgele permütasyonlarda böylesi bir kronolojik sıralama elde etme şansı p={round(empirical_p, 5)} (Şaşırtıcılık: {round(surprise_bits, 1)} bit)."
        }

    def test_waveform_peak_significance(self, verse_counts, target_peaks=None, n_permutations=10000, seed=42):
        """
        114 Surenin ayet sayıları dalga formu için HEDEFSİZ yapı testi (v6 düzeltmesi).

        Eski sürüm, sonuç görüldükten sonra seçilmiş tepe noktalarını (2, 7, 26, 37) hedef alıyordu;
        bu döngüsel (post hoc) bir testtir ve p-değeri anlamsızdır. Yeni sürüm hiçbir hedef
        kullanmaz; dizinin rastgele bir permütasyondan farkını üç önceden tanımlı istatistikle sınar:
          1. Büyük tepe sayısı (>= 50 ayet ve iki komşusundan büyük/eşit)
          2. Mushaf sırası ile ayet sayısı Spearman korelasyonu (uzundan kısaya düzen)
          3. Komşu sure ayet sayısı farklarının ortalaması (pürüzlülük; düşükse yumuşak dalga)
        target_peaks verilirse yalnızca bilgi amaçlı raporlanır, p-değerine KATILMAZ.
        """
        rng = random.Random(seed)

        def count_major_peaks(counts):
            peaks = []
            for i in range(len(counts)):
                v = counts[i]
                left_ok = (i == 0) or (counts[i - 1] <= v)
                right_ok = (i == len(counts) - 1) or (counts[i + 1] <= v)
                if left_ok and right_ok and v >= 50:
                    peaks.append(i + 1)
            return peaks

        def ranks(x):
            order = sorted(range(len(x)), key=lambda i: x[i])
            r = [0.0] * len(x)
            i = 0
            while i < len(order):
                j = i
                while j + 1 < len(order) and x[order[j + 1]] == x[order[i]]:
                    j += 1
                for k in range(i, j + 1):
                    r[order[k]] = (i + j) / 2.0 + 1
                i = j + 1
            return r

        def spearman_with_index(counts):
            rx, ry = list(range(1, len(counts) + 1)), ranks(counts)
            n = len(counts)
            mx, my = sum(rx) / n, sum(ry) / n
            sxy = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
            sxx = sum((a - mx) ** 2 for a in rx)
            syy = sum((b - my) ** 2 for b in ry)
            return sxy / math.sqrt(sxx * syy)

        def roughness(counts):
            return sum(abs(a - b) for a, b in zip(counts, counts[1:])) / (len(counts) - 1)

        obs_peaks = count_major_peaks(verse_counts)
        obs = {'peaks': len(obs_peaks), 'rho': spearman_with_index(verse_counts), 'rough': roughness(verse_counts)}
        null = {'peaks': [], 'rho': [], 'rough': []}
        counts_copy = list(verse_counts)
        for _ in range(n_permutations):
            rng.shuffle(counts_copy)
            null['peaks'].append(len(count_major_peaks(counts_copy)))
            null['rho'].append(spearman_with_index(counts_copy))
            null['rough'].append(roughness(counts_copy))

        def p_two_sided(key):
            vals = null[key]
            mu = sum(vals) / len(vals)
            dev = abs(obs[key] - mu)
            hits = sum(1 for v in vals if abs(v - mu) >= dev - 1e-12)
            return (hits + 1) / (len(vals) + 1), mu

        p_peaks, mu_peaks = p_two_sided('peaks')
        p_rho, mu_rho = p_two_sided('rho')
        p_rough, mu_rough = p_two_sided('rough')
        empirical_p = min(1.0, 3 * min(p_peaks, p_rho, p_rough))  # Bonferroni (3 istatistik)

        result = {
            'test_design': 'hedefsiz (target-free) yapı testi; post hoc tepe seçimi kaldırıldı',
            'observed_peaks': obs_peaks,
            'observed_peaks_count': obs['peaks'],
            'mean_random_peaks_count': round(mu_peaks, 2),
            'p_peaks': round(p_peaks, 5),
            'spearman_mushaf_order': round(obs['rho'], 4),
            'p_spearman': round(p_rho, 5),
            'roughness': round(obs['rough'], 2),
            'mean_random_roughness': round(mu_rough, 2),
            'p_roughness': round(p_rough, 5),
            'n_permutations': n_permutations,
            'empirical_p_value': round(empirical_p, 5),
            'surprise_bits': round(-math.log2(empirical_p), 2),
            'evaluation': (
                f"Hedefsiz test: büyük tepe sayısı {obs['peaks']} (rastgele ort. {mu_peaks:.1f}, p={p_peaks:.4f}); "
                f"mushaf sırası-ayet sayısı Spearman rho={obs['rho']:.3f} (p={p_rho:.4f}); pürüzlülük "
                f"{obs['rough']:.1f} (rastgele {mu_rough:.1f}, p={p_rough:.4f}). Yapının ana kaynağı, surelerin "
                f"kabaca uzundan kısaya dizilmesidir; belirli tepe noktalarına (ör. Allah lafzı sütunları) dair "
                f"bir iddia bu testle desteklenemez, çünkü o hedefler veriye bakılarak seçilmişti."),
        }
        if target_peaks:
            result['post_hoc_targets_info_only'] = sorted(set(obs_peaks) & set(target_peaks))
        return result

if __name__ == "__main__":
    db = MiratDB()
    null_model = MiratNullModel(db)
    br = null_model.get_equal_frequency_base_rate(20)
    print("Base rate (>=20):", br)
    
    # Test waveform peaks
    from build_quran_markdown import SURAH_METADATA
    v_counts = [SURAH_METADATA[s]['verses'] for s in range(1, 115)]
    wf_test = null_model.test_waveform_peak_significance(v_counts, n_permutations=1000)
    print("Waveform test:", wf_test)
