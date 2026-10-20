"use client";

import React, { useState } from "react";
import { Scale, ShieldAlert, CheckCircle2, HelpCircle, AlertTriangle, Info } from "lucide-react";
import claimsData from "../data/claims.json";
import { Claim } from "../types";

export default function ClaimAuditor() {
  const [selectedClaim, setSelectedClaim] = useState<Claim | null>(null);
  const claims = claimsData.claims as Claim[];

  const getTierBadge = (tier: string) => {
    if (tier.includes("Altın Standart")) {
      return (
        <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 flex items-center space-x-1">
          <CheckCircle2 className="w-3.5 h-3.5" />
          <span>Altın Standart</span>
        </span>
      );
    }
    if (tier.includes("Filtre Bağımlı")) {
      return (
        <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-amber-500/20 text-amber-300 border border-amber-500/40 flex items-center space-x-1">
          <AlertTriangle className="w-3.5 h-3.5" />
          <span>Filtre Bağımlı</span>
        </span>
      );
    }
    if (tier.includes("Denk")) {
      return (
        <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 flex items-center space-x-1">
          <Scale className="w-3.5 h-3.5" />
          <span>İstatistiki Denk (%5)</span>
        </span>
      );
    }
    return (
      <span className="px-2.5 py-1 rounded-full text-xs font-bold bg-slate-800 text-slate-300 border border-slate-700">
        Sıfır Modeli
      </span>
    );
  };

  return (
    <section className="py-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 pb-6 border-b border-slate-800">
        <div>
          <div className="flex items-center space-x-2 text-emerald-400 text-xs font-bold uppercase tracking-wider mb-2">
            <Scale className="w-4 h-4" />
            <span>FDR, TOST ve Bayesyen Denetim</span>
          </div>
          <h2 className="text-3xl font-extrabold text-white tracking-tight">
            Bilimsel İddia Denetçisi
          </h2>
          <p className="text-sm text-slate-400 mt-1 max-w-2xl">
            Sosyal medyada ve popüler yayınlarda dolaşan matematiksel simetri iddialarının morfolojik filtre şeffaflığı, çoklu test düzeltmesi ve Bayesyen kanıt derecesiyle tarafsız denetimi.
          </p>
        </div>

        <div className="mt-4 md:mt-0 p-3 rounded-xl bg-slate-900/90 border border-slate-800 text-xs text-slate-300">
          <span className="text-slate-400">Rastlantısal Eşitlik Baz Oranı:</span>{" "}
          <strong className="text-amber-400 font-mono">%{claimsData.base_rate_equal_pair_chance}</strong>
          <span className="text-slate-500 text-[11px] block mt-0.5">
            Frekansı ≥20 olan rastgele 2 kökün eşit çıkma olasılığı
          </span>
        </div>
      </div>

      {/* Claims Grid */}
      <div className="grid grid-cols-1 gap-4">
        {claims.map((c) => {
          const isSelected = selectedClaim?.id === c.id;

          return (
            <div
              key={c.id}
              className={`p-5 rounded-2xl mirat-glass border transition-all duration-200 cursor-pointer ${
                isSelected ? "border-cyan-500/60 shadow-glowCyan" : "border-slate-800 hover:border-slate-700"
              }`}
              onClick={() => setSelectedClaim(isSelected ? null : c)}
            >
              <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4">
                {/* Left: Title & Category */}
                <div className="flex-1">
                  <div className="flex items-center space-x-2 mb-1.5">
                    <span className="text-xs uppercase font-bold text-slate-400 tracking-wider">
                      {c.category}
                    </span>
                    <span className="text-slate-600">•</span>
                    <span className="text-xs font-mono text-slate-400">[{c.id}]</span>
                  </div>
                  <h3 className="text-lg font-bold text-white flex items-center space-x-2">
                    <span>{c.title}</span>
                    <span className="font-mono text-cyan-300 text-sm font-semibold">
                      ({c.counts})
                    </span>
                  </h3>
                </div>

                {/* Middle: Stats Preview */}
                <div className="flex items-center space-x-6 text-xs font-mono">
                  <div>
                    <span className="text-slate-500 text-[11px] block">FDR q-Değeri:</span>
                    <span className="text-slate-200 font-bold">q = {c.q_value_fdr.toFixed(4)}</span>
                  </div>
                  <div>
                    <span className="text-slate-500 text-[11px] block">Bayes Faktörü:</span>
                    <span className="text-cyan-400 font-bold">BF01 = {c.bayes_factor_bf01}</span>
                  </div>
                </div>

                {/* Right: Tier Badge */}
                <div>{getTierBadge(c.audit_tier)}</div>
              </div>

              {/* Collapsible Audit Drawer */}
              {isSelected && (
                <div className="mt-5 pt-4 border-t border-slate-800/80 text-xs space-y-4 animate-fadeIn">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 space-y-2">
                      <span className="text-slate-400 font-semibold block flex items-center space-x-1">
                        <Info className="w-3.5 h-3.5 text-cyan-400" />
                        <span>Filtre Bağımlılığı & Morfolojik Tercih:</span>
                      </span>
                      <p className="text-slate-200 leading-relaxed">
                        {c.filter_notes}
                      </p>
                      {c.filter_dependent && (
                        <div className="p-2.5 rounded-lg bg-amber-500/10 border border-amber-500/30 text-amber-300 text-[11px] flex items-start space-x-2 mt-2">
                          <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
                          <span>
                            <strong>Ad Hoc Seçim Riski:</strong> Bu eşitlik ancak belirli gramer ekleri veya morfolojik formlar seçildiğinde sağlanmaktadır; yalın kök aramasında frekanslar farklıdır.
                          </span>
                        </div>
                      )}
                    </div>

                    <div className="p-3.5 rounded-xl bg-slate-950/70 border border-slate-800 space-y-2">
                      <span className="text-slate-400 font-semibold block">Bayesyen Kanıt & Denklik:</span>
                      <div className="space-y-1 text-slate-300">
                        <div>• Yorum: <strong className="text-emerald-400">{c.bayes_interpretation}</strong></div>
                        <div>• TOST %5 Denkliği: <strong className={c.tost_equivalent ? "text-emerald-400" : "text-amber-400"}>{c.tost_equivalent ? "DENK (p < 0.05)" : "Denk Değil (p >= 0.05)"}</strong></div>
                        <div>• Rastlantısal Baz Olasılığı: <strong className="text-slate-300">%{c.base_rate_p ? (c.base_rate_p * 100).toFixed(2) : "1.06"}</strong></div>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </section>
  );
}

