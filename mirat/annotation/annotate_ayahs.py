#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Ayet Anotasyon ve Anlamsal Etiketleme Motoru (Ayah Semantic Annotator)
40 sabit Kur'ani tema, varlıklar (Peygamberler, Kavimler, Mekanlar) ve
konuşma eylemlerini (speech act) 3 farklı LLM ile paralel etiketler ve konsensüsü kaydeder.
"""

import glob
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from mirat.database import MiratDB
from mirat.llm.client import OpenCodeClient
from mirat.llm.router import ModelRouter
from mirat.annotation.agreement import AgreementEngine

CANONICAL_THEMES = [
    "tevhid", "nübüvvet", "ahiret", "adalet", "infak", "cihat", "sabır", "şükür",
    "ibadet", "hidayet", "dalalet", "kıssa", "yaratılış", "tabiat", "ahlak", "aile",
    "hukuk", "mucize", "ilim", "rahmet", "azap", "cehennem", "cennet", "melek",
    "cin/şeytan", "namaz", "zekat", "oruç", "hac", "dua", "tövbe", "istiğfar",
    "fitne", "nifak", "takva", "ihlas", "şirk", "küfür", "havf/reca", "kıyamet"
]

class AyahAnnotator:
    def __init__(self, db=None, client=None):
        self.db = db if db is not None else MiratDB()
        self.client = client if client is not None else OpenCodeClient()
        self.agreement_engine = AgreementEngine()
        self._sure_meals_cache = {}

    def get_ayah_meal(self, surah_num, ayah_num):
        """kuran/sureler/ dizinindeki dosyalardan ilgili ayetin Türkçe mealini çeker."""
        if surah_num not in self._sure_meals_cache:
            proj_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            pattern = os.path.join(proj_root, "kuran", "sureler", f"{surah_num:03d}_*.md")
            matches = glob.glob(pattern)
            meals = {}
            if matches:
                with open(matches[0], "r", encoding="utf-8") as f:
                    content = f.read()
                # Ayet bloklarını yakala: ### [surah:ayah] ... **Meal:**\n(metin)
                ayah_blocks = re.findall(r'###\s*\[(\d+):(\d+)\][\s\S]*?\*\*Meal:\*\*\s*\n(.*?)(?=\n\s*---|###|\Z)', content, re.DOTALL)
                for s, a, m in ayah_blocks:
                    meals[(int(s), int(a))] = m.strip()
            self._sure_meals_cache[surah_num] = meals

        return self._sure_meals_cache[surah_num].get((surah_num, ayah_num), "")

    def generate_annotation_prompt(self, surah_num, ayah_num, arabic_text, meal_text):
        return f"""Aşağıdaki Kur'an-ı Kerim ayetini ({surah_num}:{ayah_num}) analiz et ve yalnızca belirtilen JSON formatında yanıt ver.

Arapça Metin: {arabic_text}
Türkçe Meali: {meal_text}

Kullanabileceğin Sabit Temalar Listesi:
{json.dumps(CANONICAL_THEMES, ensure_ascii=False)}

Gereken JSON Şeması:
{{
  "themes": ["en_fazla_3_tane_tema_listeden"],
  "speech_act": "dua | emir | nehiy | haber | kıssa | soru",
  "sentiment": -1.0_ile_1.0_arasi_skor,
  "addressee": "müminler | kafirler | tüm_insanlar | peygamber | genel",
  "entities": [
    {{"type": "peygamber | kavim | mekan", "name": "Varlık Adı"}}
  ]
}}
"""

    def annotate_ayah(self, surah_num, ayah_num, models=None, dry_run=False):
        """
        Bir ayeti 3 modelle sorgular, oylamayı yapar, konsensüsü ve varlıkları veritabanına yazar.
        """
        arabic_text = self.db.get_ayah_text(surah_num, ayah_num)
        meal_text = self.get_ayah_meal(surah_num, ayah_num)
        
        if models is None:
            models = ModelRouter.get_models_for_task('triangulated_annotation')

        prompt = self.generate_annotation_prompt(surah_num, ayah_num, arabic_text, meal_text)
        messages = [{'role': 'user', 'content': prompt}]

        model_results = []
        all_entities = []

        for model in models:
            if dry_run:
                # Yalnızca açıkça istenirse: kural tabanlı simülasyon, gerçek veriyle karışmasın diye etiketlenir
                sim_res = self._simulate_annotation(surah_num, ayah_num, arabic_text, meal_text, 'SIMULATION')
                model_results.append(sim_res)
                all_entities.extend(sim_res.get('entities', []))
                continue
            if not self.client.is_configured():
                raise ValueError("API anahtarı yok. Simülasyon için dry_run=True kullanın.")
            # Hatalar yukarı fırlatılır; sahte etiket üretilmez
            parsed, _ = self.client.chat_json(model=model, messages=messages, temperature=0.0)
            parsed['model'] = model
            model_results.append(parsed)
            all_entities.extend(parsed.get('entities', []))

        # Ham modellerin yanıtlarını kaydet
        for r in model_results:
            self.db.save_ayah_annotation(
                surah=surah_num,
                ayah=ayah_num,
                model=r.get('model', 'unknown'),
                themes=r.get('themes', []),
                speech_act=r.get('speech_act', ''),
                sentiment=float(r.get('sentiment', 0.0)),
                addressee=r.get('addressee', '')
            )

        # Çoğunluk konsensüsünü hesapla (en az 2/3 oy alan temalar)
        consensus = AgreementEngine.calculate_majority_consensus(model_results)
        self.db.save_consensus_annotation(
            surah=surah_num,
            ayah=ayah_num,
            consensus_themes=consensus['consensus_themes'],
            agreement_score=consensus['agreement_score'],
            speech_act=consensus['majority_speech_act'],
            sentiment=consensus['avg_sentiment']
        )

        # Varlıkları kaydet (Tekilleştirilmiş)
        seen_entities = set()
        for ent in all_entities:
            ename = ent.get('name', '').strip()
            etype = ent.get('type', '').strip()
            if ename and (ename, etype) not in seen_entities:
                seen_entities.add((ename, etype))
                self.db.save_entity(surah_num, ayah_num, etype, ename, model="consensus")

        return {
            'surah': surah_num,
            'ayah': ayah_num,
            'models_used': models,
            'consensus_themes': consensus['consensus_themes'],
            'agreement_score': consensus['agreement_score'],
            'speech_act': consensus['majority_speech_act'],
            'sentiment': consensus['avg_sentiment'],
            'entities': list(seen_entities)
        }

    def _simulate_annotation(self, surah_num, ayah_num, arabic_text, meal_text, model_name):
        """API anahtarı olmayan ortamlarda veya testlerde deterministik kural tabanlı simülasyon."""
        themes = []
        entities = []
        speech_act = "haber"
        sentiment = 0.0

        meal_lower = meal_text.lower()
        if "allah" in meal_lower or "rab" in meal_lower:
            themes.append("tevhid")
        if "cennet" in meal_lower:
            themes.append("cennet")
            sentiment += 0.5
        if "cehennem" in meal_lower or "azap" in meal_lower:
            themes.append("azap")
            sentiment -= 0.5
        if "namaz" in meal_lower:
            themes.append("namaz")
            themes.append("ibadet")
        if "dua" in meal_lower or "bizi ilet" in meal_lower:
            themes.append("dua")
            speech_act = "dua"
        if "musa" in meal_lower:
            entities.append({'type': 'peygamber', 'name': 'Musa'})
            themes.append("kıssa")
        if "firavun" in meal_lower:
            entities.append({'type': 'kavim', 'name': 'Firavun'})

        if not themes:
            themes = ["hidayet"]

        return {
            'model': model_name,
            'themes': themes[:3],
            'speech_act': speech_act,
            'sentiment': sentiment,
            'addressee': 'müminler',
            'entities': entities
        }
