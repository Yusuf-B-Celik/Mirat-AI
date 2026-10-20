#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT (Metin İçi Rastlantısallık ve Analiz Teknolojisi)
Komut Satırı ve Etkileşimli Analiz Arayüzü (CLI) v4.0
"""

import argparse
import json
import sys
from mirat.database import MiratDB
from mirat.stats import z_test_equal_frequencies, chi_square_goodness_of_fit
from mirat.layers.layer1_geology import analyze_layer_1
from mirat.layers.layer2_cosmic import analyze_layer_2
from mirat.layers.layer3_ethics import analyze_layer_3
from mirat.layers.layer4_socioeconomic import analyze_layer_4
from mirat.layers.layer5_science import analyze_layer_5
from mirat.report_generator import run_all_and_save
from mirat.pattern_miner import MiratPatternMiner
from mirat.antonym_synonym_engine import MiratAntonymSynonymEngine
from mirat.advanced_structural_engine import AdvancedStructuralEngine
from mirat.claim_registry import ClaimRegistry
from mirat.null_models import MiratNullModel
from mirat.llm.budget import BudgetManager
from mirat.agent.hypothesis_agent import HypothesisAgent
from mirat.rag.qa import MiratQA
from mirat.annotation.annotate_ayahs import AyahAnnotator

def print_banner():
    print("=" * 80)
    print(" 🏛️  MİRAT (Metin İçi Rastlantısallık ve Analiz Teknolojisi) v6.0")
    print(" Doğrulanabilir Yapay Zekâ, Çok Modelli Denetçi & Bilimsel Araştırma Platformu")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="MİRAT Kur'an Morfolojik Analiz ve Doğrulanabilir Yapay Zekâ Sistemi")
    parser.add_argument("--layer", type=int, choices=[1, 2, 3, 4, 5], help="Belirli bir MİRAT analiz katmanını çalıştırır (1..5)")
    parser.add_argument("--all", action="store_true", help="Tüm 5 temel analiz katmanını çalıştırır ve rapor üretir")
    parser.add_argument("--mine", action="store_true", help="100+ Matematiksel/Bilimsel örüntüyü içeren dev madencilik kataloğunu çalıştırır")
    parser.add_argument("--category", type=int, choices=list(range(1, 20)), help="Kategori seçimi (1..10 örüntü madenciliği, 11..19 v6 keşif motorları)")
    parser.add_argument("--discover", nargs="?", const="all", type=str, help="v6 Keşif motorlarını çalıştırır: 11..19 veya 'all' (örn: --discover 11 veya --discover all)")
    parser.add_argument("--findings", action="store_true", help="Kayıtlı keşif bulgularını listeler (--category ile filtrelenebilir)")
    parser.add_argument("--antonyms", action="store_true", help="Zıt anlamlı kelimelerin 7 farklı kural ile modellenmiş analizini çalıştırır")
    parser.add_argument("--synonyms", action="store_true", help="Eş anlamlı kelime kümelerinin bağlam ve nüans analizini listeler")
    parser.add_argument("--waveform", action="store_true", help="114 Sure ayet dalga formunu ve Allah lafzı tepe noktalarını listeler/çizer")
    parser.add_argument("--crypto", action="store_true", help="Kriptografik mukattaa, palindromik ayetler ve 57-57 parite kilidini listeler")
    parser.add_argument("--chiasmus", action="store_true", help="Âyetü'l-Kürsî ve Bakara Suresi halka yapısı (chiasmus) modelini listeler")
    parser.add_argument("--phonetics", action="store_true", help="Fâsıla harfleri fonetik ve akustik dalga analizini listeler")
    parser.add_argument("--structural", action="store_true", help="Tüm ileri yapısal, grafiksel ve kriptografik analizleri çalıştırır ve raporlar")
    parser.add_argument("--root", type=str, help="Arapça kök harfleriyle arama ve frekans analizi (Örn: --root بحر)")
    parser.add_argument("--lemma", type=str, help="Arapça sözlük kök formuyla arama (Örn: --lemma دُنْيا)")
    parser.add_argument("--compare", nargs=2, metavar=('ROOT1', 'ROOT2'), help="İki kökü istatistiksel ve matematiksel olarak karşılaştırır")
    parser.add_argument("--report", action="store_true", help="Tüm analiz ve katalog raporlarını yeniden derler")
    parser.add_argument("--audit", action="store_true", help="Tüm iddiaları FDR, TOST, Bayes Faktörü ve Sıfır Modeli ile denetler")
    parser.add_argument("--null-model", action="store_true", help="Sıfır modeli baz oranı ve dalga permütasyon testini çalıştırır")
    parser.add_argument("--budget", action="store_true", help="OpenCode GO model kullanım ve kota durumunu listeler")
    parser.add_argument("--agent", action="store_true", help="Otonom hipotez keşif, eleştiri ve test döngüsünü çalıştırır")
    parser.add_argument("--ask", type=str, help="Kaynak doğrulamalı soru-cevap (RAG) motoruna soru sorar")
    parser.add_argument("--annotate", action="store_true", help="Ayet anotasyon ve konsensüs motorunu test eder")
    parser.add_argument("--limit", type=int, default=5, help="İşlem limit adedi (varsayılan: 5)")
    parser.add_argument("--web", action="store_true", help="MİRAT FastAPI Web Arayüzünü ve Canlı Jüri Panelini başlatır")
    parser.add_argument("--json", action="store_true", help="Çıktıyı JSON formatında verir")

    args = parser.parse_args()
    
    if len(sys.argv) == 1:
        print_banner()
        parser.print_help()
        return
        
    db = MiratDB()
    miner = MiratPatternMiner(db)
    antonym_engine = MiratAntonymSynonymEngine(db)
    structural_engine = AdvancedStructuralEngine(db)

    if args.discover:
        print_banner()
        from mirat.discovery.runner import run_all, ENGINES
        if args.discover == "all":
            cats = sorted(ENGINES.keys())
        else:
            try:
                cats = [int(x) for x in args.discover.split(",")]
            except ValueError:
                print(f"Geçersiz kategori: {args.discover}. 11..19 arası sayılar veya 'all' kullanın.")
                return
        print(f"🔬 MİRAT v6 Keşif Motorları Çalıştırılıyor: {cats}...\n")
        res = run_all(categories=cats, verbose=True)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
            return
        print(f"\n✅ Keşif tamamlandı! Rapor: raporlar/MIRAT_KESIF_KATALOGU.md")
        return

    if args.findings:
        print_banner()
        from mirat.discovery.runner import load_findings
        data = load_findings()
        if not data:
            print("Henüz kayıtlı keşif bulunamadı. Lütfen önce `python3 mirat_cli.py --discover all` çalıştırın.")
            return
        if args.json:
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return
        cats = data.get("categories", {})
        if args.category and str(args.category) in cats:
            target_cats = {str(args.category): cats[str(args.category)]}
        else:
            target_cats = cats
        print(f"📋 MİRAT v6 Keşif Kataloğu (Üretim: {data.get('generated_at', '-')})\n")
        for cid, c in sorted(target_cats.items(), key=lambda x: int(x[0])):
            print(f"\n📂 Kategori {cid}: {c['name']} ({c.get('runtime_sec', 0)} s)")
            print("-" * 80)
            for f in c["findings"]:
                sig = "✅" if (f.get("q_value") is not None and f["q_value"] < 0.05) else ("⚪" if f.get("null_p") is not None else "📋")
                llm = "🤖 " if f.get("llm_assisted") else ""
                if f.get("null_p") is not None:
                    q = f.get("q_value")
                    p_str = (f"p={f['null_p']:.4f} q={q:.4f}" if q is not None
                             else f"p={f['null_p']:.4f} q=- (BH uygulanmamış)")
                else:
                    p_str = "betimsel"
                print(f" {sig} {llm}[{f['id']:24}] {f['title']}")
                print(f"    Ölçüt: {f['metric']} = {f['value']} ({p_str})")
        return

    if args.waveform:
        print_banner()
        wf = structural_engine.compute_waveform_analysis()
        print(f"📈 {wf['title']}\n")
        print(f"• Toplam Sure: {wf['total_surahs']} | En Çok Ayet: {wf['max_verse_count']} (Bakara) | En Az: {wf['min_verse_count']}")
        print(f"• Oluşturulan SVG Grafiği: {wf['svg_file']}\n")
        print("Dört Ana Dalga Vuruşu (Allah Calligraphy Strokes):")
        for s in wf['silhouette_strokes']:
            print(f"  • {s['letter']:15} | {s['surah']:20} | {str(s['verses']):15} | {s['role']}")
        print("\nÖnemli Tepe Noktaları (Major Peaks):")
        for p in wf['major_peaks']:
            print(f"  Sure {p['surah_num']:3d} ({p['surah_name']:15}): {p['verse_count']:3d} Ayet")
        return

    if args.crypto:
        print_banner()
        pm = structural_engine.compute_parity_matrix()
        cp = structural_engine.compute_cryptographic_patterns()
        print(f"🔐 {pm['title']}\n")
        print(f"• Çift Toplamlı Sure Sayısı: {pm['even_count']} (Toplamları: {pm['sum_of_even_sums']:,} -> Toplam Ayet Sayısına Eşit!)")
        print(f"• Tek Toplamlı Sure Sayısı : {pm['odd_count']} (Toplamları: {pm['sum_of_odd_sums']:,} -> Toplam Sure No Toplamına Eşit!)\n")
        print(f"📜 {cp['title']}\n")
        print(f"• Mukattaa Başlangıçlı Sureler: {cp['muqattaat_surah_count']} Sure")
        print(f"• Benzersiz Harf Sayısı: {cp['muqattaat_unique_letters_count']} / 28 ({cp['alphabet_ratio']})")
        print(f"• Mnemonic: {cp['mnemonic_sentence']}\n")
        print("Çift Yönlü Döngüsel Okunan Palindromik Ayetler:")
        for pal in cp['palindromes']:
            print(f"  • {pal['verse']}: {pal['arabic']} ({pal['transliteration']})")
            print(f"    Simetri: {pal['letter_sequence']}")
            print(f"    Anlam & Mucize: {pal['marvel']}\n")
        return

    if args.chiasmus:
        print_banner()
        ch = structural_engine.compute_chiasmus_ring_composition()
        print(f"🔄 {ch['title']}\n")
        print("Âyetü'l-Kürsî (2:255) 9 Cümleli Konsantrik Hiyazm:")
        for r in ch['ayat_al_kursi_chiasmus']:
            print(f"  [{r['ring']:8}] {r['arabic']} -> {r['theme']}")
        print(f"\nBakara Suresi 286 Ayetlik Makro Halka: 143. Ayet (Vasat Ümmet):")
        print(f"  {ch['bakara_macro_ring']['ring_significance']}")
        return

    if args.phonetics:
        print_banner()
        ph = structural_engine.compute_phonetics_and_acoustics()
        print(f"🎶 {ph['title']}\n")
        print(f"• {ph['top_4_dominance']}")
        print(f"• {ph['nun_dominance']}\n")
        print("En Yaygın 10 Fâsıla Harfi:")
        for f in ph['top_fawasil']:
            print(f"  • Harf [{f['letter']}]: {f['count']:4d} kez (%{f['percentage']} )")
        return

    if args.structural:
        print_banner()
        print("MİRAT İleri Düzey Çok Boyutlu Yapısal Analiz Motoru Çalıştırılıyor...\n")
        structural_engine.generate_master_report()
        return

    if args.antonyms:
        print_banner()
        antonym_engine.generate_comprehensive_report()
        return

    if args.synonyms:
        print_banner()
        r6 = antonym_engine.analyze_rule6_synonym_clusters()
        for cl in r6['clusters']:
            print(f"🔹 {cl['cluster_name']}:")
            for m in cl['members']:
                print(f"   • {m[0]:15} (Toplam {m[1]:2d} kez): {m[2]}")
            print(f"   💡 Semantik Kural: {cl['semantic_rule']}\n")
        return

    if args.mine or args.report:
        print_banner()
        print("MİRAT Tüm Analiz, Örüntü ve İleri Yapısal Motorlar Çalıştırılıyor...\n")
        miner.generate_master_catalog()
        antonym_engine.generate_comprehensive_report()
        structural_engine.generate_master_report()
        run_all_and_save()
        print("\n✅ Tüm MİRAT Külliyatı, Raporları ve PDF Katalogları Başarıyla Güncellendi!")
        return

    if args.category:
        print_banner()
        all_cats = miner.run_all_categories()
        cat_keys = list(all_cats.keys())
        selected_key = cat_keys[args.category - 1]
        cat_data = all_cats[selected_key]
        print(f"📌 {cat_data['category_title']}\n")
        for i, p in enumerate(cat_data['patterns']):
            print(f"{i+1:02d}. {p['name']}")
            print(f"    • Metrik: {p.get('count1')} vs {p.get('count2') if 'count2' in p else ''}")
            print(f"    • Durum: {p['stat']}")
            print(f"    • Açıklama: {p['desc']}\n")
        return

    if args.all:
        print_banner()
        run_all_and_save()
        return

    if args.root:
        print_banner()
        segments = db.search_root(args.root)
        ayahs = set((s['surah'], s['ayah']) for s in segments)
        poses = {}
        for s in segments:
            poses[s['pos']] = poses.get(s['pos'], 0) + 1
        print(f"🔍 Kök Arama Sonucu: [{args.root}]")
        print(f"• Toplam Geçiş Sayısı (Segment): {len(segments)}")
        print(f"• Farklı Ayet Sayısı: {len(ayahs)}")
        print(f"• POS Dağılımı (İsim/Fiil): {poses}")
        return

    if args.compare:
        print_banner()
        r1, r2 = args.compare[0], args.compare[1]
        c1 = len(db.search_root(r1))
        c2 = len(db.search_root(r2))
        z_res = z_test_equal_frequencies(c1, c2)
        print(f"⚖️ Kök Karşılaştırma Analizi: [{r1}] vs [{r2}]")
        print(f"• [{r1}] Frekansı: {c1} | [{r2}] Frekansı: {c2}")
        print(f"• Z-Skoru: {round(z_res['z_score'], 4)} | p-Değeri: {round(z_res['p_value'], 4)}")
        print(f"• Simetrik: {'EVET' if z_res['is_symmetric'] else 'HAYIR'}")
        return

    if args.audit:
        print_banner()
        registry = ClaimRegistry(db)
        audit = registry.run_full_audit()
        if args.json:
            print(json.dumps(audit, indent=2, ensure_ascii=False))
            return
        print(f"🛡️  MİRAT Bilimsel İddia Denetimi (FDR & Bayes Doğrulaması)\n")
        print(f"• Denetlenen İddia Sayısı: {audit['total_claims_audited']}")
        print(f"• Korpus İçi Rastgele Kök Eşitlik Baz Oranı: %{audit['base_rate_equal_pair_chance']}\n")
        print("-" * 80)
        for c in audit['claims']:
            print(f"📌 [{c['id']}] {c['title']} ({c['counts']})")
            print(f"   • Sınıflandırma : {c['audit_tier']}")
            print(f"   • FDR q-Değeri  : {c['q_value_fdr']} (Ham p: {c['raw_p']})")
            print(f"   • Bayes Faktörü : BF01={c['bayes_factor_bf01']} ({c['bayes_interpretation']})")
            print(f"   • Filtre Detayı : {c['filter_notes']}\n")
        return

    if args.null_model:
        print_banner()
        null_model = MiratNullModel(db)
        br = null_model.get_equal_frequency_base_rate(min_freq=20)
        print("🎲 Sıfır Modeli 1: Rastlantısal Kök Eşitlik Baz Oranı:")
        print(f"  • {br['scientific_context']}\n")
        
        from build_quran_markdown import SURAH_METADATA
        v_counts = [SURAH_METADATA[s]['verses'] for s in range(1, 115)]
        wf = null_model.test_waveform_peak_significance(v_counts, n_permutations=2000)
        print("📈 Sıfır Modeli 2: Ayet Dalga Formu Hedefsiz Yapı Testi (post hoc tepe seçimi kaldırıldı):")
        print(f"  • Permütasyon Sayısı: {wf['n_permutations']:,}")
        print(f"  • Empirik p-Değeri  : p = {wf['empirical_p_value']}")
        print(f"  • Şaşırtıcılık Puanı: {wf['surprise_bits']} bit")
        print(f"  • Bilimsel Yorum    : {wf['evaluation']}")
        return

    if args.budget:
        print_banner()
        bm = BudgetManager()
        report = bm.get_full_budget_report()
        if args.json:
            print(json.dumps(report, indent=2, ensure_ascii=False))
            return
        print("💳 OpenCode GO Dolar Bazlı Kota Raporu (5 saat / hafta / ay pencereleri, %50 güvenlik tavanı):\n")
        print(f"{'Model Adı':26} | {'İstek':6} | {'Token':9} | {'Toplam $':9} | {'5s $ / tavan':16} | {'% 5s'}")
        print("-" * 85)
        for r in report:
            print(f"{r['model']:26} | {r['requests_used']:6d} | {r['tokens_used']:9d} | {r['cost_usd_total']:9.4f} | "
                  f"{str(r['spent_5h_usd']) + ' / ' + str(r['cap_5h_usd']):16} | %{r['usage_percent_5h']}")
        return

    if args.agent:
        print_banner()
        agent = HypothesisAgent(db)
        print("🤖 MİRAT Otonom Hipotez Keşif ve Denetim Ajanı Başlatılıyor...\n")
        cycle = agent.run_discovery_cycle(domain="etik ve adalet", n=args.limit)
        if args.json:
            print(json.dumps(cycle, indent=2, ensure_ascii=False))
            return
        for item in cycle['cycle_results']:
            r = item.get('result', {})
            crit = r.get('critic_evaluation', {})
            print(f"💡 Hipotez: {r.get('name')}")
            print(f"   • Test Edilen Kökler: [{r.get('root1')}] ({r.get('count1')}) vs [{r.get('root2')}] ({r.get('count2')})")
            print(f"   • Eleştirmen Kararı  : {crit.get('verdict')} (Risk: {crit.get('bias_risk_level')})")
            print(f"   • Deterministik Karar: {r.get('scientific_verdict')} (Güç: {r.get('evidence_strength')})")
            print(f"   • Bayes Faktörü      : BF01={r.get('bayes_factor_bf01')} ({r.get('bayes_interpretation')})")
            print(f"   • Ön-Kayıt Hash'i    : {r.get('preregistration_hash')}\n")
        return

    if args.ask:
        print_banner()
        qa = MiratQA(db)
        print(f"❓ Soru: {args.ask}\n")
        ans = qa.answer_question(args.ask)
        if args.json:
            print(json.dumps(ans, indent=2, ensure_ascii=False))
            return
        print(f"📖 Yanıt:\n{ans['answer']}\n")
        if 'citations_audit' in ans:
            ca = ans['citations_audit']
            print(f"🔍 Atıf Denetimi: Doğruluk %{ca['citation_integrity_score']} | Doğrulanan Atıflar: {ca['verified_citations']}")
            if ca['hallucinated_citations']:
                print(f"⚠️ UYARI - Uydurma Atıf Saptandı: {ca['hallucinated_citations']}")
        return

    if args.annotate:
        print_banner()
        ann = AyahAnnotator(db)
        print(f"🏷️  Ayet Anotasyon Motoru Test Ediliyor (İlk {args.limit} Ayet)...\n")
        for a_idx in range(1, args.limit + 1):
            res = ann.annotate_ayah(1, a_idx)
            print(f"Ayet [1:{a_idx}] Konsensüs Temaları: {res['consensus_themes']} | Eylem: {res['speech_act']} | Uyum: %{round(res['agreement_score']*100, 1)}")
        return

    if args.web:
        print_banner()
        print("🌐 MİRAT FastAPI Web Arayüzü ve Jüri Paneli Başlatılıyor...")
        print("👉 Tarayıcınızda açın: http://localhost:8000\n")
        import uvicorn
        uvicorn.run("web.app:app", host="0.0.0.0", port=8000, reload=False)
        return

if __name__ == "__main__":
    main()
