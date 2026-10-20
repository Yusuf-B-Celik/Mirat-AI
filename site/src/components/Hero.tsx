"use client";

import React from "react";
import { Sparkles, BarChart3, ShieldCheck, ArrowRight, BookOpen, Layers, CheckCircle2 } from "lucide-react";

interface HeroProps {
  onExplore: (tab: string) => void;
}

export default function Hero({ onExplore }: HeroProps) {
  const metrics = [
    {
      value: "130.030",
      label: "Morfolojik Segment",
      sub: "Şahıs, sayı, çatı, zaman, VF babları",
      color: "border-cyan-500/30 text-cyan-400 bg-cyan-950/20",
    },
    {
      value: "219",
      label: "Bağımsız Bulgu",
      sub: "102 Anlamlı | 75 Dürüst Negatif",
      color: "border-amber-500/30 text-amber-300 bg-amber-950/20",
    },
    {
      value: "9",
      label: "Yeni Keşif Motoru",
      sub: "Kategori 11–19 (Kronoloji, Belâgat...)",
      color: "border-indigo-500/30 text-indigo-300 bg-indigo-950/20",
    },
    {
      value: "114",
      label: "Sure Dalga Formu",
      sub: "Nüzul sırası & Welch kırılma analizi",
      color: "border-emerald-500/30 text-emerald-300 bg-emerald-950/20",
    },
    {
      value: "κ = 0.88",
      label: "Çift-Modelli Konsensüs",
      sub: "DeepSeek-V4.1 & Qwen-3.7 Uzlaşması",
      color: "border-purple-500/30 text-purple-300 bg-purple-950/20",
    },
    {
      value: "52 / 52",
      label: "Doğrulama Testi",
      sub: "%100 Başarı | Sıfır Halüsinasyon",
      color: "border-teal-500/30 text-teal-300 bg-teal-950/20",
    },
  ];

  return (
    <section className="relative pt-12 pb-16 overflow-hidden">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center relative z-10">
        {/* Top Badge */}
        <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-slate-900/80 border border-slate-700/80 text-xs text-slate-300 mb-6 shadow-inner">
          <span className="flex h-2 w-2 relative">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-cyan-500"></span>
          </span>
          <span className="font-semibold text-slate-200">Hakemli Akademik Düzeyde Metin Madenciliği</span>
          <span className="text-slate-500">•</span>
          <span className="text-amber-400 font-medium">Doğrulanabilir Yapay Zekâ</span>
        </div>

        {/* Headline */}
        <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight text-white max-w-5xl mx-auto leading-tight sm:leading-tight">
          Kutsal Metinlerin Dış Dünyaya ve Matematiğe Tuttuğu{" "}
          <span className="bg-gradient-to-r from-amber-300 via-amber-400 to-amber-500 bg-clip-text text-transparent">
            Objektif Ayna
          </span>
        </h1>

        {/* Subtitle */}
        <p className="mt-6 text-base sm:text-lg text-slate-300 max-w-3xl mx-auto font-normal leading-relaxed">
          Apolojetik seçici sayımların (<span className="text-amber-300/90 italic">cherry-picking</span>) ötesinde;{" "}
          <strong className="text-white font-semibold">130.030 morfolojik segment</strong>, katı Monte Carlo sıfır modelleri,
          Benjamini-Hochberg FDR düzeltmesi ve çift-modelli LLM konsensüsü ile çalışan bilimsel keşif platformu.
        </p>

        {/* Action Buttons */}
        <div className="mt-8 flex flex-wrap items-center justify-center gap-3 sm:gap-4">
          <button
            onClick={() => onExplore("kesifler")}
            className="flex items-center space-x-2 px-6 py-3 rounded-xl bg-gradient-to-r from-cyan-500 to-cyan-600 hover:from-cyan-400 hover:to-cyan-500 text-slate-950 font-bold text-sm shadow-glowCyan transition-all duration-200 transform hover:-translate-y-0.5"
          >
            <Sparkles className="w-4 h-4" />
            <span>219 Keşfi İncele</span>
            <ArrowRight className="w-4 h-4 ml-1" />
          </button>

          <button
            onClick={() => onExplore("laboratuvar")}
            className="flex items-center space-x-2 px-5 py-3 rounded-xl bg-slate-900/90 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold text-sm transition-all duration-200"
          >
            <BarChart3 className="w-4 h-4 text-amber-400" />
            <span>114 Sure Dalgasını Gör</span>
          </button>

          <button
            onClick={() => onExplore("denetci")}
            className="flex items-center space-x-2 px-5 py-3 rounded-xl bg-slate-900/90 hover:bg-slate-800 text-slate-200 border border-slate-700 font-semibold text-sm transition-all duration-200"
          >
            <ShieldCheck className="w-4 h-4 text-emerald-400" />
            <span>İddia Denetçisi (FDR & TOST)</span>
          </button>
        </div>

        {/* 6 Metrics Grid */}
        <div className="mt-14 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 sm:gap-4 text-left">
          {metrics.map((m, idx) => (
            <div
              key={idx}
              className={`p-4 rounded-xl mirat-glass border ${m.color} mirat-glass-hover flex flex-col justify-between`}
            >
              <div>
                <span className="text-xs uppercase tracking-wider font-semibold opacity-70 block mb-1">
                  {m.label}
                </span>
                <span className="text-xl sm:text-2xl font-extrabold tracking-tight block">
                  {m.value}
                </span>
              </div>
              <p className="text-[11px] text-slate-400 mt-2 font-normal leading-tight">
                {m.sub}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

