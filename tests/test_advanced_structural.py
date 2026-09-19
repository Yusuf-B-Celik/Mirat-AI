#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT İleri Yapısal, Grafiksel ve Kriptografik Motor Birim Testleri
"""

import unittest
from mirat.database import MiratDB
from mirat.advanced_structural_engine import AdvancedStructuralEngine

class TestAdvancedStructuralEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = MiratDB()
        cls.engine = AdvancedStructuralEngine(cls.db)

    def test_waveform_analysis(self):
        wf = self.engine.compute_waveform_analysis()
        self.assertEqual(wf['total_surahs'], 114)
        self.assertEqual(wf['max_verse_count'], 286)
        self.assertEqual(wf['min_verse_count'], 3)
        self.assertGreaterEqual(len(wf['major_peaks']), 10)

    def test_parity_milan_sulc(self):
        pm = self.engine.compute_parity_matrix()
        self.assertEqual(pm['even_count'], 57)
        self.assertEqual(pm['odd_count'], 57)
        self.assertEqual(pm['sum_of_even_sums'], 6236)
        self.assertEqual(pm['sum_of_odd_sums'], 6555)
        self.assertTrue(pm['even_equals_total_verses'])
        self.assertTrue(pm['odd_equals_total_surah_indices'])

    def test_cryptographic_palindromes(self):
        cp = self.engine.compute_cryptographic_patterns()
        self.assertEqual(cp['muqattaat_surah_count'], 29)
        self.assertEqual(cp['muqattaat_unique_letters_count'], 14)
        self.assertTrue(len(cp['palindromes']) >= 2)

    def test_phonetics_fawasil(self):
        ph = self.engine.compute_phonetics_and_acoustics()
        self.assertEqual(ph['total_verses'], 6236)
        self.assertEqual(ph['top_fawasil'][0]['letter'], 'ن')

if __name__ == '__main__':
    unittest.main()
