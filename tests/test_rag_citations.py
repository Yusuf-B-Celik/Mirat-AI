#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Soru-Cevap ve Atıf Doğrulama (Citation Grounding) Birim Testleri
"""

import unittest
from mirat.database import MiratDB
from mirat.rag.qa import MiratQA

class TestRAGAndCitations(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = MiratDB()
        cls.qa = MiratQA(cls.db)

    def test_citation_verification_valid(self):
        text = "Kur'an'da [1:1] ve [2:255] ayetlerinde açıkça buyrulmaktadır."
        res = self.qa._verify_citations_in_text(text)
        self.assertEqual(res['total_citations_found'], 2)
        self.assertEqual(len(res['verified_citations']), 2)
        self.assertEqual(len(res['hallucinated_citations']), 0)
        self.assertTrue(res['is_fully_grounded'])

    def test_citation_verification_hallucination_detected(self):
        # 115:10 diye bir ayet yoktur (Kur'an 114 suredir!)
        # 1:99 diye bir ayet yoktur (Fatiha 7 ayettir!)
        text = "Bu konuda [115:10] ve [1:99] ayetlerine bakabilirsiniz."
        res = self.qa._verify_citations_in_text(text)
        self.assertEqual(res['total_citations_found'], 2)
        self.assertEqual(len(res['hallucinated_citations']), 2)
        self.assertFalse(res['is_fully_grounded'])
        self.assertEqual(res['citation_integrity_score'], 0.0)

    def test_numeric_query_deterministic_bypass(self):
        # Sayısal sorular LLM'e gitmeden SQL katmanından kesin dönmeli
        ans = self.qa.answer_question("Kur'an'da deniz kelimesi kaç kez geçer?")
        self.assertEqual(ans['type'], 'deterministic_sql_count')
        self.assertIn('42 defa', ans['answer'])

if __name__ == '__main__':
    unittest.main()
