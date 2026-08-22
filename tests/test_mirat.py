#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Sistemi Otomatik Birim ve Entegrasyon Testleri
"""

import unittest
from mirat.database import MiratDB
from mirat.stats import (
    chi_square_goodness_of_fit,
    z_test_equal_frequencies,
    co_occurrence_metrics,
    linearity_rank_test
)
from mirat.layers.layer1_geology import analyze_layer_1
from mirat.layers.layer2_cosmic import analyze_layer_2
from mirat.layers.layer3_ethics import analyze_layer_3
from mirat.layers.layer4_socioeconomic import analyze_layer_4
from mirat.layers.layer5_science import analyze_layer_5

class TestMiratSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = MiratDB()

    def test_database_counts(self):
        with self.db.get_connection() as conn:
            c = conn.cursor()
            c.execute("SELECT count(*) FROM segments")
            seg_count = c.fetchone()[0]
            c.execute("SELECT count(*) FROM words")
            word_count = c.fetchone()[0]
            c.execute("SELECT count(*) FROM roots")
            root_count = c.fetchone()[0]

        self.assertGreaterEqual(seg_count, 128000)
        self.assertGreaterEqual(word_count, 77000)
        self.assertGreaterEqual(root_count, 1600)

    def test_stats_chi_square(self):
        res = chi_square_goodness_of_fit([32, 13], [0.711, 0.289])
        self.assertIn('chi2', res)
        self.assertIn('p_value', res)
        self.assertEqual(res['df'], 1)

    def test_stats_z_test_exact(self):
        res = z_test_equal_frequencies(115, 115)
        self.assertEqual(res['z_score'], 0.0)
        self.assertEqual(res['p_value'], 1.0)
        self.assertTrue(res['is_symmetric'])

    def test_layer1_geology(self):
        res = analyze_layer_1(self.db)
        self.assertEqual(res['surface_balance']['sea_root'], 'بحر')
        self.assertGreater(res['surface_balance']['sea_count'], 30)
        self.assertGreater(res['surface_balance']['total_land_count'], 15)
        self.assertEqual(res['isostasy']['peg_root'], 'وتد')

    def test_layer2_cosmic(self):
        res = analyze_layer_2(self.db)
        self.assertGreater(res['calendar_cycle']['day_total_occurrences'], 300)
        self.assertEqual(res['calendar_cycle']['month_root'], 'شهر')

    def test_layer3_theological_symmetry(self):
        res = analyze_layer_3(self.db)
        theo = res['theological_symmetry']
        self.assertEqual(theo['dunya_count'], 115)
        self.assertEqual(theo['akhirah_count'], 115)
        self.assertTrue(theo['is_dunya_akhira_exact'])
        self.assertEqual(theo['malak_count'], 88)
        self.assertEqual(theo['shaytan_count'], 88)
        self.assertTrue(theo['is_malak_shaytan_exact'])

    def test_layer4_socioeconomic(self):
        res = analyze_layer_4(self.db)
        self.assertGreater(res['social_justice_infak']['feed_to_hunger_ratio'], 3.0)
        self.assertGreater(res['gender_variation']['biological_filter']['male_dhakar_count'], 0)

    def test_layer5_science(self):
        res = analyze_layer_5(self.db)
        self.assertEqual(res['embryology_linearity']['kendall_tau_score'], 1.0)
        self.assertTrue(res['embryology_linearity']['is_perfectly_linear'])
        self.assertEqual(res['seven_heavens']['phrase_exact_count'], 7)

if __name__ == '__main__':
    unittest.main()
