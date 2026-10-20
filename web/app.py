#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT v5.0 Canlı Jüri ve Araştırma Paneli (FastAPI Web Application)
Bilimsel İddia Denetimi, Otonom Hipotez Ajanı, Ayet Dalga Formu,
Kaynak Doğrulamalı RAG ve OpenCode GO Kota Takibini tek bir interaktif arayüzde sunar.
"""

import json
import os
import sys
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel

# Proje kökünü sys.path'e ekle
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, os.path.join(PROJECT_ROOT, "scripts"))

from mirat.database import MiratDB
from mirat.claim_registry import ClaimRegistry
from mirat.null_models import MiratNullModel
from mirat.llm.budget import BudgetManager
from mirat.agent.hypothesis_agent import HypothesisAgent
from mirat.rag.qa import MiratQA
from mirat.advanced_structural_engine import AdvancedStructuralEngine

app = FastAPI(
    title="MİRAT v5.0 Araştırma ve Jüri Paneli",
    description="Doğrulanabilir Yapay Zekâ, Çok Modelli Denetçi ve Kur'an Metin Madenciliği Platformu",
    version="5.0.0"
)

db = MiratDB()
registry = ClaimRegistry(db)
null_model = MiratNullModel(db)
budget_manager = BudgetManager()
agent = HypothesisAgent(db)
qa_engine = MiratQA(db)
structural_engine = AdvancedStructuralEngine(db)

# -------------------------------------------------------------
# API ENDPOINT'LERİ
# -------------------------------------------------------------

@app.get("/api/audit")
def get_claims_audit():
    """Tüm iddiaların FDR, TOST, Bayes Faktörü ve Sıfır Modeli denetim tablosunu döner."""
    return registry.run_full_audit()

@app.get("/api/null-models")
def get_null_model_stats():
    """Rastlantısal kök eşitlik baz oranı ve 114 sure ayet dalgası permütasyon testini döner."""
    from build_quran_markdown import SURAH_METADATA
    v_counts = [SURAH_METADATA[s]['verses'] for s in range(1, 115)]
    base_rate = null_model.get_equal_frequency_base_rate(min_freq=20)
    waveform_res = null_model.test_waveform_peak_significance(v_counts, n_permutations=2000)
    return {
        'base_rate': base_rate,
        'waveform_permutation': waveform_res,
        'verse_counts': v_counts
    }

@app.get("/api/budget")
def get_llm_budget():
    """OpenCode GO model limitleri, harcama ve kalan istek kotalarını döner."""
    return budget_manager.get_full_budget_report()

class AgentRequest(BaseModel):
    domain: str = "etik ve teoloji"
    n: int = 2

@app.post("/api/agent/run")
def run_agent_cycle(req: AgentRequest):
    """Otonom hipotez üretici, eleştirmen ve deterministik test döngüsünü çalıştırır."""
    return agent.run_discovery_cycle(domain=req.domain, n=req.n)

class QARequest(BaseModel):
    query: str

@app.post("/api/qa")
def ask_question(req: QARequest):
    """Kaynak doğrulamalı (halüsinasyonsuz) soru-cevap motorunu çalıştırır."""
    return qa_engine.answer_question(req.query)

@app.get("/api/preregistration")
def get_preregistration_status():
    """Ön-kayıt defteri bütünlüğünü ve hash zincirini döner."""
    return ClaimRegistry.verify_preregistration_chain()

@app.get("/api/findings")
def get_findings_api(category: str = None):
    """MİRAT v6 Keşif motorlarının bulgularını döner."""
    from mirat.discovery.runner import load_findings, run_all
    data = load_findings()
    if not data:
        data = run_all(categories=[11, 12, 13, 14, 17, 18, 19], verbose=False)
    if category and category in data.get("categories", {}):
        return {"generated_at": data["generated_at"], "categories": {category: data["categories"][category]}}
    return data

# -------------------------------------------------------------
# WEB ARAYÜZÜ (SINGLE PAGE APPLICATION)
# -------------------------------------------------------------

@app.get("/", response_class=HTMLResponse)
def index_page():
    html_content = """<!DOCTYPE html>
<html lang="tr" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MİRAT v6.0 | Bilimsel Araştırma ve Keşif Paneli</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        gold: '#d4af37',
                        cyanAccent: '#00f0ff',
                        darkBg: '#0b0f19',
                        darkCard: '#131b2e',
                        darkBorder: '#1f293d'
                    }
                }
            }
        }
    </script>
    <style>
        body { background-color: #0b0f19; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
        .tab-btn.active { border-bottom: 3px solid #00f0ff; color: #00f0ff; font-weight: 600; }
    </style>
</head>
<body class="text-gray-200 min-h-screen">
    <!-- Üst Bar -->
    <header class="border-b border-darkBorder bg-darkCard/80 backdrop-blur sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <span class="text-3xl">🏛️</span>
                <div>
                    <h1 class="text-xl font-bold tracking-tight text-white flex items-center gap-2">
                        MİRAT <span class="text-xs bg-cyanAccent/20 text-cyanAccent px-2 py-0.5 rounded border border-cyanAccent/40">v5.0 Bilimsel Doğrulama</span>
                    </h1>
                    <p class="text-xs text-gray-400">Doğrulanabilir Yapay Zekâ, Çok Modelli Denetçi & Ön-Kayıt Defteri</p>
                </div>
            </div>
            <div class="flex items-center space-x-4">
                <div class="text-right text-xs">
                    <span class="text-green-400 font-semibold flex items-center justify-end gap-1">
                        <span class="w-2 h-2 rounded-full bg-green-500 animate-pulse"></span> Çekirdek Aktif
                    </span>
                    <span class="text-gray-400">SQLite (130k Segment)</span>
                </div>
            </div>
        </div>
        <!-- Sekmeler -->
        <nav class="max-w-7xl mx-auto px-6 flex space-x-8 text-sm">
            <button onclick="switchTab('audit')" id="tab-audit" class="tab-btn py-3 active">🛡️ İddia Denetçisi (Audit)</button>
            <button onclick="switchTab('agent')" id="tab-agent" class="tab-btn py-3 text-gray-400 hover:text-white">🤖 Otonom Hipotez Ajanı</button>
            <button onclick="switchTab('waveform')" id="tab-waveform" class="tab-btn py-3 text-gray-400 hover:text-white">📈 Dalga & Sıfır Modeli</button>
            <button onclick="switchTab('qa')" id="tab-qa" class="tab-btn py-3 text-gray-400 hover:text-white">💬 Kaynaklı Soru-Cevap (RAG)</button>
            <button onclick="switchTab('budget')" id="tab-budget" class="tab-btn py-3 text-gray-400 hover:text-white">💳 OpenCode GO Kota Paneli</button>
            <button onclick="switchTab('discover')" id="tab-discover" class="tab-btn py-3 text-gray-400 hover:text-white">🔬 v6 Keşif Kataloğu</button>
        </nav>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8">
        <!-- 1. İDDİA DENETÇİSİ SEKMESİ -->
        <section id="sec-audit" class="space-y-6">
            <div class="bg-darkCard p-6 rounded-xl border border-darkBorder shadow-lg">
                <div class="flex justify-between items-start mb-4">
                    <div>
                        <h2 class="text-lg font-bold text-white flex items-center gap-2">
                            <span>🛡️</span> Bilimsel İddia Denetimi ve Çoklu Test Düzeltmesi (FDR & Bayes)
                        </h2>
                        <p class="text-sm text-gray-400 mt-1">
                            Bu panel, metindeki popüler iddiaları "seçici algı" veya "p-hacking" tuzaklarına düşmeden 
                            <strong>Benjamini-Hochberg FDR</strong>, <strong>TOST Denklik</strong> ve <strong>Bayes Faktörü (BF₀₁)</strong> ile tarafsızca sınar.
                        </p>
                    </div>
                    <span id="base-rate-badge" class="bg-yellow-500/10 text-yellow-400 border border-yellow-500/30 text-xs px-3 py-1.5 rounded-full font-mono">
                        Yükleniyor...
                    </span>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left text-sm">
                        <thead class="bg-darkBg/60 text-xs text-gray-400 uppercase border-b border-darkBorder">
                            <tr>
                                <th class="p-3">İddia / Kavram Çifti</th>
                                <th class="p-3">Kategori</th>
                                <th class="p-3 text-center">Frekanslar</th>
                                <th class="p-3">Bayes BF₀₁</th>
                                <th class="p-3">FDR q-Değeri</th>
                                <th class="p-3">Bilimsel Sınıflandırma</th>
                                <th class="p-3">Morfolojik Filtre Notu</th>
                            </tr>
                        </thead>
                        <tbody id="claims-table-body" class="divide-y divide-darkBorder">
                            <tr><td colspan="7" class="p-4 text-center text-gray-500">Yükleniyor...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- 2. OTONOM HİPOTEZ AJANI SEKMESİ -->
        <section id="sec-agent" class="hidden space-y-6">
            <div class="bg-darkCard p-6 rounded-xl border border-darkBorder">
                <h2 class="text-lg font-bold text-white flex items-center gap-2 mb-2">
                    <span>🤖</span> Çok Modelli Hipotez Keşif ve Ön-Kayıt Ajanı
                </h2>
                <p class="text-sm text-gray-400 mb-6">
                    Ajan döngüsü: <strong>Önerici (GPT 6 Luna)</strong> hipotez kurar ➔ <strong>Eleştirmen (GLM)</strong> filtre taraflılığını denetler ➔ <strong>Ön-Kayıt Defteri</strong> SHA-256 hash'ler ➔ <strong>Deterministik SQLite Çekirdeği</strong> sayar ve karar verir.
                </p>
                <div class="flex gap-4 mb-6">
                    <input type="text" id="agent-domain" value="etik ve adalet dengeleri" class="bg-darkBg border border-darkBorder rounded-lg px-4 py-2 flex-1 text-sm focus:outline-none focus:border-cyanAccent" placeholder="Araştırma Alanı (örn: tabiat, kıyamet, infak)">
                    <button onclick="runAgent()" id="btn-run-agent" class="bg-cyanAccent hover:bg-cyan-400 text-darkBg font-bold px-6 py-2 rounded-lg text-sm transition">
                        Döngüyü Çalıştır
                    </button>
                </div>

                <div id="agent-results" class="space-y-4">
                    <div class="text-center text-gray-500 py-8 border border-dashed border-darkBorder rounded-lg">
                        Döngüyü başlatmak için yukarıdaki butona tıklayın.
                    </div>
                </div>
            </div>
        </section>

        <!-- 3. DALGA VE SIFIR MODELİ SEKMESİ -->
        <section id="sec-waveform" class="hidden space-y-6">
            <div class="bg-darkCard p-6 rounded-xl border border-darkBorder">
                <div class="flex justify-between items-start mb-4">
                    <div>
                        <h2 class="text-lg font-bold text-white flex items-center gap-2">
                            <span>📈</span> 114 Sure Ayet Sayıları Dalga Formu ve Monte Carlo Permütasyonu
                        </h2>
                        <p class="text-sm text-gray-400 mt-1">
                            114 surenin ayet sayıları dizisindeki tepe noktaları (2. Bakara, 7. A'raf, 26. Şuarâ, 37. Sâffât) rastgele permütasyonlarla sınanmıştır.
                        </p>
                    </div>
                    <div id="waveform-stat-box" class="text-right text-xs bg-darkBg p-3 rounded border border-darkBorder font-mono">
                        Yükleniyor...
                    </div>
                </div>
                <div class="h-80 w-full mb-4">
                    <canvas id="waveformChart"></canvas>
                </div>
            </div>
        </section>

        <!-- 4. KAYNAK DOĞRULAMALI RAG SEKMESİ -->
        <section id="sec-qa" class="hidden space-y-6">
            <div class="bg-darkCard p-6 rounded-xl border border-darkBorder">
                <h2 class="text-lg font-bold text-white flex items-center gap-2 mb-2">
                    <span>💬</span> Kaynak Doğrulamalı Soru-Cevap (Halüsinasyonsuz RAG)
                </h2>
                <p class="text-sm text-gray-400 mb-6">
                    Sayısal sorular doğrudan <strong>SQL Motoru</strong> tarafından sıfır hata ile çözülür; kavramsal sorularda üretilen her [sure:ayet] atfı SQLite indeksinde anlık doğrulanır.
                </p>
                <div class="flex gap-4 mb-6">
                    <input type="text" id="qa-input" value="Kur'an'da deniz kelimesi kaç kez geçer?" class="bg-darkBg border border-darkBorder rounded-lg px-4 py-2 flex-1 text-sm focus:outline-none focus:border-cyanAccent" placeholder="Sorunuzu buraya yazın...">
                    <button onclick="askQuestion()" id="btn-qa" class="bg-cyanAccent hover:bg-cyan-400 text-darkBg font-bold px-6 py-2 rounded-lg text-sm transition">
                        Soruyu Yanıtla
                    </button>
                </div>
                <div id="qa-output" class="bg-darkBg p-6 rounded-xl border border-darkBorder min-h-[140px] text-sm">
                    <span class="text-gray-500">Yanıt burada görüntülenecek...</span>
                </div>
            </div>
        </section>

        <!-- 5. KOTA VE MODEL SEKMESİ -->
        <section id="sec-budget" class="hidden space-y-6">
            <div class="bg-darkCard p-6 rounded-xl border border-darkBorder">
                <h2 class="text-lg font-bold text-white flex items-center gap-2 mb-2">
                    <span>💳</span> OpenCode GO Model Kota ve Harcama İzleme (Sarı Sınırlar)
                </h2>
                <p class="text-sm text-gray-400 mb-6">
                    API kotalarınız yerel SQLite sayaçlarıyla her istek öncesinde denetlenir; limit aşımı durumunda otomatik olarak ücretsiz veya yedek modele yönlenir.
                </p>
                <div id="budget-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    <!-- Dinamik Model Kartları -->
                </div>
            </div>
        </section>

        <!-- 6. v6 KEŞİFLER SEKMESİ -->
        <section id="sec-discover" class="hidden space-y-6">
            <div class="bg-darkCard p-6 rounded-xl border border-darkBorder shadow-lg">
                <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 mb-6">
                    <div>
                        <h3 class="text-xl font-bold text-white flex items-center gap-2">
                            🔬 MİRAT v6 Keşif Kataloğu
                            <span class="text-xs bg-cyanAccent/20 text-cyanAccent border border-cyanAccent/30 px-2 py-0.5 rounded">9 Kategori · Çoklu Test</span>
                        </h3>
                        <p class="text-xs text-gray-400 mt-1">
                            Tüm sayımlar deterministik morfoloji çekirdeğinden. LLM yalnızca etiket (🤖) üretir. Negatif / anlamsız (⚪) sonuçlar da raporlanır.
                        </p>
                    </div>
                    <div class="flex items-center gap-3">
                        <select id="discover-cat-filter" onchange="renderDiscoverList()" class="bg-darkBg border border-darkBorder text-gray-200 text-xs rounded px-3 py-2">
                            <option value="all">Tüm Kategoriler (11-19)</option>
                        </select>
                        <input id="discover-search" type="text" oninput="renderDiscoverList()" placeholder="Bulgu ara..." class="bg-darkBg border border-darkBorder text-gray-200 text-xs rounded px-3 py-2 w-48 focus:border-cyanAccent outline-none" />
                    </div>
                </div>

                <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6 text-center text-xs">
                    <div class="bg-darkBg p-3 rounded border border-darkBorder">
                        <div class="text-gray-400">Toplam Bulgu</div>
                        <div id="stat-total-findings" class="text-lg font-bold text-white mt-1">-</div>
                    </div>
                    <div class="bg-darkBg p-3 rounded border border-darkBorder">
                        <div class="text-gray-400">Hipotez Testi</div>
                        <div id="stat-tested-findings" class="text-lg font-bold text-cyan-300 mt-1">-</div>
                    </div>
                    <div class="bg-darkBg p-3 rounded border border-darkBorder">
                        <div class="text-gray-400">Anlamlı (q&lt;0.05)</div>
                        <div id="stat-sig-findings" class="text-lg font-bold text-green-400 mt-1">-</div>
                    </div>
                    <div class="bg-darkBg p-3 rounded border border-darkBorder">
                        <div class="text-gray-400">Negatif / Anlamsız</div>
                        <div id="stat-null-findings" class="text-lg font-bold text-gray-300 mt-1">-</div>
                    </div>
                </div>

                <div id="discover-list" class="space-y-3">
                    <div class="text-center py-8 text-gray-500 text-sm">Keşifler yükleniyor...</div>
                </div>
            </div>
        </section>
    </main>

    <footer class="border-t border-darkBorder py-6 text-center text-xs text-gray-500">
        MİRAT AI v6.0 — Bilimsel İddia Denetimi, Çok Modelli Konsensüs ve Külliyat Platformu
    </footer>

    <script>
        function switchTab(tabId) {
            ['audit', 'agent', 'waveform', 'qa', 'budget', 'discover'].forEach(t => {
                document.getElementById('sec-' + t).classList.add('hidden');
                document.getElementById('tab-' + t).classList.remove('active', 'text-cyanAccent');
                document.getElementById('tab-' + t).classList.add('text-gray-400');
            });
            document.getElementById('sec-' + tabId).classList.remove('hidden');
            document.getElementById('tab-' + tabId).classList.add('active', 'text-cyanAccent');
            document.getElementById('tab-' + tabId).classList.remove('text-gray-400');

            if (tabId === 'waveform' && !window.waveformChartLoaded) {
                loadWaveform();
            }
            if (tabId === 'discover' && !window.discoverLoaded) {
                loadDiscover();
            }
        }

        // 1. Audit Verilerini Yükle
        async function loadAudit() {
            try {
                const res = await fetch('/api/audit');
                const data = await res.json();
                document.getElementById('base-rate-badge').innerHTML = 
                    `Kök Eşitlik Baz Oranı: %${data.base_rate_equal_pair_chance} (Rastgele Şans)`;

                const tbody = document.getElementById('claims-table-body');
                tbody.innerHTML = '';
                data.claims.forEach(c => {
                    let badgeClass = "bg-gray-500/20 text-gray-300 border-gray-500/30";
                    if (c.audit_tier.includes("Altın")) badgeClass = "bg-green-500/20 text-green-300 border-green-500/30";
                    else if (c.audit_tier.includes("Denk")) badgeClass = "bg-cyan-500/20 text-cyan-300 border-cyan-500/30";
                    else if (c.audit_tier.includes("Anlamlı")) badgeClass = "bg-blue-500/20 text-blue-300 border-blue-500/30";

                    tbody.innerHTML += `
                        <tr class="hover:bg-darkBg/30 transition">
                            <td class="p-3 font-semibold text-white">${c.title}</td>
                            <td class="p-3 text-gray-400">${c.category}</td>
                            <td class="p-3 text-center font-mono font-bold">${c.counts}</td>
                            <td class="p-3 font-mono text-xs">BF₀₁=${c.bayes_factor_bf01}</td>
                            <td class="p-3 font-mono text-xs">q=${c.q_value_fdr}</td>
                            <td class="p-3">
                                <span class="px-2 py-1 rounded text-xs border ${badgeClass}">
                                    ${c.audit_tier}
                                </span>
                            </td>
                            <td class="p-3 text-xs text-gray-400">${c.filter_notes}</td>
                        </tr>
                    `;
                });
            } catch (e) {
                console.error(e);
            }
        }

        // 2. Dalga Formunu Yükle
        async function loadWaveform() {
            try {
                const res = await fetch('/api/null-models');
                const data = await res.json();
                window.waveformChartLoaded = true;

                const wf = data.waveform_permutation;
                document.getElementById('waveform-stat-box').innerHTML = `
                    <div class="text-green-400 font-bold">Empirik p = ${wf.empirical_p_value}</div>
                    <div class="text-gray-400">Şaşırtıcılık: ${wf.surprise_bits} bit (${wf.n_permutations} perm.)</div>
                `;

                const labels = data.verse_counts.map((_, i) => (i + 1).toString());
                const ctx = document.getElementById('waveformChart').getContext('2d');
                new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Ayet Sayısı',
                            data: data.verse_counts,
                            borderColor: '#00f0ff',
                            backgroundColor: 'rgba(0, 240, 255, 0.1)',
                            borderWidth: 1.5,
                            fill: true,
                            tension: 0.2,
                            pointRadius: labels.map((_, i) => (wf.observed_peaks || []).includes(i + 1) ? 4 : 0),
                            pointBackgroundColor: '#d4af37'
                        }]
                    },
                    options: {
                        responsive: true,
                        maintainAspectRatio: false,
                        plugins: { legend: { display: false } },
                        scales: {
                            x: { grid: { color: '#1f293d' }, ticks: { color: '#64748b', maxTicksLimit: 20 } },
                            y: { grid: { color: '#1f293d' }, ticks: { color: '#64748b' } }
                        }
                    }
                });
            } catch (e) {
                console.error(e);
            }
        }

        // 3. Ajan Çalıştır
        async function runAgent() {
            const domain = document.getElementById('agent-domain').value;
            const btn = document.getElementById('btn-run-agent');
            const resDiv = document.getElementById('agent-results');
            btn.disabled = true;
            btn.innerText = "Döngü Sürüyor...";
            resDiv.innerHTML = '<div class="text-center py-6 text-cyanAccent animate-pulse">Ajan hipotez üretiyor, eleştirmen sınıyor ve SQLite sayıyor...</div>';

            try {
                const resp = await fetch('/api/agent/run', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ domain: domain, n: 2 })
                });
                const data = await resp.json();
                resDiv.innerHTML = '';
                data.cycle_results.forEach(item => {
                    const r = item.result;
                    const crit = r.critic_evaluation || {};
                    resDiv.innerHTML += `
                        <div class="bg-darkBg p-4 rounded-lg border border-darkBorder">
                            <div class="flex justify-between items-start">
                                <div>
                                    <h4 class="font-bold text-white">${r.name}</h4>
                                    <p class="text-xs text-gray-400 mt-1">Kökler: <strong>[${r.root1}]</strong> (${r.count1}) vs <strong>[${r.root2}]</strong> (${r.count2})</p>
                                </div>
                                <span class="text-xs px-2 py-1 rounded bg-cyanAccent/10 text-cyanAccent border border-cyanAccent/30">
                                    ${r.scientific_verdict}
                                </span>
                            </div>
                            <div class="mt-3 text-xs grid grid-cols-2 gap-2 text-gray-400 pt-2 border-t border-darkBorder">
                                <div>Bayes BF₀₁: <span class="font-mono text-white">${r.bayes_factor_bf01}</span></div>
                                <div>Eleştirmen: <span class="text-green-400">${crit.verdict || 'ONAY'}</span></div>
                                <div class="col-span-2 text-gray-500 font-mono truncate">Ön-Kayıt Hash: ${r.preregistration_hash}</div>
                            </div>
                        </div>
                    `;
                });
            } catch (e) {
                resDiv.innerHTML = '<div class="text-red-400">Hata oluştu: ' + e + '</div>';
            } finally {
                btn.disabled = false;
                btn.innerText = "Döngüyü Çalıştır";
            }
        }

        // 4. Soru-Cevap
        async function askQuestion() {
            const query = document.getElementById('qa-input').value;
            const btn = document.getElementById('btn-qa');
            const out = document.getElementById('qa-output');
            btn.disabled = true;
            btn.innerText = "Sorgulanıyor...";
            out.innerHTML = '<span class="text-cyanAccent animate-pulse">Ayetler taranıyor ve atıflar doğrulanıyor...</span>';

            try {
                const resp = await fetch('/api/qa', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ query: query })
                });
                const data = await resp.json();
                let auditBadge = "";
                if (data.citations_audit) {
                    const ca = data.citations_audit;
                    auditBadge = `
                        <div class="mt-4 pt-3 border-t border-darkBorder flex items-center gap-2 text-xs">
                            <span class="px-2 py-0.5 rounded ${ca.is_fully_grounded ? 'bg-green-500/20 text-green-300' : 'bg-red-500/20 text-red-300'}">
                                ${ca.is_fully_grounded ? '✓ %100 Doğrulanmış Atıf' : '⚠ Atıf Hatası Var'}
                            </span>
                            <span class="text-gray-400 font-mono">Doğrulanan: ${ca.verified_citations.join(', ') || 'Yok'}</span>
                        </div>
                    `;
                }

                out.innerHTML = `
                    <div class="text-white whitespace-pre-line leading-relaxed">${data.answer}</div>
                    ${auditBadge}
                `;
            } catch (e) {
                out.innerHTML = '<span class="text-red-400">Hata: ' + e + '</span>';
            } finally {
                btn.disabled = false;
                btn.innerText = "Soruyu Yanıtla";
            }
        }

        // 5. Bütçe Verilerini Yükle
        async function loadBudget() {
            try {
                const res = await fetch('/api/budget');
                const list = await res.json();
                const grid = document.getElementById('budget-grid');
                grid.innerHTML = '';
                list.forEach(m => {
                    const isInf = (m.monthly_limit_usd === '∞');
                    grid.innerHTML += `
                        <div class="bg-darkBg p-4 rounded-lg border border-darkBorder">
                            <div class="flex justify-between items-center mb-2">
                                <h4 class="font-bold text-white text-sm truncate" title="${m.model}">${m.model}</h4>
                                <span class="text-xs px-2 py-0.5 rounded bg-darkCard text-gray-300 border border-darkBorder">
                                    Aylık: $${m.monthly_limit_usd}
                                </span>
                            </div>
                            <div class="w-full bg-darkCard rounded-full h-2 mb-2 overflow-hidden">
                                <div class="bg-cyanAccent h-2 rounded-full" style="width: ${isInf ? 0 : Math.min(100, m.usage_percent_5h)}%"></div>
                            </div>
                            <div class="flex justify-between text-xs text-gray-400">
                                <span>İstek: ${m.requests_used} | Toplam $${m.cost_usd_total}</span>
                                <span>5s: $${m.spent_5h_usd} / $${m.cap_5h_usd}</span>
                            </div>
                        </div>
                    `;
                });
            } catch (e) {
                console.error(e);
            }
        }

        // 6. v6 Keşif Kataloğunu Yükle
        let discoverData = null;
        async function loadDiscover() {
            try {
                window.discoverLoaded = true;
                const res = await fetch('/api/findings');
                discoverData = await res.json();
                
                const sel = document.getElementById('discover-cat-filter');
                sel.innerHTML = '<option value="all">Tüm Kategoriler (11-19)</option>';
                const cats = discoverData.categories || {};
                Object.keys(cats).sort((a,b) => parseInt(a) - parseInt(b)).forEach(cid => {
                    sel.innerHTML += `<option value="${cid}">Kategori ${cid}: ${cats[cid].name}</option>`;
                });
                
                let total = 0, tested = 0, sig = 0;
                Object.values(cats).forEach(c => {
                    (c.findings || []).forEach(f => {
                        total++;
                        if (f.null_p !== null && f.null_p !== undefined) {
                            tested++;
                            if (f.q_value !== null && f.q_value < 0.05) sig++;
                        }
                    });
                });
                document.getElementById('stat-total-findings').innerText = total;
                document.getElementById('stat-tested-findings').innerText = tested;
                document.getElementById('stat-sig-findings').innerText = sig;
                document.getElementById('stat-null-findings').innerText = (tested - sig);

                renderDiscoverList();
            } catch (e) {
                console.error(e);
                document.getElementById('discover-list').innerHTML = `<div class="text-red-400 text-sm">Hata: ${e}</div>`;
            }
        }

        function renderDiscoverList() {
            if (!discoverData) return;
            const catFilter = document.getElementById('discover-cat-filter').value;
            const search = (document.getElementById('discover-search').value || '').toLowerCase();
            const list = document.getElementById('discover-list');
            list.innerHTML = '';
            
            const cats = discoverData.categories || {};
            let matchCount = 0;

            Object.keys(cats).sort((a,b) => parseInt(a) - parseInt(b)).forEach(cid => {
                if (catFilter !== 'all' && catFilter !== cid) return;
                const c = cats[cid];
                const findings = (c.findings || []).filter(f => {
                    if (!search) return true;
                    return (f.title || '').toLowerCase().includes(search) || 
                           (f.method || '').toLowerCase().includes(search) ||
                           (f.id || '').toLowerCase().includes(search);
                });
                if (findings.length === 0) return;

                let itemsHtml = '';
                findings.forEach(f => {
                    matchCount++;
                    const isSig = (f.q_value !== null && f.q_value < 0.05);
                    const isTested = (f.null_p !== null && f.null_p !== undefined);
                    let badge = isTested ? (isSig ? 
                        '<span class="bg-green-500/20 text-green-300 border border-green-500/30 text-xs px-2 py-0.5 rounded font-mono">✅ q=' + f.q_value.toFixed(4) + '</span>' :
                        '<span class="bg-gray-500/20 text-gray-300 border border-gray-500/30 text-xs px-2 py-0.5 rounded font-mono">⚪ q=' + (f.q_value !== null && f.q_value !== undefined ? f.q_value.toFixed(4) : '-') + '</span>') :
                        '<span class="bg-blue-500/20 text-blue-300 border border-blue-500/30 text-xs px-2 py-0.5 rounded">📋 Betimsel</span>';
                    if (f.llm_assisted) badge += ' <span class="bg-purple-500/20 text-purple-300 border border-purple-500/30 text-xs px-1.5 py-0.5 rounded">🤖 LLM</span>';
                    
                    let evHtml = '';
                    if (f.evidence && f.evidence.length > 0) {
                        evHtml = `
                            <details class="mt-2 text-xs text-gray-400">
                                <summary class="cursor-pointer text-cyanAccent hover:underline">Kanıt Listesi (${f.evidence.length})</summary>
                                <div class="mt-1 p-2 bg-darkCard rounded border border-darkBorder font-mono text-[11px] max-h-36 overflow-y-auto">
                                    ${f.evidence.map(e => `• ${e}`).join('<br>')}
                                </div>
                            </details>
                        `;
                    }

                    itemsHtml += `
                        <div class="bg-darkBg p-4 rounded-lg border border-darkBorder hover:border-gray-600 transition">
                            <div class="flex flex-col md:flex-row justify-between items-start md:items-center gap-2 mb-1.5">
                                <h4 class="font-bold text-white text-sm flex items-center gap-2">
                                    ${f.title}
                                </h4>
                                <div class="flex items-center gap-2 shrink-0">
                                    ${badge}
                                </div>
                            </div>
                            <div class="text-xs text-gray-300 mb-1">
                                <span class="text-gray-500">Yöntem:</span> ${f.method} · 
                                <span class="text-gray-500">Ölçüt:</span> <span class="font-mono text-cyan-300">${f.metric} = ${f.value}</span>
                                ${isTested ? ` · <span class="text-gray-500">p:</span> <span class="font-mono">${f.null_p.toFixed(4)}</span>` : ''}
                                ${f.effect_size !== null && f.effect_size !== undefined ? ` · <span class="text-gray-500">Etki:</span> <span class="font-mono">${typeof f.effect_size === 'number' ? f.effect_size.toFixed(2) : f.effect_size}</span>` : ''}
                            </div>
                            ${f.detail ? `<div class="text-xs text-gray-400 mt-1">${f.detail}</div>` : ''}
                            ${evHtml}
                        </div>
                    `;
                });

                list.innerHTML += `
                    <div class="mb-6">
                        <div class="text-sm font-bold text-cyanAccent uppercase tracking-wide mb-3 pb-1 border-b border-darkBorder flex justify-between">
                            <span>📂 Kategori ${cid}: ${c.name}</span>
                            <span class="text-xs text-gray-500 lowercase">${c.runtime_sec || 0}s</span>
                        </div>
                        <div class="space-y-3">
                            ${itemsHtml}
                        </div>
                    </div>
                `;
            });

            if (matchCount === 0) {
                list.innerHTML = '<div class="text-center py-8 text-gray-500 text-sm">Filtreye uygun bulgu bulunamadı.</div>';
            }
        }

        // İlk Yüklemeler
        loadAudit();
        loadBudget();
    </script>
</body>
</html>
"""
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
