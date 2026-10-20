"use client";

import React from "react";
import { BookOpen, ShieldCheck, CheckCircle2, AlertTriangle, Layers, Brain, Database } from "lucide-react";

export default function MethodologySection() {
  const principles = [
    {
      title: "1. Benjamini-Hochberg Yanlış Keşif Oranı (FDR)",
      desc: "Metin madenciliğinde yüzlerce hipotez test edildiğinde 'p < 0.05' eşiği sahte pozitiflere yol açar. MİRAT, tüm keşiflerde Benjamini-Hochberg FDR düzeltmesi uygulayarak q-değerlerini hesaplar ve sahte keşifleri eler.",
      icon: ShieldCheck,
      color: "text-cyan-400 border-cyan-500/30",
    },
    {
      title: "2. TOST Biyoistatistiksel Denklik Standardı",
      desc: "İki frekansın eşit olduğunu iddia etmek için klasik sıfır hipotezi testi yetersizdir (p = 1.0 eşitlik kanıtı değildir). Klinik ilaç araştırmalarında kullanılan TOST (Two One-Sided Tests) ile %5 marjında resmi denklik testi uygulanır.",
      icon: Layers,
      color: "text-emerald-400 border-emerald-500/30",
    },
    {
      title: "3. Dürüst Negatif Sonuç Raporlama Cesareti",
      desc: "Geleneksel apolojik çalışmalar yalnızca uyan verileri sunup uymayanları gizler. MİRAT; Halka Kompozisyonunun tüm surelerde evrensel olmadığını (q = 1.0) ve zıt kelimelerin eşit sayıda geçmediğini (q = 0.945) şeffaflıkla raporlar.",
      icon: AlertTriangle,
      color: "text-amber-400 border-amber-500/30",
    },
    {
      title: "4. Çift-Modelli LLM Konsensüsü (κ = 0.88)",
      desc: "Sayılar %100 deterministik SQLite çekirdeğinden gelir; yapay zekâya asla sayı saydırılmaz. LLM yalnızca anlamsal etiketleme (zıt anlam, tema) için kullanılır ve bağımsız iki modelin (DeepSeek ve Qwen) mutabakatı aranır.",
      icon: Brain,
      color: "text-purple-400 border-purple-500/30",
    },
  ];

  return (
    <section className="py-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8 pb-6 border-b border-slate-800">
        <div className="flex items-center space-x-2 text-indigo-400 text-xs font-bold uppercase tracking-wider mb-2">
          <BookOpen className="w-4 h-4" />
          <span>Bilimsel Metodoloji ve Güvenilirlik</span>
        </div>
        <h2 className="text-3xl font-extrabold text-white tracking-tight">
          Neden MİRAT Farklıdır?
        </h2>
        <p className="text-sm text-slate-400 mt-1 max-w-2xl">
          MİRAT bir inanç savunusu (apoloji) aracı değil; kutsal metne modern veri biliminin, bilgi teorisinin ve biyoistatistiğin en katı standartlarıyla bakan bağımsız bir araştırma platformudur.
        </p>
      </div>

      {/* 4 Pillars Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {principles.map((p, idx) => {
          const Icon = p.icon;
          return (
            <div
              key={idx}
              className={`p-6 rounded-2xl mirat-glass border ${p.color} space-y-3`}
            >
              <div className="flex items-center space-x-2.5">
                <Icon className={`w-5 h-5 ${p.color.split(" ")[0]}`} />
                <h3 className="text-base font-bold text-white">
                  {p.title}
                </h3>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">
                {p.desc}
              </p>
            </div>
          );
        })}
      </div>
    </section>
  );
}

