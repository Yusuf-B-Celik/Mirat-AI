"use client";

import React, { useState } from "react";
import Navbar from "../components/Navbar";
import Hero from "../components/Hero";
import DiscoveryExplorer from "../components/DiscoveryExplorer";
import VisualLab from "../components/VisualLab";
import ClaimAuditor from "../components/ClaimAuditor";
import StatisticalPlayground from "../components/StatisticalPlayground";
import PreregistrationLedger from "../components/PreregistrationLedger";
import MethodologySection from "../components/MethodologySection";
import Publications from "../components/Publications";
import Footer from "../components/Footer";

export default function Home() {
  const [activeTab, setActiveTab] = useState<string>("kesifler");

  return (
    <div className="flex flex-col min-h-screen">
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="flex-1">
        {/* Hero Section */}
        <Hero onExplore={(tab) => setActiveTab(tab)} />

        {/* Tab Controls Bar */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 mb-6">
          <div className="flex items-center justify-center p-1 rounded-2xl bg-slate-900/90 border border-slate-800 max-w-3xl mx-auto overflow-x-auto">
            <button
              onClick={() => setActiveTab("kesifler")}
              className={`flex-1 py-2 px-4 rounded-xl text-xs font-bold transition-all whitespace-nowrap ${
                activeTab === "kesifler"
                  ? "bg-cyan-500 text-slate-950 shadow-glowCyan"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              🔬 Keşif Kataloğu (219)
            </button>
            <button
              onClick={() => setActiveTab("laboratuvar")}
              className={`flex-1 py-2 px-4 rounded-xl text-xs font-bold transition-all whitespace-nowrap ${
                activeTab === "laboratuvar"
                  ? "bg-cyan-500 text-slate-950 shadow-glowCyan"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              📊 Veri Laboratuvarı
            </button>
            <button
              onClick={() => setActiveTab("denetci")}
              className={`flex-1 py-2 px-4 rounded-xl text-xs font-bold transition-all whitespace-nowrap ${
                activeTab === "denetci"
                  ? "bg-cyan-500 text-slate-950 shadow-glowCyan"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              🛡️ İddia Denetçisi
            </button>
            <button
              onClick={() => setActiveTab("hesaplayici")}
              className={`flex-1 py-2 px-4 rounded-xl text-xs font-bold transition-all whitespace-nowrap ${
                activeTab === "hesaplayici"
                  ? "bg-cyan-500 text-slate-950 shadow-glowCyan"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              🧮 Canlı Hesaplayıcı
            </button>
            <button
              onClick={() => setActiveTab("raporlar")}
              className={`flex-1 py-2 px-4 rounded-xl text-xs font-bold transition-all whitespace-nowrap ${
                activeTab === "raporlar"
                  ? "bg-cyan-500 text-slate-950 shadow-glowCyan"
                  : "text-slate-400 hover:text-white"
              }`}
            >
              📥 Raporlar & Atıf
            </button>
          </div>
        </div>

        {/* Tab Content Display */}
        <div className="min-h-[500px]">
          {activeTab === "kesifler" && <DiscoveryExplorer />}
          {activeTab === "laboratuvar" && <VisualLab />}
          {activeTab === "denetci" && (
            <>
              <ClaimAuditor />
              <PreregistrationLedger />
            </>
          )}
          {activeTab === "hesaplayici" && <StatisticalPlayground />}
          {activeTab === "raporlar" && (
            <>
              <Publications />
              <MethodologySection />
            </>
          )}
        </div>

        {/* Supporting Methodology & Transparency on Main Page */}
        {activeTab === "kesifler" && (
          <div className="mt-12">
            <MethodologySection />
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}

