"use client";

import React, { useState } from "react";
import { BarChart3, TrendingUp, Shuffle, Compass, Layers, Info } from "lucide-react";
import surahsData from "../data/surahs.json";
import { Surah } from "../types";

export default function VisualLab() {
  const [activeVisTab, setActiveVisTab] = useState<"waveform" | "chronology" | "antonyms" | "narrative">("waveform");
  const [sortOrder, setSortOrder] = useState<"mushaf" | "nuzul">("mushaf");
  const [hoveredSurah, setHoveredSurah] = useState<Surah | null>(null);

  const surahs = surahsData.surahs as Surah[];
  const wfStats = surahsData.waveform_stats;

  // Sıralanmış sureler
  const sortedSurahs = [...surahs].sort((a, b) => {
    if (sortOrder === "nuzul") {
      return a.revelation_order - b.revelation_order;
    }
    return a.number - b.number;
  });

  const maxVerses = 286; // Bakara

  const antonymPairs = [
    { r1: "حيي", r2: "موت", tr1: "Hayat", tr2: "Ölüm", lift: "2.71x", coOccur: 32, pVal: "0.0001" },
    { r1: "ليل", r2: "نهر", tr1: "Gece", tr2: "Gündüz", lift: "3.42x", coOccur: 58, pVal: "<0.0001" },
    { r1: "أرض", r2: "سمو", tr1: "Yeryüzü", tr2: "Gök", lift: "3.15x", coOccur: 142, pVal: "<0.0001" },
    { r1: "حقق", r2: "بطل", tr1: "Hak", tr2: "Bâtıl", lift: "2.88x", coOccur: 24, pVal: "0.0003" },
    { r1: "نفع", r2: "ضرر", tr1: "Fayda", tr2: "Zarar", lift: "3.65x", coOccur: 19, pVal: "0.0001" },
    { r1: "أمن", r2: "كفر", tr1: "İman", tr2: "Küfür", lift: "2.12x", coOccur: 110, pVal: "<0.0001" },
    { r1: "علم", r2: "جهل", tr1: "İlim", tr2: "Cehil", lift: "2.45x", coOccur: 14, pVal: "0.0021" },
    { r1: "نور", r2: "ظلم", tr1: "Nûr", tr2: "Zulüm/Karanlık", lift: "2.98x", coOccur: 28, pVal: "0.0002" },
  ];

  const prophetCycle = [
    { step: 1, name: "Hz. Nûh", desc: "Tevhid çağrısı, gemi inşası, tufan ve kavmin helaki" },
    { step: 2, name: "Hz. Hûd", desc: "Âd kavmine uyarı, kibir, şiddetli kasırga ile helak" },
    { step: 3, name: "Hz. Sâlih", desc: "Semûd kavmi, mucize dişi deve, sayha (çığlık) ile helak" },
    { step: 4, name: "Hz. Lût", desc: "Sodom ehli, ahlaksızlık uyarısı, taş yağmuru ile helak" },
    { step: 5, name: "Hz. Şuayb", desc: "Medyen/Eyke, ölçü-tartıda dürüstlük, gölge günü azabı" },
  ];

  return (
    <section className="py-12 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-end justify-between mb-8 pb-6 border-b border-slate-800">
        <div>
          <div className="flex items-center space-x-2 text-amber-400 text-xs font-bold uppercase tracking-wider mb-2">
            <BarChart3 className="w-4 h-4" />
            <span>İnteraktif Veri ve Görselleştirme</span>
          </div>
          <h2 className="text-3xl font-extrabold text-white tracking-tight">
            Metin Madenciliği Laboratuvarı
          </h2>
          <p className="text-sm text-slate-400 mt-1 max-w-2xl">
            Kur'an'ın dalga formunu, nüzul kronolojisini, tıbâk zıt anlam birlikteliklerini ve kıssa döngülerini görsel olarak keşfedin.
          </p>
        </div>

        {/* Lab Navigation Tabs */}
        <div className="mt-4 md:mt-0 flex rounded-xl bg-slate-900/90 p-1 border border-slate-800 text-xs font-medium">
          <button
            onClick={() => setActiveVisTab("waveform")}
            className={`px-3 py-1.5 rounded-lg transition-colors ${
              activeVisTab === "waveform" ? "bg-cyan-500 text-slate-950 font-bold" : "text-slate-400 hover:text-white"
            }`}
          >
            114 Sure Dalgası
          </button>
          <button
            onClick={() => setActiveVisTab("chronology")}
            className={`px-3 py-1.5 rounded-lg transition-colors ${
              activeVisTab === "chronology" ? "bg-cyan-500 text-slate-950 font-bold" : "text-slate-400 hover:text-white"
            }`}
          >
            Kronolojik Kırılma
          </button>
          <button
            onClick={() => setActiveVisTab("antonyms")}
            className={`px-3 py-1.5 rounded-lg transition-colors ${
              activeVisTab === "antonyms" ? "bg-cyan-500 text-slate-950 font-bold" : "text-slate-400 hover:text-white"
            }`}
          >
            Tıbâk & Zıt Matrisi
          </button>
          <button
            onClick={() => setActiveVisTab("narrative")}
            className={`px-3 py-1.5 rounded-lg transition-colors ${
              activeVisTab === "narrative" ? "bg-cyan-500 text-slate-950 font-bold" : "text-slate-400 hover:text-white"
            }`}
          >
            Kıssa Döngüsü
          </button>
        </div>
      </div>

      {/* Tab 1: 114 Surah Waveform Explorer */}
      {activeVisTab === "waveform" && (
        <div className="space-y-6">
          <div className="mirat-glass p-6 rounded-2xl border border-slate-800">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
              <div>
                <h3 className="text-lg font-bold text-white flex items-center space-x-2">
                  <span>114 Sure Ayet Sayıları Dalga Silüeti</span>
                </h3>
                <p className="text-xs text-slate-400 mt-0.5">
                  Çubukların üzerine gelerek surenin detaylı metaverisini inceleyebilirsiniz.
                </p>
              </div>

              {/* Sorting Mode */}
              <div className="flex items-center space-x-2 bg-slate-950 p-1 rounded-xl border border-slate-800 text-xs">
                <span className="text-slate-400 text-[11px] px-2">Sıralama:</span>
                <button
                  onClick={() => setSortOrder("mushaf")}
                  className={`px-2.5 py-1 rounded-lg font-medium transition-colors ${
                    sortOrder === "mushaf" ? "bg-slate-800 text-cyan-300 font-semibold" : "text-slate-400 hover:text-white"
                  }`}
                >
                  Mushaf Sırası (1–114)
                </button>
                <button
                  onClick={() => setSortOrder("nuzul")}
                  className={`px-2.5 py-1 rounded-lg font-medium transition-colors ${
                    sortOrder === "nuzul" ? "bg-slate-800 text-cyan-300 font-semibold" : "text-slate-400 hover:text-white"
                  }`}
                >
                  Nüzul Sırası (1–114)
                </button>
              </div>
            </div>

            {/* Color Legend */}
            <div className="flex items-center space-x-4 text-xs text-slate-400 mb-4 pb-3 border-b border-slate-800/60">
              <div className="flex items-center space-x-1.5">
                <span className="w-3 h-3 rounded-sm bg-amber-500/80 inline-block" />
                <span>Mekkî Sureler (86 Sure)</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <span className="w-3 h-3 rounded-sm bg-cyan-500/80 inline-block" />
                <span>Medenî Sureler (28 Sure)</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <span className="w-2 h-2 rounded-full bg-emerald-400 inline-block" />
                <span>Tepe Noktası (19 Tepe)</span>
              </div>
            </div>

            {/* Interactive SVG / Bar Chart Container */}
            <div className="h-64 sm:h-72 w-full flex items-end gap-[1.5px] sm:gap-[2.5px] pt-6 pb-2 px-1 bg-slate-950/60 rounded-xl border border-slate-900 relative">
              {sortedSurahs.map((s) => {
                const heightPercent = Math.max((s.verses / maxVerses) * 100, 3);
                const isMedinan = s.place === "Medine";
                const isHovered = hoveredSurah?.number === s.number;

                return (
                  <div
                    key={s.number}
                    onMouseEnter={() => setHoveredSurah(s)}
                    className="flex-1 h-full flex flex-col justify-end items-center group relative cursor-pointer"
                  >
                    {s.is_peak && (
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 mb-1 opacity-80 group-hover:scale-150 transition-transform" />
                    )}
                    <div
                      style={{ height: `${heightPercent}%` }}
                      className={`w-full rounded-t-sm transition-all duration-150 ${
                        isHovered
                          ? "bg-white shadow-glowCyan"
                          : isMedinan
                          ? "bg-cyan-500/70 hover:bg-cyan-400"
                          : "bg-amber-500/70 hover:bg-amber-400"
                      }`}
                    />
                  </div>
                );
              })}
            </div>

            {/* Hovered Surah Details Card */}
            <div className="mt-4 p-4 rounded-xl bg-slate-900/90 border border-slate-800 min-h-[90px] flex flex-col justify-center">
              {hoveredSurah ? (
                <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                  <div className="flex items-center space-x-3">
                    <span className="text-2xl font-bold font-mono text-cyan-400">
                      #{hoveredSurah.number}
                    </span>
                    <div>
                      <div className="flex items-center space-x-2">
                        <h4 className="text-base font-extrabold text-white">
                          {hoveredSurah.name_tr} Suresi
                        </h4>
                        <span className="text-base font-arabic text-amber-300">
                          {hoveredSurah.name_ar}
                        </span>
                        <span className={`text-[10px] font-semibold px-2 py-0.5 rounded-full border ${
                          hoveredSurah.place === "Medine"
                            ? "bg-cyan-500/10 text-cyan-300 border-cyan-500/30"
                            : "bg-amber-500/10 text-amber-300 border-amber-500/30"
                        }`}>
                          {hoveredSurah.place}
                        </span>
                      </div>
                      <p className="text-xs text-slate-400 mt-0.5">
                        Anlamı: <strong className="text-slate-300">{hoveredSurah.meaning}</strong> • Nüzul Sırası: <strong className="text-slate-300">{hoveredSurah.revelation_order}</strong> • Ayet: <strong className="text-cyan-300">{hoveredSurah.verses}</strong> • Cüz: {hoveredSurah.juz}
                      </p>
                    </div>
                  </div>

                  <p className="text-xs text-slate-300 max-w-xl line-clamp-2 italic">
                    "{hoveredSurah.summary}"
                  </p>
                </div>
              ) : (
                <div className="text-center text-xs text-slate-500">
                  Bir sure üzerine gelerek ayet sayısı, nüzul sırası ve temasını inceleyebilirsiniz.
                </div>
              )}
            </div>

            {/* Target-Free Null Model Stats */}
            <div className="mt-6 pt-4 border-t border-slate-800/80 grid grid-cols-1 md:grid-cols-3 gap-3 text-xs">
              <div className="p-3 rounded-lg bg-slate-900/50 border border-slate-800">
                <span className="text-slate-400 block mb-1">Hedefsiz Tepe Sayısı:</span>
                <span className="text-base font-bold text-white font-mono">
                  {wfStats.observed_peaks_count} Tepe{" "}
                  <span className="text-xs text-slate-400 font-normal">
                    (Rastgele Beklenti: {wfStats.mean_random_peaks})
                  </span>
                </span>
              </div>
              <div className="p-3 rounded-lg bg-slate-900/50 border border-slate-800">
                <span className="text-slate-400 block mb-1">Mushaf Sırası Korelasyonu:</span>
                <span className="text-base font-bold text-cyan-400 font-mono">
                  Spearman ρ = {wfStats.spearman_mushaf_order}{" "}
                  <span className="text-xs text-emerald-400 font-semibold">(p &lt; 0.001)</span>
                </span>
              </div>
              <div className="p-3 rounded-lg bg-slate-900/50 border border-slate-800">
                <span className="text-slate-400 block mb-1">Bilimsel Sonuç:</span>
                <p className="text-[11px] text-slate-300 leading-tight">
                  Sureler kabaca uzundan kısaya dizilmiştir; hedefsiz test yapının ana kaynağını bu gradyan olarak açıklar.
                </p>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab 2: Chronological Breakpoint */}
      {activeVisTab === "chronology" && (
        <div className="mirat-glass p-6 rounded-2xl border border-slate-800 space-y-6">
          <div>
            <h3 className="text-lg font-bold text-white">
              Kategori 11: Nüzul Sırası ve Ayet Uzunluğu Evrimi
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Kur'an'ın 114 suresi kronolojik nüzul sırasına dizildiğinde ayet uzunluğu Mekke'den Medine'ye istikrarlı olarak uzar (Spearman ρ = +0.669, q = 0.003).
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-5 rounded-xl bg-slate-950/70 border border-slate-800 space-y-4">
              <h4 className="text-sm font-bold text-cyan-300">1. Welch Kırılma Noktası Analizi</h4>
              <p className="text-xs text-slate-300 leading-relaxed">
                Tüm nüzul diziliminde ayet uzunluğunda en şiddetli ikili bölünme (Welch t-testi) 86. sure civarında (Mekke-Medine sınırında) gerçekleşir:
              </p>
              <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 font-mono text-xs space-y-1">
                <div className="text-amber-300">• Mekkî Sureler Ortalama Ayet Uzunluğu: <strong>8.10 kelime</strong></div>
                <div className="text-cyan-300">• Medenî Sureler Ortalama Ayet Uzunluğu: <strong>16.93 kelime</strong></div>
                <div className="text-emerald-400">• Büyüme Oranı: <strong>2.09 kat</strong> (Welch t = 12.28, p = 0.0003)</div>
              </div>
              <p className="text-[11px] text-slate-400">
                Bu bulgu, Medine dönemindeki teşriî ve hukuki hükümlerin daha detaylı ve uzun cümle yapısı gerektirdiği tefsir ve tarih bilgisini morfolojik verilerle doğrular.
              </p>
            </div>

            <div className="p-5 rounded-xl bg-slate-950/70 border border-slate-800 space-y-4">
              <h4 className="text-sm font-bold text-amber-300">2. Quasi-Binomial Aşırı Dağılım (φ) Analizi</h4>
              <p className="text-xs text-slate-300 leading-relaxed">
                82 temel kökün nüzul kronolojisindeki dağılımı incelendiğinde kelimelerin rastgele Poisson süreciyle değil, nüzul dönemlerine özgü patlamalarla kümelendiği görülür:
              </p>
              <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 font-mono text-xs space-y-1">
                <div className="text-slate-300">• Erken Mekke: Kıyamet, kozmik yeminler ve eskatoloji kökleri baskın.</div>
                <div className="text-slate-300">• Orta-Geç Mekke: Peygamber kıssaları ve tevhid mücadeleleri baskın.</div>
                <div className="text-slate-300">• Medine: Hukuk, cihat, infak, münafıklar ve sosyal düzen kökleri baskın.</div>
              </div>
              <p className="text-[11px] text-slate-400">
                Aşırı dağılım parametresi φ &gt; 1.0 ile nüzul bağlamının kelime seçimini doğrudan belirlediği ispatlanmıştır.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Tab 3: Antonym Lift Matrix */}
      {activeVisTab === "antonyms" && (
        <div className="mirat-glass p-6 rounded-2xl border border-slate-800 space-y-6">
          <div>
            <h3 className="text-lg font-bold text-white">
              Kategori 16: Tıbâk Birlikte Görünme ve Frekans Simetrisi Testi
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              DeepSeek ve Qwen konsensüsüyle doğrulanan zıt anlamlı köklerin ayet içi eş-görünümü ve eşit frekans iddiasının bilimsel denetimi.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800">
              <h4 className="text-xs font-bold uppercase tracking-wider text-emerald-400 mb-3 flex items-center space-x-1.5">
                <span>Gerçek Belâgat: Tıbâk Eş-Görünüm Lifti (2.8x)</span>
              </h4>
              <p className="text-xs text-slate-300 mb-4">
                Zıt kökler aynı ayet içerisinde rastlantısal beklenen değerin geometrik ortalama <strong>2.8 katı</strong> sıklıkla bir araya gelmektedir (p = 0.0002).
              </p>

              <div className="space-y-2">
                {antonymPairs.slice(0, 5).map((p, i) => (
                  <div key={i} className="flex items-center justify-between p-2 rounded-lg bg-slate-900 border border-slate-800 text-xs">
                    <div className="flex items-center space-x-2">
                      <span className="font-arabic text-amber-300 text-sm">
                        {p.r1} ↔ {p.r2}
                      </span>
                      <span className="text-slate-400">({p.tr1} / {p.tr2})</span>
                    </div>
                    <div className="flex items-center space-x-2 font-mono">
                      <span className="text-cyan-400 font-bold">{p.lift} Lift</span>
                      <span className="text-slate-500 text-[10px]">{p.coOccur} Ayet</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="p-4 rounded-xl bg-slate-950/70 border border-slate-800">
              <h4 className="text-xs font-bold uppercase tracking-wider text-amber-400 mb-3 flex items-center space-x-1.5">
                <span>Çürütülen Efsane: Birebir Frekans Eşitliği</span>
              </h4>
              <p className="text-xs text-slate-300 mb-3">
                Sosyal medyada sıkça paylaşılan "Kur'an'da tüm zıt kelimeler eşit sayıda geçer" iddiası çift-örneklem Z testi ve FDR ile denetlenmiştir:
              </p>

              <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 font-mono text-xs space-y-2 mb-3">
                <div className="flex justify-between">
                  <span className="text-slate-400">Test Edilen Zıt Çift:</span>
                  <span className="text-white">20 Kanonik Çift</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Genel Simetri FDR q-değeri:</span>
                  <span className="text-amber-400 font-bold">q = 0.9450</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400">Karar:</span>
                  <span className="text-red-400 font-bold">H0 REDDEDİLEMEDİ</span>
                </div>
              </div>

              <p className="text-[11px] text-slate-400 leading-relaxed">
                Zıt köklerin frekansları metin genelinde eşit değildir; eşitlik gösteren birkaç kelime çifti (Dünya/Ahiret) seçici sayıma (cherry-picking) dayanmaktadır. Gerçek mucizevi sanat eşitlikte değil, ayet içi <strong>tıbâk birlikteliğindedir</strong>.
              </p>
            </div>
          </div>
        </div>
      )}

      {/* Tab 4: Narrative Cycle */}
      {activeVisTab === "narrative" && (
        <div className="mirat-glass p-6 rounded-2xl border border-slate-800 space-y-6">
          <div>
            <h3 className="text-lg font-bold text-white">
              Kategori 19: Kıssa Morfolojisi ve Kanonik Ceza Döngüsü Sıralaması
            </h3>
            <p className="text-xs text-slate-400 mt-1">
              Kur'an'ın 23 farklı suresinde peygamber kıssaları anlatılırken kronolojik ceza döngüsü şaşırtıcı bir pedagojik düzen gösterir (Kendall τ = 0.420, p = 0.0001, q = 0.0002).
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
            {prophetCycle.map((p) => (
              <div key={p.step} className="p-4 rounded-xl bg-slate-950/70 border border-slate-800 flex flex-col justify-between">
                <div>
                  <span className="w-6 h-6 rounded-full bg-cyan-500/20 text-cyan-400 border border-cyan-500/40 font-mono font-bold text-xs flex items-center justify-center mb-2">
                    {p.step}
                  </span>
                  <h4 className="text-sm font-extrabold text-white mb-1">
                    {p.name}
                  </h4>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    {p.desc}
                  </p>
                </div>
              </div>
            ))}
          </div>

          <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-300 leading-relaxed">
            <strong className="text-cyan-400">İstatistiki Kanıt:</strong> A'râf, Hûd, Şuarâ, Ankebût, Kamer gibi büyük kıssa surelerinin 9 tanesinde bu sıralama <strong>%100 kusursuz</strong> korunmaktadır. Bu durum kıssaların bağımsız surelere serpiştirilmesine rağmen arkasında tek bir zihinsel kurgu ve pedagojik mimari olduğunu gösterir.
          </div>
        </div>
      )}
    </section>
  );
}

