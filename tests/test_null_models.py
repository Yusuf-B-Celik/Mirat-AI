#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Sıfır Modelleri, İddia Denetçisi ve Ön-Kayıt Bütünlüğü Birim Testleri
"""

import os
import unittest
from mirat.database import MiratDB
from mirat.null_models import MiratNullModel
from mirat.claim_registry import ClaimRegistry, PREREG_FILE

class TestNullModelsAndAuditor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.db = MiratDB()
        cls.null_model = MiratNullModel(cls.db)
        cls.registry = ClaimRegistry(cls.db)

    def test_base_rate_calculation(self):
        res = self.null_model.get_equal_frequency_base_rate(min_freq=20)
        self.assertEqual(res['min_frequency_threshold'], 20)
        self.assertGreater(res['total_qualifying_roots'], 400)
        self.assertGreater(res['exact_equal_frequency_pairs'], 500)
        self.assertGreater(res['base_rate_probability'], 0.005)
        self.assertLess(res['base_rate_probability'], 0.05)

    def test_claim_registry_audit(self):
        audit = self.registry.run_full_audit()
        self.assertGreaterEqual(audit['total_claims_audited'], 5)
        claims_map = {c['id']: c for c in audit['claims']}
        self.assertIn('theo_dunya_ahira', claims_map)
        # Ad hoc Ahiret filtresi nedeniyle 115=115 eşitliği Altın Standart alamaz
        self.assertEqual(claims_map['theo_dunya_ahira']['audit_tier'], 'Eşit ama Filtre Bağımlı (Ad Hoc Seçim Riski)')
        self.assertTrue(claims_map['theo_dunya_ahira']['filter_dependent'])

    def test_preregistration_hash_chain(self):
        # Geçici bir ön-kayıt oluştur ve zinciri doğrula
        rec1 = ClaimRegistry.append_preregistration(
            hypothesis_text="Test hipotezi: Hakikat vs Batıl simetrisi",
            model_name="gpt-6-luna",
            target_roots=["حقق", "بطل"],
            expected_relation="equal_frequency"
        )
        self.assertIn('hash', rec1)
        self.assertIn('prev_hash', rec1)

        # İkinci halkayı ekle
        rec2 = ClaimRegistry.append_preregistration(
            hypothesis_text="İkinci test: Sabır vs Şükür",
            model_name="deepseek-v4.1-flash",
            target_roots=["صبر", "شكر"],
            expected_relation="positive_correlation"
        )
        self.assertEqual(rec2['prev_hash'], rec1['hash'])

        # Bütünlüğü doğrula
        chain_status = ClaimRegistry.verify_preregistration_chain()
        self.assertTrue(chain_status['valid'])
        self.assertGreaterEqual(chain_status['count'], 2)

if __name__ == '__main__':
    unittest.main()
