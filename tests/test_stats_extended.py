#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Genişletilmiş İstatistiksel Yöntemler Birim Testleri (FDR, TOST, Bayes Factor)
"""

import unittest
from mirat.stats import (
    benjamini_hochberg,
    equivalence_test_tost,
    bayes_factor_binomial,
    z_test_equal_frequencies
)

class TestStatsExtended(unittest.TestCase):
    def test_benjamini_hochberg_ordering(self):
        # Bilinen örnek: [0.001, 0.02, 0.04, 0.07, 0.15] (m=5)
        # q1 = min(0.001 * 5/1, ...) = 0.005
        # q2 = 0.02 * 5/2 = 0.05
        # q3 = 0.04 * 5/3 = 0.0667
        p_vals = [0.001, 0.02, 0.04, 0.07, 0.15]
        res = benjamini_hochberg(p_vals, fdr_level=0.05)
        self.assertEqual(len(res), 5)
        self.assertTrue(res[0]['is_significant_fdr'])
        self.assertTrue(res[1]['is_significant_fdr'])
        self.assertFalse(res[2]['is_significant_fdr'])
        self.assertEqual(res[0]['q_value'], 0.005)

    def test_benjamini_hochberg_dict_input(self):
        p_dict = {'claim_a': 0.001, 'claim_b': 0.50}
        res = benjamini_hochberg(p_dict, fdr_level=0.05)
        self.assertIn('claim_a', res)
        self.assertTrue(res['claim_a']['is_significant_fdr'])
        self.assertFalse(res['claim_b']['is_significant_fdr'])

    def test_tost_equivalence(self):
        # 1000 vs 1000 çok yüksek örneklemde %5 marjda kesin denk olmalı
        res = equivalence_test_tost(1000, 1000, margin=0.05, alpha=0.05)
        self.assertTrue(res['is_equivalent'])
        self.assertLess(res['p_tost'], 0.001)

        # 100 vs 200 denk olmamalı
        res_diff = equivalence_test_tost(100, 200, margin=0.05, alpha=0.05)
        self.assertFalse(res_diff['is_equivalent'])

    def test_bayes_factor_binomial(self):
        # 115 vs 115 için H0 lehine pozitif ve güçlü kanıt olmalı (BF > 10)
        res = bayes_factor_binomial(115, 115)
        self.assertGreater(res['bf01'], 10.0)
        self.assertGreater(res['log_bf01'], 2.0)
        self.assertIn('güçlü', res['interpretation'])

        # 100 vs 200 için H0 aleyhine (BF < 1) olmalı
        res_diff = bayes_factor_binomial(100, 200)
        self.assertLess(res_diff['bf01'], 1.0)

if __name__ == '__main__':
    unittest.main()
