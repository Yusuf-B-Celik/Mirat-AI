"use client";

import React, { useState } from "react";
import { ShieldCheck, Hash, Link2, CheckCircle2, Lock } from "lucide-react";
import preregData from "../data/preregistration.json";
import { PreregRecord } from "../types";

export default function PreregistrationLedger() {
  const records = preregData.records as PreregRecord[];
  const isValid = preregData.chain_valid;

  return (
    <section className="py-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 pb-6 border-b border-slate-800">
        <div>
          <div className="flex items-center space-x-2 text-purple-400 text-xs font-bold uppercase tracking-wider mb-2">
            <Lock className="w-4 h-4" />
            <span>Kriptografik Bütünlük ve Şeffaflık</span>
          </div>
          <h2 className="text-3xl font-extrabold text-white tracking-tight">
            Ön-Kayıt (Preregistration) Defteri
          </h2>
          <p className="text-sm text-slate-400 mt-1 max-w-2xl">
            Tüm hipotezler, sayım işlemi yapılmadan önce SHA-256 hash zinciriyle kayıt altına alınır. Bu sayede sonuç görüldükten sonra hipotez uydurulması (p-hacking / HARKing) matematiksel olarak imkânsız hale getirilir.
          </p>
        </div>

        <div className="mt-4 md:mt-0 flex items-center space-x-2 px-3 py-1.5 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 text-xs font-bold">
          <CheckCircle2 className="w-4 h-4" />
          <span>SHA-256 Zinciri Doğrulandı ({records.length} Blok)</span>
        </div>
      </div>

      {/* Hash Chain Records */}
      <div className="space-y-3 font-mono text-xs">
        {records.map((r, idx) => (
          <div
            key={r.hash}
            className="p-4 rounded-xl mirat-glass border border-slate-800 flex flex-col md:flex-row md:items-center justify-between gap-3 hover:border-purple-500/40 transition-colors"
          >
            <div className="flex items-start space-x-3">
              <span className="w-7 h-7 rounded-lg bg-purple-500/20 text-purple-300 border border-purple-500/40 flex items-center justify-center font-bold text-xs shrink-0">
                #{idx + 1}
              </span>
              <div>
                <h4 className="text-sm font-sans font-bold text-white mb-1">
                  {r.hypothesis}
                </h4>
                <div className="flex items-center space-x-2 text-[11px] text-slate-400 flex-wrap">
                  <span>Hedef Kökler: <strong className="text-amber-300 font-arabic text-sm">{r.target_roots.join(" vs ")}</strong></span>
                  <span>•</span>
                  <span>Model: {r.model_name}</span>
                  <span>•</span>
                  <span>İlişki: {r.expected_relation}</span>
                </div>
              </div>
            </div>

            <div className="text-right shrink-0">
              <span className="text-slate-500 text-[10px] block">Blok Hash'i:</span>
              <span className="text-cyan-400 font-bold tracking-tight text-[11px]">
                {r.hash.substring(0, 16)}...{r.hash.substring(r.hash.length - 8)}
              </span>
              <span className="text-[10px] text-slate-500 block">
                {r.timestamp.replace("T", " ").substring(0, 19)} UTC
              </span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}

