"use client";

import React from "react";
import { Github, Heart, Database, ShieldCheck, Cpu } from "lucide-react";

export default function Footer() {
  return (
    <footer className="border-t border-slate-800/80 bg-mirat-bg/80 backdrop-blur-md pt-12 pb-8 mt-20 text-xs text-slate-400">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8 pb-8 border-b border-slate-800/60">
          {/* Col 1: Brand */}
          <div className="md:col-span-2 space-y-3">
            <div className="flex items-center space-x-2">
              <span className="text-xl">🏛️</span>
              <span className="font-extrabold text-base tracking-tight text-white">MİRAT</span>
              <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                v6.0
              </span>
            </div>
            <p className="text-xs text-slate-400 max-w-md leading-relaxed">
              Metin İçi Rastlantısallık ve Analiz Teknolojisi — Kur'an-ı Kerim metnini 130.030 morfolojik segment, katı sıfır modelleri ve çift-modelli LLM konsensüsüyle inceleyen bağımsız bilimsel araştırma platformu.
            </p>
          </div>

          {/* Col 2: Stack */}
          <div className="space-y-2">
            <h4 className="text-xs font-bold text-slate-200 uppercase tracking-wider">Teknoloji Yığını</h4>
            <ul className="space-y-1.5 text-slate-400 text-xs">
              <li className="flex items-center space-x-1.5">
                <Database className="w-3.5 h-3.5 text-cyan-400" />
                <span>SQLite (130k Segment)</span>
              </li>
              <li className="flex items-center space-x-1.5">
                <Cpu className="w-3.5 h-3.5 text-amber-400" />
                <span>DeepSeek + Qwen Konsensüsü</span>
              </li>
              <li className="flex items-center space-x-1.5">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
                <span>Benjamini-Hochberg FDR</span>
              </li>
              <li>Next.js 15 & Tailwind CSS</li>
            </ul>
          </div>

          {/* Col 3: Repos & Docs */}
          <div className="space-y-2">
            <h4 className="text-xs font-bold text-slate-200 uppercase tracking-wider">Açık Kaynak</h4>
            <ul className="space-y-1.5 text-slate-400 text-xs">
              <li>
                <a
                  href="https://github.com/yusufberkaycelik/Mirat-AI"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-cyan-400 transition-colors flex items-center space-x-1"
                >
                  <Github className="w-3.5 h-3.5" />
                  <span>GitHub Deposu</span>
                </a>
              </li>
              <li>
                <a
                  href="https://github.com/yusufberkaycelik/Mirat-AI/tree/main/raporlar"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="hover:text-cyan-400 transition-colors"
                >
                  Akademik Raporlar (PDF/MD)
                </a>
              </li>
              <li>MIT Açık Kaynak Lisansı</li>
            </ul>
          </div>
        </div>

        {/* Bottom */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 text-slate-500 text-[11px]">
          <p>© 2026 MİRAT Araştırma Projesi. Tüm bilimsel analizler ve bulgular açık erişimlidir.</p>
          <p className="flex items-center space-x-1">
            <span>Vercel Edge üzerinde sıfır sunucu maliyetiyle barındırılmaktadır</span>
          </p>
        </div>
      </div>
    </footer>
  );
}

