#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Modeller Arası Uyum ve Konsensüs Motoru (Inter-Annotator Agreement & Consensus)
Farklı LLM'lerin ayetler üzerine ürettiği etiketlerin tutarlılığını ölçer
(Fleiss' Kappa / Krippendorff's Alpha) ve en az 2/3 oy çokluğu kuralını uygular.
"""

import collections
import math

class AgreementEngine:
    @staticmethod
    def calculate_majority_consensus(model_annotations, min_agreement_ratio=0.66):
        """
        model_annotations: [
            {'model': 'model1', 'themes': ['tevhid', 'dua'], 'sentiment': 0.5, 'speech_act': 'dua'},
            {'model': 'model2', 'themes': ['tevhid', 'ahiret'], 'sentiment': 0.4, 'speech_act': 'dua'},
            {'model': 'model3', 'themes': ['tevhid', 'dua'], 'sentiment': 0.6, 'speech_act': 'emir'}
        ]
        Dönen: Konsensüs temaları (en az 2/3 alanlar), ortalama duygu ve en yaygın konuşma eylemi.
        """
        n_models = len(model_annotations)
        if n_models == 0:
            return {'consensus_themes': [], 'agreement_score': 0.0, 'sentiment': 0.0, 'speech_act': ''}

        # 1. Tema Oylaması
        theme_votes = collections.Counter()
        for ann in model_annotations:
            for t in ann.get('themes', []):
                theme_votes[t.strip().lower()] += 1

        required_votes = math.ceil(n_models * min_agreement_ratio)
        consensus_themes = [t for t, v in theme_votes.items() if v >= required_votes]

        # 2. Ortalama Duygu Skoru
        sentiments = [ann.get('sentiment', 0.0) for ann in model_annotations if 'sentiment' in ann]
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0.0

        # 3. Konuşma Eylemi Çoğunluğu
        speech_votes = collections.Counter(ann.get('speech_act', '') for ann in model_annotations if ann.get('speech_act'))
        majority_speech = speech_votes.most_common(1)[0][0] if speech_votes else ""

        # Uyum Skoru (Toplam oyların oybirliğine oranı)
        total_possible_unanimous = len(theme_votes) * n_models
        total_actual_votes = sum(theme_votes.values())
        agreement_score = total_actual_votes / total_possible_unanimous if total_possible_unanimous > 0 else 1.0

        return {
            'consensus_themes': sorted(consensus_themes),
            'agreement_score': round(agreement_score, 4),
            'avg_sentiment': round(avg_sentiment, 3),
            'majority_speech_act': majority_speech,
            'rejected_themes': [t for t, v in theme_votes.items() if v < required_votes],
            'n_models_participated': n_models
        }

    @staticmethod
    def fleiss_kappa(ratings_matrix):
        """
        ratings_matrix: N x k matrisi.
        N: Ayet (veya karar) sayısı
        k: Kategori sayısı.
        ratings_matrix[i][j]: i. ayete j. kategoriyi veren model sayısı.
        """
        N = len(ratings_matrix)
        if N == 0:
            return 1.0
        k = len(ratings_matrix[0])
        n = sum(ratings_matrix[0]) # her ayete oy veren model sayısı

        if n <= 1:
            return 1.0

        # p_j: Her kategorinin genel seçilme oranı
        p_j = [0.0] * k
        for j in range(k):
            p_j[j] = sum(ratings_matrix[i][j] for i in range(N)) / (N * n)

        # P_e: Rastlantısal beklenen örtüşme
        P_e = sum(pj ** 2 for pj in p_j)
        if P_e >= 1.0:
            return 1.0

        # P_i: i. ayet için gözlenen örtüşme
        P_obs_sum = 0.0
        for i in range(N):
            row_sum = sum(ratings_matrix[i][j] ** 2 for j in range(k))
            P_i = (row_sum - n) / (n * (n - 1))
            P_obs_sum += P_i

        P_obs = P_obs_sum / N

        kappa = (P_obs - P_e) / (1.0 - P_e) if (1.0 - P_e) != 0 else 1.0
        return round(kappa, 4)
