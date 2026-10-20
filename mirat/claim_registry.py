#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Bilimsel İddia Denetçisi ve Ön-Kayıt Defteri (Scientific Claim Auditor & Preregistration)
Tüm iddiaları toplar, çoklu test düzeltmesi (FDR), duyarlılık (sensitivity) analizi,
sıfır modeli karşılaştırması ve hash zincirli ön-kayıt (preregistration) defteri ile denetler.
"""

import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from mirat.database import MiratDB
from mirat.stats import (
    benjamini_hochberg,
    equivalence_test_tost,
    bayes_factor_binomial,
    z_test_equal_frequencies
)
from mirat.null_models import MiratNullModel

PREREG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "veriler", "preregistration.jsonl")

class ClaimRegistry:
    def __init__(self, db=None):
        self.db = db if db is not None else MiratDB()
        self.null_model = MiratNullModel(self.db)
        self.claims = []

    def register_claim(self, claim_id, title, category, counts, filter_description, raw_p_value, notes="",
                       filter_dependent=False):
        """Bir iddiayı denetim havuzuna ekler.
        filter_dependent=True: sayımlardan biri sonuç görüldükten sonra seçilebilecek ad hoc bir
        morfolojik filtreye dayanıyorsa işaretlenir; böyle bir eşitlik 'Altın Standart' alamaz."""
        self.claims.append({
            'filter_dependent': filter_dependent,
            'claim_id': claim_id,
            'title': title,
            'category': category,
            'counts': counts,
            'filter_description': filter_description,
            'raw_p_value': raw_p_value,
            'notes': notes
        })

    def run_full_audit(self):
        """
        Kayıtlı tüm iddialara FDR, TOST, Bayes Faktörü ve Sıfır Modeli
        denetimi uygulayarak tarafsız jüri değerlendirme raporu üretir.
        """
        if not self.claims:
            self._load_standard_claims()

        # 1. FDR Düzeltmesi
        p_dict = {c['claim_id']: c['raw_p_value'] for c in self.claims}
        bh_results = benjamini_hochberg(p_dict, fdr_level=0.05)

        base_rate_info = self.null_model.get_equal_frequency_base_rate(min_freq=20)
        base_rate_p = base_rate_info['base_rate_probability']

        audited_claims = []
        for c in self.claims:
            cid = c['claim_id']
            fdr_info = bh_results.get(cid, {})
            q_val = fdr_info.get('q_value', c['raw_p_value'])
            
            c1, c2 = c['counts'][0], c['counts'][1]
            total = c1 + c2

            tost_res = equivalence_test_tost(c1, c2, margin=0.05)
            bf_res = bayes_factor_binomial(c1, c2)

            # Sınıflandırma
            if c1 == c2 and c.get('filter_dependent'):
                tier = "Eşit ama Filtre Bağımlı (Ad Hoc Seçim Riski)"
                status_color = "yellow"
            elif c1 == c2 and bf_res['log_bf01'] > 2.0:
                tier = "Altın Standart (Güçlü Bayes & Eşitlik)"
                status_color = "green"
            elif tost_res['is_equivalent']:
                tier = "Denk (TOST %5 Marjında Uyumlu)"
                status_color = "cyan"
            elif q_val < 0.05:
                tier = "Anlamlı Sapma (FDR Doğrulanmış)"
                status_color = "blue"
            else:
                tier = "Sıfır Modeliyle Uyumlu / Zayıf"
                status_color = "gray"

            audited_claims.append({
                'id': cid,
                'title': c['title'],
                'category': c['category'],
                'counts': f"{c1} vs {c2}",
                'raw_p': c['raw_p_value'],
                'q_value_fdr': q_val,
                'tost_equivalent': tost_res['is_equivalent'],
                'tost_p': tost_res['p_tost'],
                'bayes_factor_bf01': bf_res['bf01'],
                'bayes_interpretation': bf_res['interpretation'],
                'filter_notes': c['filter_description'],
                'filter_dependent': bool(c.get('filter_dependent')),
                'audit_tier': tier,
                'base_rate_p': base_rate_p
            })

        return {
            'total_claims_audited': len(audited_claims),
            'base_rate_equal_pair_chance': base_rate_info['base_rate_percentage'],
            'claims': audited_claims
        }

    def _load_standard_claims(self):
        """MİRAT'ın temel analiz katmanlarındaki ana iddiaları kaydeder."""
        # 1. Dünya vs Ahiret
        dunya = len([s for s in self.db.search_lemma('دُنْيا')])
        ahira = len([s for s in self.db.search_root('أخر') if s['pos'] == 'N' and ('اخره' in s['clean_form'] or 'خرة' in s['form'] or 'خرت' in s['form'] or 'خِرَة' in s['form'])])
        self.register_claim('theo_dunya_ahira', 'Dünya vs Ahiret', 'Teoloji', (dunya, ahira),
                            'Dünya lemma araması; Ahiret ise Noun + son ek filtresi', 1.0,
                            notes='Birebir 115=115, ancak Ahiret filtresi morfolojik olarak seçilidir.',
                            filter_dependent=True)

        # 2. Melek vs Şeytan
        malak = len([s for s in self.db.search_root('ملك') if s['lemma'] in ['مَلَك', 'مَلائِكَة']])
        shaytan = len([s for s in self.db.search_root('شطن') if s['lemma'] in ['شَيْطان', 'شَياطِين']])
        self.register_claim('theo_malak_shaytan', 'Melek vs Şeytan', 'Teoloji', (malak, shaytan),
                            'Melek ve Şeytan lemmaları (tekil ve çoğul)', 1.0,
                            notes='Birebir 88=88 mutlak eşitlik.')

        # 3. Fayda vs Zarar (Nef vs Fesad)
        nef = len(self.db.search_root('نفع'))
        fesad = len(self.db.search_root('فسد'))
        z_nef = z_test_equal_frequencies(nef, fesad)['p_value']
        self.register_claim('ethic_nef_fesad', 'Fayda vs Fesad/Zarar', 'Etik', (nef, fesad),
                            'Kök düzeyinde tam arama [نفع] vs [فسد]', z_nef,
                            notes='Kök düzeyinde 50=50 birebir eşitlik.')

        # 4. Çocukluk vs İhtiyarlık
        tifl = len(self.db.search_root('طفل'))
        seyh = len(self.db.search_root('شيخ'))
        z_age = z_test_equal_frequencies(tifl, seyh)['p_value']
        self.register_claim('bio_tifl_seyh', 'Çocukluk vs İhtiyarlık', 'Biyoloji', (tifl, seyh),
                            'Kök düzeyinde tam arama [طفل] vs [شيخ]', z_age,
                            notes='Kök düzeyinde 4=4 birebir eşitlik.')

        # 5. Fuad vs Lübb (Duygu vs Akıl)
        fuad = len(self.db.search_root('فأد'))
        lubb = len(self.db.search_root('لبب'))
        z_mind = z_test_equal_frequencies(fuad, lubb)['p_value']
        self.register_claim('psy_fuad_lubb', 'Fuad (Gönül) vs Lübb (Akıl)', 'Psikoloji', (fuad, lubb),
                            'Kök düzeyinde tam arama [فأد] vs [لبب]', z_mind,
                            notes='Kök düzeyinde 16=16 birebir eşitlik.')

        # 6. Güneş vs Ay
        sems = len(self.db.search_root('شمس'))
        qmr = len(self.db.search_root('قمر'))
        z_astro = z_test_equal_frequencies(sems, qmr)['p_value']
        self.register_claim('cosmo_sems_qmr', 'Güneş vs Ay', 'Kozmoloji', (sems, qmr),
                            'Kök düzeyinde [شمس] (33) vs [قمر] (27)', z_astro,
                            notes='Yaklaşık simetri (%55 - %45).')

        # 7. Musibet vs Şükür
        musibet = len(self.db.search_root('صوب'))
        sukur = len(self.db.search_root('شكر'))
        z_mus = z_test_equal_frequencies(musibet, sukur)['p_value']
        self.register_claim('ethic_musibet_sukur', 'Musibet vs Şükür', 'Etik', (musibet, sukur),
                            'Kök düzeyinde [صوب] (77) vs [شكر] (75)', z_mus,
                            notes='Yüksek simetri (%50.6 - %49.4).')

    # -------------------------------------------------------------
    # HASH ZİNCİRLİ ÖN-KAYIT DEFTERİ (PREREGISTRATION LOG)
    # -------------------------------------------------------------
    @staticmethod
    def append_preregistration(hypothesis_text, model_name, target_roots, expected_relation):
        """
        Yeni bir hipotezi sayımdan ÖNCE hash zincirli JSONL defterine kaydeder.
        Bu, sonuç görüldükten sonra filtre uydurulduğu (p-hacking) şüphesini sıfırlar.
        """
        os.makedirs(os.path.dirname(PREREG_FILE), exist_ok=True)
        prev_hash = "GENESIS_MIRAT_V5_HASH"
        
        if os.path.exists(PREREG_FILE):
            with open(PREREG_FILE, "r", encoding="utf-8") as f:
                lines = [l.strip() for l in f if l.strip()]
                if lines:
                    last_record = json.loads(lines[-1])
                    prev_hash = last_record.get('hash', prev_hash)

        record_data = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'prev_hash': prev_hash,
            'model_name': model_name,
            'hypothesis': hypothesis_text,
            'target_roots': target_roots,
            'expected_relation': expected_relation
        }
        
        # SHA-256 zinciri oluştur
        payload = json.dumps(record_data, sort_keys=True, ensure_ascii=False)
        curr_hash = hashlib.sha256(payload.encode('utf-8')).hexdigest()
        record_data['hash'] = curr_hash

        with open(PREREG_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps(record_data, ensure_ascii=False) + "\n")

        return record_data

    @staticmethod
    def verify_preregistration_chain():
        """Ön-kayıt defterinin bütünlüğünü ve zincir kırılmasını doğrular."""
        if not os.path.exists(PREREG_FILE):
            return {'valid': True, 'count': 0, 'message': 'Ön-kayıt defteri henüz boş.'}

        with open(PREREG_FILE, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f if l.strip()]

        expected_prev = "GENESIS_MIRAT_V5_HASH"
        for idx, line in enumerate(lines):
            rec = json.loads(line)
            actual_hash = rec.pop('hash', '')
            actual_prev = rec.get('prev_hash', '')
            
            if actual_prev != expected_prev:
                return {'valid': False, 'corrupted_at_index': idx, 'error': 'Geçersiz prev_hash zinciri'}

            payload = json.dumps(rec, sort_keys=True, ensure_ascii=False)
            recalculated = hashlib.sha256(payload.encode('utf-8')).hexdigest()
            if recalculated != actual_hash:
                return {'valid': False, 'corrupted_at_index': idx, 'error': 'Hash uyumsuzluğu'}

            expected_prev = actual_hash

        return {'valid': True, 'count': len(lines), 'latest_hash': expected_prev}

if __name__ == "__main__":
    registry = ClaimRegistry()
    audit = registry.run_full_audit()
    print("MİRAT İddia Denetimi Sonuçları:")
    print(f"Toplam Denetlenen İddia: {audit['total_claims_audited']}")
    print(f"Rastgele Kök Eşitlik Baz Oranı: %{audit['base_rate_equal_pair_chance']}")
    print("-" * 75)
    for c in audit['claims']:
        print(f"[{c['id']}] {c['title']} ({c['counts']})")
        print(f"  • FDR q: {c['q_value_fdr']} | Bayes BF01: {c['bayes_factor_bf01']} ({c['bayes_interpretation']})")
        print(f"  • Sınıflandırma: {c['audit_tier']}")
        print(f"  • Filtre Notu: {c['filter_notes']}\n")
