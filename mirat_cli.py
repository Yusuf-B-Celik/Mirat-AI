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

def print_banner():
    print("=" * 80)
    print(" 🏛️  MİRAT (Metin İçi Rastlantısallık ve Analiz Teknolojisi) v4.0")
    print(" Kur'an-ı Kerim Morfolojik Veritabanı, Kriptografi, Fonetik & Dalga Motoru")
    print("=" * 80)

def main():
    parser = argparse.ArgumentParser(description="MİRAT Kur'an Morfolojik Analiz ve Matematiksel Örüntü Sistemi")
    parser.add_argument("--layer", type=int, choices=[1, 2, 3, 4, 5], help="Belirli bir MİRAT analiz katmanını çalıştırır (1..5)")
    parser.add_argument("--all", action="store_true", help="Tüm 5 temel analiz katmanını çalıştırır ve rapor üretir")
    parser.add_argument("--mine", action="store_true", help="100+ Matematiksel/Bilimsel örüntüyü içeren dev madencilik kataloğunu çalıştırır")
    parser.add_argument("--category", type=int, choices=list(range(1, 11)), help="10 Örüntü madenciliği kategorisinden birini seçip listeler (1..10)")
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

if __name__ == "__main__":
    main()
