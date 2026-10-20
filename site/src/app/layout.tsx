import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "MİRAT v6.0 | Doğrulanabilir Yapay Zekâ ve Kur'an Metin Madenciliği",
  description:
    "130.030 morfolojik segment, 9 yeni keşif kategorisi, 219 bağımsız bulgu, çift-modelli LLM konsensüsü (DeepSeek + Qwen) ve katı sıfır modelleri ile hakemli akademik düzeyde hesaplamalı metin madenciliği vitrini.",
  keywords: [
    "Kur'an metin madenciliği",
    "hesaplamalı dilbilim",
    "doğrulanabilir yapay zekâ",
    "Benjamini-Hochberg FDR",
    "TOST denklik testi",
    "Bayes faktörü",
    "MİRAT",
    "Quran text mining",
    "NLP",
  ],
  authors: [{ name: "MİRAT Araştırma Ekibi" }],
  openGraph: {
    title: "MİRAT v6.0 — Doğrulanabilir Yapay Zekâ ve Kur'an Metin Madenciliği",
    description:
      "219 bağımsız bulgu, 114 sure dalga formu, çift modelli konsensüs ve sıfır modeli zırhı ile akademik metin madenciliği platformu.",
    type: "website",
    locale: "tr_TR",
    siteName: "MİRAT v6.0",
  },
  twitter: {
    card: "summary_large_image",
    title: "MİRAT v6.0 | Doğrulanabilir Yapay Zekâ ve Kur'an Metin Madenciliği",
    description:
      "219 bağımsız bulgu, 114 sure dalga formu, çift modelli konsensüs ve sıfır modeli zırhı ile akademik metin madenciliği platformu.",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="tr" className="dark scroll-smooth">
      <head>
        <meta charSet="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" sizes="any" />
      </head>
      <body className="bg-mirat-bg text-slate-100 min-h-screen selection:bg-cyan-500/30 selection:text-cyan-200 relative antialiased">
        {/* Ambient Top Glow */}
        <div className="fixed top-0 left-1/2 -translate-x-1/2 w-[800px] h-[350px] bg-gradient-to-b from-cyan-600/10 via-indigo-600/5 to-transparent blur-3xl pointer-events-none -z-10" />
        <div className="fixed top-40 right-10 w-[450px] h-[450px] bg-amber-500/5 blur-3xl pointer-events-none -z-10" />

        {children}
      </body>
    </html>
  );
}

