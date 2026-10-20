#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT v6 Keşif Motorları (Kategori 11-19) Birim Testleri
Tüm testler deterministiktir ve MIRAT_OFFLINE=1 altında canlı API çağrısı yapmadan çalışır.
"""

import os
import unittest
from mirat.features import get_corpus
from mirat.discovery.finding import Finding, rankdata, spearman, bh_adjust
from mirat.discovery import c11_chronology, c12_rhetoric, c13_number_morphology, c14_repetition
from mirat.discovery import c17_ring_detection, c18_information, c19_narrative


class TestDiscoveryEngines(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.corpus = get_corpus()

    def test_corpus_features(self):
        """Külliyatın ve morfolojik özelliklerin doğru yüklendiğini test eder."""
        self.assertEqual(len(self.corpus.segments), 130030)
        self.assertEqual(len(self.corpus.ayah_keys), 6236)
        # Fâtiha 1:5 fiilleri: na'budu (1P, V) ve nesta'în (1P, V)
        v15 = self.corpus.ayah_verbs(1, 5)
        self.assertEqual(len(v15), 2)
        self.assertEqual(v15[0].person, '1')
        self.assertEqual(v15[0].number, 'P')
        self.assertEqual(v15[1].person, '1')

    def test_finding_helpers(self):
        """İstatistiksel yardımcı fonksiyonları test eder."""
        # Rankdata tie handling
        ranks = rankdata([10, 20, 20, 30])
        self.assertEqual(ranks, [1.0, 2.5, 2.5, 4.0])
        # Spearman correlation
        rho = spearman([1, 2, 3, 4], [2, 4, 6, 8])
        self.assertAlmostEqual(rho, 1.0, places=5)
        # Benjamini-Hochberg adjustment
        findings = [
            Finding(id="f1", category="t", title="t1", method="m", metric="val", value=1.0, null_p=0.01),
            Finding(id="f2", category="t", title="t2", method="m", metric="val", value=2.0, null_p=0.04),
            Finding(id="f3", category="t", title="t3", method="m", metric="val", value=3.0, null_p=0.50),
        ]
        bh_adjust(findings)
        self.assertLess(findings[0].q_value, 0.05)
        self.assertLess(findings[1].q_value, 0.10)
        self.assertEqual(findings[2].q_value, 0.50)

    def test_c11_chronology(self):
        """Kategori 11 Kronolojik Evrim motorunu test eder."""
        findings, extras = c11_chronology.run(corpus=self.corpus)
        f_map = {f.id: f for f in findings}
        # Ayet uzunluğu trendi (c11_trend_00) pozitif ve anlamlı olmalı
        self.assertIn("c11_trend_00", f_map)
        trend_len = f_map["c11_trend_00"]
        self.assertGreater(trend_len.value, 0.5)
        self.assertLess(trend_len.null_p, 0.01)
        self.assertIn("c11_root_summary", f_map)

    def test_c12_rhetoric(self):
        """Kategori 12 Belâgat ve İltifat motorunu test eder."""
        findings, extras = c12_rhetoric.run(corpus=self.corpus)
        f_map = {f.id: f for f in findings}
        # Fâtiha 1:4 -> 1:5 gaibden muhataba iltifat geçişi yakalanmalı
        self.assertIn("c12_iltifat_gaib_muhatap", f_map)
        iltifat = f_map["c12_iltifat_gaib_muhatap"]
        self.assertTrue(any("1:4→1:5" in e for e in iltifat.evidence))
        # Ahiret sahnelerinde edilgen çatı testi
        self.assertIn("c12_passive_eschatology", f_map)
        self.assertLess(f_map["c12_passive_eschatology"].null_p, 0.05)

    def test_c13_number_morphology(self):
        """Kategori 13 Sayı Morfolojisi ve Fiil Babları motorunu test eder."""
        findings, extras = c13_number_morphology.run(corpus=self.corpus)
        f_map = {f.id: f for f in findings}
        self.assertIn("c13_singular_only", f_map)
        self.assertIn("c13_dual_surahs", f_map)
        # Rahmân suresi en yüksek ikil yoğunluğuna sahip olmalı
        self.assertIn("Rahmân", f_map["c13_dual_surahs"].evidence[0])

    def test_c14_repetition(self):
        """Kategori 14 Tekrar ve Formül Yapıları motorunu test eder."""
        findings, extras = c14_repetition.run(corpus=self.corpus)
        f_map = {f.id: f for f in findings}
        # Rahmân suresi nakaratı 31 kez tespit edilmeli
        self.assertIn("c14_refrain_55_13", f_map)
        self.assertEqual(f_map["c14_refrain_55_13"].value, 31)
        # Fâsıla semantik uyum testi anlamlı olmalı
        self.assertIn("c14_fasila_semantic_coherence", f_map)
        self.assertLess(f_map["c14_fasila_semantic_coherence"].null_p, 0.05)

    def test_c17_ring_detection(self):
        """Kategori 17 Halka Kompozisyonu motorunu test eder."""
        findings, extras = c17_ring_detection.run(corpus=self.corpus)
        f_map = {f.id: f for f in findings}
        # Küresel düzeyde sistematik halka iddiasının desteklenmediği dürüstçe raporlanmalı
        self.assertIn("c17_global_ayah", f_map)
        self.assertIn("c17_global_block", f_map)

    def test_c18_information(self):
        """Kategori 18 Bilgi Teorisi ve Dinamik motorunu test eder."""
        findings, extras = c18_information.run(corpus=self.corpus)
        f_map = {f.id: f for f in findings}
        self.assertIn("c18_dfa_ayah_length", f_map)
        self.assertGreater(f_map["c18_dfa_ayah_length"].value, 0.6)  # DFA alfa > 0.6 (kalıcı korelasyon)
        self.assertIn("c18_rhyme_boundary", f_map)
        self.assertLess(f_map["c18_rhyme_boundary"].null_p, 0.05)

    def test_c19_narrative(self):
        """Kategori 19 Kıssa ve Anlatı motorunu test eder."""
        findings, extras = c19_narrative.run(corpus=self.corpus)
        f_map = {f.id: f for f in findings}
        # Helak döngüsü kanonik sıralama uyumu pozitif ve anlamlı olmalı
        self.assertIn("c19_punishment_cycle_order", f_map)
        cycle_f = f_map["c19_punishment_cycle_order"]
        self.assertGreater(cycle_f.value, 0.2)
        self.assertLess(cycle_f.null_p, 0.01)
        # En çok anılan figür Musa olmalı
        self.assertIn("c19_episode_map", f_map)
        self.assertTrue(any("Mûsâ" in e for e in f_map["c19_episode_map"].evidence))


if __name__ == '__main__':
    unittest.main()
