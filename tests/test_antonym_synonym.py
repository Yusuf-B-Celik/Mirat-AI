#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Zıt ve Eş Anlamlı Motoru Birim Testleri
"""

import unittest
from mirat.database import MiratDB
from mirat.antonym_synonym_engine import MiratAntonymSynonymEngine

class TestAntonymSynonymEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = MiratDB()
        cls.engine = MiratAntonymSynonymEngine(cls.db)

    def test_full_analysis_rules(self):
        res = self.engine.run_full_analysis()
        self.assertIn('rule1_root_exact_parity', res)
        self.assertIn('rule2_definite_noun_equality', res)
        self.assertIn('rule3_harmonic_ratios', res)
        self.assertIn('rule4_tibak_co_occurrence', res)
        self.assertIn('rule5_verbal_vs_nominal', res)
        self.assertIn('rule6_synonym_nuance_clusters', res)
        self.assertIn('rule7_symmetry_index_rankings', res)

    def test_rule1_nafa_fasad(self):
        r1 = self.engine.analyze_rule1_root_parity()
        nafa_p = [p for p in r1['items'] if 'نفع' in p['root1']][0]
        self.assertEqual(nafa_p['count1'], 50)
        self.assertEqual(nafa_p['count2'], 50)
        self.assertEqual(nafa_p['vsi_score'], 100.0)

    def test_rule6_synonyms(self):
        r6 = self.engine.analyze_rule6_synonym_clusters()
        clusters = r6['clusters']
        self.assertGreaterEqual(len(clusters), 4)

if __name__ == '__main__':
    unittest.main()
