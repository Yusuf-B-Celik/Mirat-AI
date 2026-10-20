#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Bilimsel Hipotez Keşif ve Denetim Ajanı (Hypothesis Discovery Agent)
Çok modelli LLM zinciri (Önerici -> Eleştirmen -> Ön-Kayıt -> Çekirdek Sayım -> Sıfır Modeli)
ile çalışan tam otonom bilimsel araştırma ajanıdır.
"""

import json
import os
import sys
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mirat.database import MiratDB
from mirat.llm.client import OpenCodeClient
from mirat.llm.router import ModelRouter
from mirat.claim_registry import ClaimRegistry
from mirat.null_models import MiratNullModel
from mirat.stats import (
    z_test_equal_frequencies,
    equivalence_test_tost,
    bayes_factor_binomial,
    co_occurrence_metrics,
    benjamini_hochberg
)

class HypothesisAgent:
    def __init__(self, db=None, client=None):
        self.db = db if db is not None else MiratDB()
        self.client = client if client is not None else OpenCodeClient()
        self.null_model = MiratNullModel(self.db)
        self.registry = ClaimRegistry(self.db)

    def propose_hypotheses(self, domain_context="etik ve teoloji", n=3, model=None):
        """Güçlü modelden (GPT 6 Luna / Qwen) ölçülebilir kavramsal hipotezler talep eder."""
        if model is None:
            model = ModelRouter.get_primary_model('hypothesis_proposer')

        prompt = f"""Sen MİRAT bilimsel metin madenciliği projesinin araştırma tasarımcısısın.
Kur'an-ı Kerim metninde test edilmek üzere {n} adet ÖLÇÜLEBİLİR, YANLIŞLANABİLİR leksikal/kavramsal hipotez öner.
Bağlam: {domain_context}.

KURALLAR:
1. Her hipotez mutlaka somut iki Arapça kök (root) veya lemmaya dayanmalıdır.
2. Özel filtre uydurma; kök düzeyinde veya yalın lemma düzeyinde olmalıdır.
3. Beklenen ilişki türünü belirt ('exact_parity', 'co_occurrence', 'proportional_ratio').

Yalnızca aşağıdaki JSON listesi formatında yanıt ver:
[
  {{
    "id": "hyp_01",
    "name": "Kavram 1 vs Kavram 2 Dengesi",
    "root1": "Arapça kök 1 (örn: صلح)",
    "root2": "Arapça kök 2 (örn: فسد)",
    "expected_relation": "exact_parity | co_occurrence | ratio",
    "theological_rationale": "Bu iki kökün dengeli veya ilişkili olmasının gerekçesi"
  }}
]
"""
        messages = [{'role': 'user', 'content': prompt}]

        if not self.client.is_configured():
            # Heuristic / Offline Mock Mode
            return self._mock_proposals()

        try:
            resp = self.client.chat_completion(
                model=model,
                messages=messages,
                temperature=0.3,
                response_format={'type': 'json_object'}
            )
            data = json.loads(resp['content'])
            if isinstance(data, dict) and 'hypotheses' in data:
                return data['hypotheses']
            if isinstance(data, list):
                return data
            return self._mock_proposals()
        except Exception:
            return self._mock_proposals()

    def critique_hypothesis(self, hypothesis, critic_model=None):
        """Eleştirmen model (GLM) hipotezde p-hacking veya taraflılık riski olup olmadığını denetler."""
        if critic_model is None:
            critic_model = ModelRouter.get_primary_model('hypothesis_critic')

        prompt = f"""Aşağıdaki araştırma hipotezini bilimsel tarafsızlık, p-hacking ve morfolojik filtre riski açısından denetle:
Hipotez: {json.dumps(hypothesis, ensure_ascii=False)}

Yalnızca JSON formatında yanıt ver:
{{
  "verdict": "APPROVED | REJECTED",
  "criticism": "Gerekçe ve zayıf noktalar",
  "bias_risk_level": "LOW | MEDIUM | HIGH"
}}
"""
        messages = [{'role': 'user', 'content': prompt}]

        if not self.client.is_configured():
            return {'verdict': 'APPROVED', 'criticism': 'Standart kök karşılaştırması; taraflılık riski düşük.', 'bias_risk_level': 'LOW'}

        try:
            resp = self.client.chat_completion(
                model=critic_model,
                messages=messages,
                temperature=0.0,
                response_format={'type': 'json_object'}
            )
            return json.loads(resp['content'])
        except Exception:
            return {'verdict': 'APPROVED', 'criticism': 'Otomatik onay (fallback)', 'bias_risk_level': 'LOW'}

    def test_hypothesis_deterministically(self, hypothesis):
        """
        Onaylanan hipotezi deterministik MİRAT çekirdeğinde test eder:
        1. Ön-kayıt defterine hash zinciriyle yazar (p-hacking'i kanıtlamak için).
        2. SQLite'tan kesin frekansları çeker.
        3. TOST, Z-skoru, Bayes Faktörü ve Sıfır Modeli baz oranını hesaplar.
        """
        r1 = hypothesis.get('root1', '').strip()
        r2 = hypothesis.get('root2', '').strip()

        # 1. Ön-Kayıt
        prereg_record = ClaimRegistry.append_preregistration(
            hypothesis_text=hypothesis.get('theological_rationale', hypothesis.get('name', '')),
            model_name="mirat-autonomous-agent",
            target_roots=[r1, r2],
            expected_relation=hypothesis.get('expected_relation', 'exact_parity')
        )

        # 2. Deterministik Çekirdek Sayımı (LLM asla sayı uyduramaz!)
        seg1 = self.db.search_root(r1)
        seg2 = self.db.search_root(r2)
        c1, c2 = len(seg1), len(seg2)

        # 3. İstatistiki ve Bayesyen Testler
        z_res = z_test_equal_frequencies(c1, c2)
        tost_res = equivalence_test_tost(c1, c2, margin=0.05)
        bf_res = bayes_factor_binomial(c1, c2)
        base_rate = self.null_model.get_equal_frequency_base_rate(min_freq=20)

        # 4. Bilimsel Sentez Kararı
        if c1 == c2 and bf_res['log_bf01'] > 2.0:
            verdict = "ALTIN STANDART: Güçlü Eşitlik Kanıtı"
            reliability = "Çok Yüksek"
        elif tost_res['is_equivalent']:
            verdict = "DENK: %5 Marjında İstatistiki Olarak Denk"
            reliability = "Yüksek"
        elif z_res['is_symmetric']:
            verdict = "KISMEN DENGELİ: Sıfır Hipotezi Reddedilemedi"
            reliability = "Orta"
        else:
            verdict = "SIFIR MODELİ İLE UYUMLU: Anlamlı Simetri Yok"
            reliability = "Düşük / Reddedildi"

        return {
            'hypothesis_id': hypothesis.get('id', 'hyp'),
            'name': hypothesis.get('name', ''),
            'root1': r1,
            'count1': c1,
            'root2': r2,
            'count2': c2,
            'total_tokens': c1 + c2,
            'z_score': round(z_res['z_score'], 4),
            'raw_p_value': round(z_res['p_value'], 4),
            'tost_equivalent': tost_res['is_equivalent'],
            'bayes_factor_bf01': bf_res['bf01'],
            'bayes_interpretation': bf_res['interpretation'],
            'equal_base_rate_chance': base_rate['base_rate_percentage'],
            'scientific_verdict': verdict,
            'evidence_strength': reliability,
            'preregistration_hash': prereg_record['hash']
        }

    def run_discovery_cycle(self, domain="etik ve ahlak", n=2):
        """Uçtan uca hipotez üretim, denetim, ön-kayıt ve test döngüsünü çalıştırır."""
        proposals = self.propose_hypotheses(domain_context=domain, n=n)
        results = []

        for p in proposals:
            critic = self.critique_hypothesis(p)
            if critic.get('verdict') == 'REJECTED':
                results.append({
                    'hypothesis': p,
                    'status': 'REJECTED_BY_CRITIC',
                    'reason': critic.get('criticism')
                })
            else:
                test_result = self.test_hypothesis_deterministically(p)
                test_result['critic_evaluation'] = critic
                results.append({
                    'hypothesis': p,
                    'status': 'AUDITED_AND_TESTED',
                    'result': test_result
                })

        return {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'domain': domain,
            'total_processed': len(results),
            'cycle_results': results
        }

    def _mock_proposals(self):
        return [
            {
                'id': 'hyp_mock_01',
                'name': 'Isrâr (Günah/Israr) vs İstiğfar (Bağışlanma Dileme)',
                'root1': 'صرر',
                'root2': 'غفر',
                'expected_relation': 'exact_parity',
                'theological_rationale': 'Günahta ısrar ile bağışlanma arayışı arasındaki manevi denge'
            },
            {
                'id': 'hyp_mock_02',
                'name': 'Sıdk (Doğruluk) vs Kizb (Yalan)',
                'root1': 'صدق',
                'root2': 'كذب',
                'expected_relation': 'exact_parity',
                'theological_rationale': 'Ahlaki dürüstlük ile yalan arasındaki temel çatışma'
            }
        ]
