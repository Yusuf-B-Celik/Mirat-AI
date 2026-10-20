"use client";

import React, { useState } from "react";
import { BookMarked, Download, Copy, Check, FileText, Code2, ExternalLink } from "lucide-react";

export default function Publications() {
  const [copiedBibtex, setCopiedBibtex] = useState(false);
  const [copiedApa, setCopiedApa] = useState(false);

  const bibtex = `@software{celik2026mirat,
  author = {Çelik, Yusuf Berkay and MİRAT Araştırma Ekibi},
  title = {MİRAT v6.0: Doğrulanabilir Yapay Zekâ ve Kur'an Metin Madenciliği Platformu},
  year = {2026},
  url = {https://github.com/yusufberkaycelik/Mirat-AI},
  version = {6.0.0},
  note = {130.030 Morfolojik Segment, 9 Keşif Motoru, 219 Bulgu}
}`;

  const apa = `Çelik, Y. B., & MİRAT Araştırma Ekibi. (2026). MİRAT v6.0: Doğrulanabilir Yapay Zekâ ve Kur'an Metin Madenciliği Platformu (Sürüm 6.0.0) [Yazılım]. GitHub. https://github.com/yusufberkaycelik/Mirat-AI`;

  const copyText = (text: string, type: "bibtex" | "apa") => {
    navigator.clipboard.writeText(text);
    if (type === "bibtex") {
      setCopiedBibtex(true);
      setTimeout(() => setCopiedBibtex(false), 2000);
    } else {
      setCopiedApa(true);
      setTimeout(() => setCopiedApa(false), 2000);
    }
  };

  const reports = [
    {
      title: "MİRAT v6.0 Keşif Kataloğu (Master Rapor)",
      desc: "9 yeni araştırma kategorisi ve 219 bağımsız bulgunun tüm istatistiki kanıtlarını içeren ana katalog.",
      badge: "Kategori 11–19",
      file: "MIRAT_KESIF_KATALOGU.md",
      icon: BookMarked,
    },
    {
      title: "MİRAT Büyük Külliyat ve Sistem Dokümantasyonu",
      desc: "1.500+ satırlık ansiklopedik teknik dokümantasyon, formüller, hipotezler ve mimari kılavuz.",
      badge: "Master Doküman",
      file: "MIRAT_BUYUK_KULLIYAT_VE_SISTEM_DOKUMANTASYONU.md",
      icon: FileText,
    },
    {
      title: "İleri Yapısal ve Grafiksel Analiz Raporu",
      desc: "Kriptografik parite, palindromik ayetler, 114 sure dalga formu ve akustik fâsıla analizi.",
      badge: "Kriptografi & Dalga",
      file: "MIRAT_ILERI_YAPISAL_VE_GRAFIKSEL_ANALIZ.md",
      icon: Code2,
    },
  ];

  return (
    <section className="py-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="mb-8 pb-6 border-b border-slate-800">
        <div className="flex items-center space-x-2 text-amber-400 text-xs font-bold uppercase tracking-wider mb-2">
          <BookMarked className="w-4 h-4" />
          <span>Yayınlar ve Atıf Merkezi</span>
        </div>
        <h2 className="text-3xl font-extrabold text-white tracking-tight">
          Raporlar ve Akademik Kaynaklar
        </h2>
        <p className="text-sm text-slate-400 mt-1 max-w-2xl">
          MİRAT sisteminin ürettiği tüm raporlar, ham veri kümeleri ve akademik atıf biçimleri açık erişimlidir.
        </p>
      </div>

      {/* Reports Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        {reports.map((r, i) => {
          const Icon = r.icon;
          return (
            <div
              key={i}
              className="p-5 rounded-2xl mirat-glass border border-slate-800 flex flex-col justify-between hover:border-amber-500/40 transition-colors"
            >
              <div>
                <div className="flex items-center justify-between mb-3">
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-300 border border-amber-500/30">
                    {r.badge}
                  </span>
                  <Icon className="w-4 h-4 text-slate-400" />
                </div>
                <h3 className="text-base font-bold text-white mb-2 leading-snug">
                  {r.title}
                </h3>
                <p className="text-xs text-slate-300 leading-relaxed">
                  {r.desc}
                </p>
              </div>

              <div className="mt-5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
                <span className="font-mono text-slate-400 text-[11px] truncate max-w-[170px]">
                  {r.file}
                </span>
                <a
                  href={`https://github.com/yusufberkaycelik/Mirat-AI/tree/main/raporlar`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="flex items-center space-x-1 text-cyan-400 hover:text-cyan-300 font-semibold"
                >
                  <span>Görüntüle</span>
                  <ExternalLink className="w-3 h-3" />
                </a>
              </div>
            </div>
          );
        })}
      </div>

      {/* Citation Box */}
      <div className="mirat-glass p-6 rounded-2xl border border-slate-800 space-y-4">
        <h3 className="text-base font-bold text-white">Akademik Atıf (Citation)</h3>
        <p className="text-xs text-slate-400">
          Bu çalışmayı akademik veya kurumsal araştırmalarınızda kaynak göstermek için aşağıdaki formatları kullanabilirsiniz:
        </p>

        {/* BibTeX */}
        <div className="space-y-1.5">
          <div className="flex items-center justify-between text-xs">
            <span className="font-bold text-slate-300">BibTeX Formatı:</span>
            <button
              onClick={() => copyText(bibtex, "bibtex")}
              className="flex items-center space-x-1 text-cyan-400 hover:text-cyan-300"
            >
              {copiedBibtex ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-400" />
                  <span className="text-emerald-400">Kopyalandı</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" />
                  <span>Kopyala</span>
                </>
              )}
            </button>
          </div>
          <pre className="p-3 rounded-xl bg-slate-950 font-mono text-[11px] text-slate-300 overflow-x-auto border border-slate-800/80">
            {bibtex}
          </pre>
        </div>

        {/* APA */}
        <div className="space-y-1.5 pt-2">
          <div className="flex items-center justify-between text-xs">
            <span className="font-bold text-slate-300">APA 7 Formatı:</span>
            <button
              onClick={() => copyText(apa, "apa")}
              className="flex items-center space-x-1 text-cyan-400 hover:text-cyan-300"
            >
              {copiedApa ? (
                <>
                  <Check className="w-3.5 h-3.5 text-emerald-400" />
                  <span className="text-emerald-400">Kopyalandı</span>
                </>
              ) : (
                <>
                  <Copy className="w-3.5 h-3.5" />
                  <span>Kopyala</span>
                </>
              )}
            </button>
          </div>
          <p className="p-3 rounded-xl bg-slate-950 font-sans text-xs text-slate-300 border border-slate-800/80">
            {apa}
          </p>
        </div>
      </div>
    </section>
  );
}

