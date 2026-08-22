#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Örüntü Madenciliği Birim Testleri
"""

import unittest
from mirat.database import MiratDB
from mirat.pattern_miner import MiratPatternMiner

class TestPatternMiner(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = MiratDB()
        cls.miner = MiratPatternMiner(cls.db)

    def test_run_all_categories(self):
        cats = self.miner.run_all_categories()
        self.assertEqual(len(cats), 10)
        self.assertIn('cat1_theological_symmetries', cats)
        self.assertIn('cat2_cosmology_astronomy', cats)
        self.assertIn('cat4_biology_genetics', cats)
        self.assertIn('cat5_chemistry_elements', cats)

    def test_category_patterns_count(self):
        cats = self.miner.run_all_categories()
        total_p = sum(len(c['patterns']) for c in cats.values())
        self.assertGreaterEqual(total_p, 40)

    def test_chemistry_iron(self):
        c5 = self.miner.mine_chemistry_elements()
        iron_p = c5['patterns'][0]
        self.assertEqual(iron_p['count1'], 57)
        self.assertEqual(iron_p['count2'], 26)

if __name__ == '__main__':
    unittest.main()
