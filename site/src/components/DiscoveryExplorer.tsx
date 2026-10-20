"use client";

import React, { useState, useMemo } from "react";
import { Search, Filter, CheckCircle2, AlertCircle, ChevronDown, ChevronUp, Copy, Check, Sparkles, ExternalLink } from "lucide-react";
import findingsData from "../data/findings.json";
import { Finding } from "../types";

export default function DiscoveryExplorer() {
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedCategory, setSelectedCategory] = useState<string>("all");
  const [statusFilter, setStatusFilter] = useState<"all" | "sig" | "null" | "llm">("all");
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const [copiedId, setCopiedId] = useState<string | null>(null);

  const categories = findingsData.categories as Record<string, { id: string; name: string; total_findings: number; significant_count: number }>;
  const allFindings = findingsData.findings as Finding[];

  // Filtreleme
  const filteredFindings = useMemo(() => {
    return allFindings.filter((f) => {
      // Kategori filtresi
      if (selectedCategory !== "all" && f.category_id !== selectedCategory) {
        return false;
      }

      // Durum filtresi
      if (statusFilter === "sig" && !f.is_significant) return false;
      if (statusFilter === "null" && !f.is_honest_null) return false;
      if (statusFilter === "llm" && !f.llm_assisted) return false;

      // Arama filtresi
      if (searchQuery.trim() !== "") {
        const q = searchQuery.toLowerCase();
        const matchTitle = f.title.toLowerCase().includes(q);
        const matchDetail = f.detail.toLowerCase().includes(q);
        const matchMetric = f.metric.toLowerCase().includes(q);
        const matchEvidence = f.evidence.some((e) => e.toLowerCase().includes(q));
        const matchMethod = f.method.toLowerCase().includes(q);
        if (!matchTitle && !matchDetail && !matchMetric && !matchEvidence && !matchMethod) {
          return false;
        }
      }

      return true;
    });
  }, [allFindings, selectedCategory, statusFilter, searchQuery]);

  const toggleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const copyFinding = (f: Finding) => {
    const text = `MİRAT v6.0 Keşfi [${f.id}]: ${f.title}\nÖlçüt: ${f.metric} = ${f.value} (p=${f.null_p ?? "-"}, q=${f.q_value ?? "-"})\nDetay: ${f.detail}`;
    navigator.clipboard.writeText(text);
    setCopiedId(f.id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  return (
    <section className="py-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 pb-6 border-b border-slate-800">
        <div>
          <div className="flex items-center space-x-2 text-cyan-400 text-xs font-bold uppercase tracking-wider mb-2">
            <Sparkles className="w-4 h-4" />
            <span>Kategori 11–19 Keşif Envanteri</span>
          </div>
          <h2 className="text-3xl font-extrabold text-white tracking-tight">
            Bilimsel Keşif Kataloğu
          </h2>
          <p className="text-sm text-slate-400 mt-1 max-w-2xl">
            130.030 morfolojik segment üzerinde test edilmiş 219 bağımsız bulgu. Her bulgu katı Monte Carlo sıfır modelleri ve Benjamini-Hochberg FDR düzeltmesiyle taranmıştır.
          </p>
        </div>

        <div className="mt-4 md:mt-0 flex items-center space-x-2 text-xs text-slate-300">
          <span className="px-3 py-1.5 rounded-lg bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 font-semibold">
            102 Anlamlı (q &lt; 0.05)
          </span>
          <span className="px-3 py-1.5 rounded-lg bg-amber-500/10 text-amber-400 border border-amber-500/30 font-semibold">
            75 Dürüst Negatif
          </span>
        </div>
      </div>

      {/* Search & Filter Bar */}
      <div className="space-y-4 mb-8">
        <div className="flex flex-col sm:flex-row gap-3">
          {/* Search Box */}
          <div className="relative flex-1">
            <Search className="absolute left-3.5 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Bulgularda ara (ör. iltifat, deniz, Rahmân, kafiye, kıssa, eskatoloji)..."
              className="w-full pl-10 pr-4 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700/80 text-sm text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 transition-all"
            />
            {searchQuery && (
              <button
                onClick={() => setSearchQuery("")}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-slate-400 hover:text-white"
              >
                Temizle
              </button>
            )}
          </div>

          {/* Status Tabs */}
          <div className="flex rounded-xl bg-slate-900/90 p-1 border border-slate-800 text-xs font-medium">
            <button
              onClick={() => setStatusFilter("all")}
              className={`px-3 py-1.5 rounded-lg transition-colors ${
                statusFilter === "all" ? "bg-slate-800 text-white font-semibold" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              Tümü ({findingsData.total_count})
            </button>
            <button
              onClick={() => setStatusFilter("sig")}
              className={`px-3 py-1.5 rounded-lg transition-colors flex items-center space-x-1 ${
                statusFilter === "sig" ? "bg-emerald-500/20 text-emerald-300 font-semibold" : "text-slate-400 hover:text-emerald-300"
              }`}
            >
              <CheckCircle2 className="w-3 h-3 text-emerald-400" />
              <span>Anlamlı ({findingsData.significant_count})</span>
            </button>
            <button
              onClick={() => setStatusFilter("null")}
              className={`px-3 py-1.5 rounded-lg transition-colors flex items-center space-x-1 ${
                statusFilter === "null" ? "bg-amber-500/20 text-amber-300 font-semibold" : "text-slate-400 hover:text-amber-300"
              }`}
            >
              <AlertCircle className="w-3 h-3 text-amber-400" />
              <span>Dürüst Negatif ({findingsData.honest_null_count})</span>
            </button>
          </div>
        </div>

        {/* Category Filter Pills */}
        <div className="flex flex-wrap gap-1.5 pt-1">
          <button
            onClick={() => setSelectedCategory("all")}
            className={`px-3 py-1 rounded-lg text-xs font-semibold transition-all ${
              selectedCategory === "all"
                ? "bg-cyan-500 text-slate-950 shadow-glowCyan"
                : "bg-slate-900/80 text-slate-400 hover:bg-slate-800 hover:text-slate-200 border border-slate-800"
            }`}
          >
            Tüm Kategoriler ({allFindings.length})
          </button>
          {Object.entries(categories).map(([cid, cat]) => {
            const isSelected = selectedCategory === cid;
            return (
              <button
                key={cid}
                onClick={() => setSelectedCategory(cid)}
                className={`px-2.5 py-1 rounded-lg text-xs font-medium transition-all ${
                  isSelected
                    ? "bg-cyan-500/20 text-cyan-300 border border-cyan-500/50 shadow-glowCyan"
                    : "bg-slate-900/80 text-slate-400 hover:bg-slate-800 hover:text-slate-200 border border-slate-800"
                }`}
              >
                <span>{cat.name.replace(/^\d+\.\s*/, "")}</span>
                <span className="ml-1 text-[10px] opacity-70">({cat.total_findings})</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Results Count */}
      <div className="flex items-center justify-between text-xs text-slate-400 mb-4 px-1">
        <span>
          Görüntülenen: <strong className="text-white">{filteredFindings.length}</strong> bulgu
        </span>
        {searchQuery && (
          <span>
            "<span className="text-cyan-400">{searchQuery}</span>" için arama sonuçları
          </span>
        )}
      </div>

      {/* Findings Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {filteredFindings.map((f) => {
          const isExpanded = expandedId === f.id;
          const isCopied = copiedId === f.id;
          const isSig = f.is_significant;

          return (
            <div
              key={f.id}
              className={`p-5 rounded-2xl mirat-glass border transition-all duration-200 flex flex-col justify-between ${
                isSig
                  ? "border-slate-800 hover:border-emerald-500/40 hover:shadow-glowEmerald"
                  : "border-slate-800 hover:border-amber-500/40"
              }`}
            >
              <div>
                {/* Card Top: Badges */}
                <div className="flex items-center justify-between gap-2 mb-3">
                  <div className="flex items-center space-x-1.5 flex-wrap gap-y-1">
                    <span className="text-[10px] uppercase font-bold tracking-wider px-2 py-0.5 rounded-md bg-slate-800 text-slate-300 border border-slate-700">
                      Kat {f.category_id}
                    </span>
                    <span className="text-[10px] font-mono px-2 py-0.5 rounded-md bg-slate-900 text-slate-400 border border-slate-800">
                      {f.id}
                    </span>
                    {f.llm_assisted && (
                      <span className="text-[10px] font-semibold px-2 py-0.5 rounded-md bg-purple-500/15 text-purple-300 border border-purple-500/30">
                        🤖 Çift-Modelli
                      </span>
                    )}
                  </div>

                  {/* Status Indicator */}
                  {isSig ? (
                    <span className="flex items-center space-x-1 text-[11px] font-bold text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded-full border border-emerald-500/30">
                      <CheckCircle2 className="w-3 h-3" />
                      <span>Anlamlı</span>
                    </span>
                  ) : f.is_honest_null ? (
                    <span className="flex items-center space-x-1 text-[11px] font-bold text-amber-400 bg-amber-500/10 px-2 py-0.5 rounded-full border border-amber-500/30">
                      <AlertCircle className="w-3 h-3" />
                      <span>Dürüst Negatif</span>
                    </span>
                  ) : (
                    <span className="text-[11px] text-slate-400 font-medium">Betimsel</span>
                  )}
                </div>

                {/* Title */}
                <h3 className="text-base font-bold text-white mb-2 leading-snug">
                  {f.title}
                </h3>

                {/* Main Metric Value & Stats */}
                <div className="my-3 p-3 rounded-xl bg-slate-950/70 border border-slate-800/80 flex items-center justify-between flex-wrap gap-2 text-xs">
                  <div>
                    <span className="text-slate-400 text-[11px] block">{f.metric}:</span>
                    <span className="font-mono font-bold text-cyan-300 text-sm">
                      {typeof f.value === "number" ? f.value.toFixed(4) : f.value ?? "-"}
                    </span>
                  </div>

                  {f.null_p !== null && (
                    <div className="text-right">
                      <span className="text-slate-400 text-[11px] block">İstatistiki Güç:</span>
                      <span className="font-mono text-[11px] text-slate-300">
                        p={f.null_p.toFixed(4)} • <strong className={isSig ? "text-emerald-400" : "text-amber-400"}>q={f.q_value?.toFixed(4)}</strong>
                      </span>
                    </div>
                  )}
                </div>

                {/* Primary Detail Summary */}
                <p className="text-xs text-slate-300 leading-relaxed line-clamp-2">
                  {f.detail}
                </p>

                {/* Expanded Drawer */}
                {isExpanded && (
                  <div className="mt-4 pt-4 border-t border-slate-800/80 space-y-3 text-xs animate-fadeIn">
                    <div>
                      <span className="text-slate-400 font-semibold block mb-0.5">Analiz Yöntemi:</span>
                      <p className="text-slate-300 bg-slate-900/60 p-2 rounded-lg border border-slate-800/60">
                        {f.method}
                      </p>
                    </div>

                    {f.evidence && f.evidence.length > 0 && (
                      <div>
                        <span className="text-slate-400 font-semibold block mb-0.5">Kanıt ve Atıflar ({f.evidence.length}):</span>
                        <div className="bg-slate-900/60 p-2.5 rounded-lg border border-slate-800/60 max-h-36 overflow-y-auto space-y-1 font-mono text-[11px] text-slate-300">
                          {f.evidence.map((ev, i) => (
                            <div key={i} className="flex items-start space-x-1.5">
                              <span className="text-cyan-400">•</span>
                              <span>{ev}</span>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </div>

              {/* Card Footer: Actions */}
              <div className="mt-4 pt-3 border-t border-slate-800/60 flex items-center justify-between text-xs">
                <button
                  onClick={() => toggleExpand(f.id)}
                  className="flex items-center space-x-1 text-slate-400 hover:text-cyan-400 transition-colors font-medium"
                >
                  {isExpanded ? (
                    <>
                      <span>Detayları Gizle</span>
                      <ChevronUp className="w-3.5 h-3.5" />
                    </>
                  ) : (
                    <>
                      <span>Kanıt ve Tefsir Detayı</span>
                      <ChevronDown className="w-3.5 h-3.5" />
                    </>
                  )}
                </button>

                <button
                  onClick={() => copyFinding(f)}
                  className="flex items-center space-x-1 px-2.5 py-1 rounded-lg bg-slate-800/60 hover:bg-slate-700 text-slate-300 transition-colors"
                  title="Bulguyu Kopyala"
                >
                  {isCopied ? (
                    <>
                      <Check className="w-3.5 h-3.5 text-emerald-400" />
                      <span className="text-emerald-400 font-medium">Kopyalandı</span>
                    </>
                  ) : (
                    <>
                      <Copy className="w-3.5 h-3.5" />
                      <span>Kopyala</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {filteredFindings.length === 0 && (
        <div className="text-center py-16 mirat-glass rounded-2xl border border-slate-800">
          <AlertCircle className="w-12 h-12 text-slate-500 mx-auto mb-3" />
          <h3 className="text-lg font-bold text-white mb-1">Aradığınız kriterlere uygun bulgu bulunamadı</h3>
          <p className="text-sm text-slate-400 max-w-md mx-auto mb-4">
            Arama ifadenizi değiştirebilir veya filtreleri sıfırlayabilirsiniz.
          </p>
          <button
            onClick={() => {
              setSearchQuery("");
              setSelectedCategory("all");
              setStatusFilter("all");
            }}
            className="px-4 py-2 rounded-xl bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 text-xs font-semibold hover:bg-cyan-500/30"
          >
            Tüm Filtreleri Sıfırla
          </button>
        </div>
      )}
    </section>
  );
}

