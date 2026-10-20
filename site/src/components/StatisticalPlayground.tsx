"use client";

import React, { useState, useMemo } from "react";
import { Calculator, Play, Sparkles, Scale, CheckCircle2, AlertTriangle, HelpCircle } from "lucide-react";
import { computeParityStats } from "../lib/stats";

export default function StatisticalPlayground() {
  const [c1, setC1] = useState<number>(115);
  const [c2, setC2] = useState<number>(115);
  const [margin, setMargin] = useState<number>(0.05);

  const stats = useMemo(() => {
    return computeParityStats(Number(c1) || 0, Number(c2) || 0, margin);
  }, [c1, c2, margin]);

  const setPreset = (v1: number, v2: number) => {
    setC1(v1);
    setC2(v2);
  };

  return (
    <section className="py-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8 pb-6 border-b border-slate-800">
        <div className="flex items-center space-x-2 text-cyan-400 text-xs font-bold uppercase tracking-wider mb-2">
          <Calculator className="w-4 h-4" />
          <span>İnteraktif Laboratuvar Aracı</span>
        </div>
        <h2 className="text-3xl font-extrabold text-white tracking-tight">
          Canlı İstatistiki Hesaplayıcı
        </h2>
        <p className="text-sm text-slate-400 mt-1 max-w-2xl">
          Herhangi iki kelime veya kök frekansı girerek iki-yönlü Z-skorunu, biyoistatistiki TOST denkliğini ve Noktasal Bayes Faktörünü (BF₀₁) anında hesaplayın.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left: Input Form */}
        <div className="lg:col-span-5 mirat-glass p-6 rounded-2xl border border-slate-800 space-y-5">
          <h3 className="text-base font-bold text-white flex items-center space-x-2">
            <span>Frekans Değerlerini Girin</span>
          </h3>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="text-xs text-slate-400 block mb-1.5 font-medium">
                1. Kavram / Kök Sayısı:
              </label>
              <input
                type="number"
                min="0"
                value={c1}
                onChange={(e) => setC1(Math.max(0, parseInt(e.target.value) || 0))}
                className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white font-mono font-bold text-base focus:outline-none focus:border-cyan-500"
              />
            </div>

            <div>
              <label className="text-xs text-slate-400 block mb-1.5 font-medium">
                2. Kavram / Kök Sayısı:
              </label>
              <input
                type="number"
                min="0"
                value={c2}
                onChange={(e) => setC2(Math.max(0, parseInt(e.target.value) || 0))}
                className="w-full px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-700 text-white font-mono font-bold text-base focus:outline-none focus:border-cyan-500"
              />
            </div>
          </div>

          <div>
            <div className="flex justify-between text-xs text-slate-400 mb-1.5">
              <span>TOST Biyoistatistiki Denklik Marjı:</span>
              <strong className="text-cyan-400 font-mono">%{Math.round(margin * 100)}</strong>
            </div>
            <input
              type="range"
              min="0.01"
              max="0.15"
              step="0.01"
              value={margin}
              onChange={(e) => setMargin(parseFloat(e.target.value))}
              className="w-full accent-cyan-500 cursor-pointer"
            />
            <span className="text-[11px] text-slate-500 block mt-1">
              Klinik araştırmalarda standart marj %5'tir (±0.05).
            </span>
          </div>

          {/* Quick Presets */}
          <div className="pt-2">
            <span className="text-xs text-slate-400 font-semibold block mb-2">Hızlı Örnekler:</span>
            <div className="flex flex-wrap gap-2 text-xs">
              <button
                onClick={() => setPreset(115, 115)}
                className="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800"
              >
                Dünya / Ahiret (115, 115)
              </button>
              <button
                onClick={() => setPreset(88, 88)}
                className="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800"
              >
                Melek / Şeytan (88, 88)
              </button>
              <button
                onClick={() => setPreset(24, 24)}
                className="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800"
              >
                Zina / İffet (24, 24)
              </button>
              <button
                onClick={() => setPreset(145, 140)}
                className="px-2.5 py-1 rounded-lg bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800"
              >
                Yakın Eşitlik (145, 140)
              </button>
            </div>
          </div>
        </div>

        {/* Right: Results Engine */}
        <div className="lg:col-span-7 mirat-glass p-6 rounded-2xl border border-slate-800 flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between pb-4 mb-4 border-b border-slate-800">
              <h3 className="text-base font-bold text-white">İstatistiki Değerlendirme Çıktısı</h3>
              <span className="text-xs font-mono text-slate-400">Toplam Gözlem: {stats.total}</span>
            </div>

            {/* Verdict Box */}
            <div className="p-4 rounded-xl bg-slate-950/80 border border-slate-800 mb-5">
              <span className="text-[11px] uppercase font-bold text-slate-400 block mb-1">
                Bilimsel Karar:
              </span>
              <p className="text-base font-extrabold text-amber-300">
                {stats.scientificVerdict}
              </p>
            </div>

            {/* Metric Grid */}
            <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs font-mono">
              <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800">
                <span className="text-slate-500 text-[11px] block">İki-Yönlü Z-Skoru:</span>
                <span className="text-base font-bold text-white">Z = {stats.zScore}</span>
                <span className="text-[10px] text-slate-400 block">p = {stats.pValue}</span>
              </div>

              <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800">
                <span className="text-slate-500 text-[11px] block">TOST %{Math.round(margin * 100)} Denkliği:</span>
                <span className={`text-base font-bold ${stats.tostEquivalent ? "text-emerald-400" : "text-amber-400"}`}>
                  {stats.tostEquivalent ? "DENK" : "DENK DEĞİL"}
                </span>
                <span className="text-[10px] text-slate-400 block">p = {stats.tostPValue}</span>
              </div>

              <div className="p-3 rounded-lg bg-slate-900/60 border border-slate-800">
                <span className="text-slate-500 text-[11px] block">Bayes Faktörü (BF01):</span>
                <span className="text-base font-bold text-cyan-400">
                  {stats.bayesFactorBF01 > 9999 ? ">9999" : stats.bayesFactorBF01}
                </span>
                <span className="text-[10px] text-slate-400 block">H0 / H1 Oranı</span>
              </div>
            </div>

            {/* Bayes Interpretation */}
            <div className="mt-4 p-3 rounded-lg bg-slate-900/40 border border-slate-800 text-xs text-slate-300">
              <span className="text-slate-400 block font-semibold mb-0.5">Jeffreys Bayesyen Kanıt Ölçeği:</span>
              <p className="text-emerald-400 font-medium">
                {stats.bayesInterpretation}
              </p>
            </div>
          </div>

          {/* Context footer */}
          <div className="mt-6 pt-3 border-t border-slate-800/80 text-[11px] text-slate-400">
            💡 <strong>Sıfır Modeli Notu:</strong> Kur'an külliyatında frekansı ≥20 olan tüm kökler arasında rastgele seçilen iki kökün tam eşit frekansa sahip olma baz şansı <strong>%{stats.baseRateChance}</strong>'dir.
          </div>
        </div>
      </div>
    </section>
  );
}

