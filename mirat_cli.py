#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT (Metin İçi Rastlantısallık ve Analiz Teknolojisi)
Komut Satırı ve Etkileşimli Analiz Arayüzü (CLI) v3.0
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

def print_banner():
    print("=" * 78)
    print(" 🏛️  MİRAT (Metin İçi Rastlantısallık ve Analiz Teknolojisi) v3.0")
    print(" Kur'an-ı Kerim Morfolojik Veritabanı, Zıt/Eş Anlam ve Matematiksel Örüntü Motoru")
    print("=" * 78)

def main():
    parser = argparse.ArgumentParser(description="MİRAT Kur'an Morfolojik Analiz ve Matematiksel Örüntü Sistemi")
    parser.add_argument("--layer", type=int, choices=[1, 2, 3, 4, 5], help="Belirli bir MİRAT analiz katmanını çalıştırır (1..5)")
    parser.add_argument("--all", action="store_true", help="Tüm 5 temel analiz katmanını çalıştırır ve rapor üretir")
    parser.add_argument("--mine", action="store_true", help="100+ Matematiksel/Bilimsel örüntüyü içeren dev madencilik kataloğunu çalıştırır")
    parser.add_argument("--category", type=int, choices=list(range(1, 11)), help="10 Örüntü madenciliği kategorisinden birini seçip listeler (1..10)")
    parser.add_argument("--antonyms", action="store_true", help="Zıt anlamlı kelimelerin 7 farklı kural ile modellenmiş analizini çalıştırır")
    parser.add_argument("--synonyms", action="store_true", help="Eş anlamlı kelime kümelerinin bağlam ve nüans analizini listeler")
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
    
    if args.antonyms:
        print_banner()
        print("Zıt Anlamlı Kelimelerin 7 Kural ile Analizi Çalıştırılıyor...\n")
        antonym_engine.generate_comprehensive_report()
        res = antonym_engine.run_full_analysis()
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            r1 = res['rule1_root_exact_parity']
            print(f"📌 {r1['title']}:")
            for item in r1['items']:
                print(f"  • {item['name']:35} | {item['count1']:3d} vs {item['count2']:3d} | VSI: %{item['vsi_score']} | {item['p_value']}")
            print("\n" + "="*50 + "\n")
            r4 = res['rule4_tibak_co_occurrence']
            print(f"📌 {r4['title']}:")
            for item in r4['items']:
                print(f"  • {item['pair_name']:35} | Aynı Ayette: {item['same_ayah_count']:3d} Ayet | PMI: {item['pmi']}")
        return

    if args.synonyms:
        print_banner()
        r6 = antonym_engine.analyze_rule6_synonym_clusters()
        print(f"📌 {r6['title']}\n")
        for cl in r6['clusters']:
            print(f"🔹 {cl['cluster_name']}:")
            for m in cl['members']:
                print(f"   • {m[0]:15} (Toplam {m[1]:2d} kez): {m[2]}")
            print(f"   💡 Semantik Kural: {cl['semantic_rule']}\n")
        return

    if args.mine or args.report:
        print_banner()
        print("MİRAT Örüntü Madenciliği ve Raporlama Motoru Çalıştırılıyor...\n")
        miner.generate_master_catalog()
        antonym_engine.generate_comprehensive_report()
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
        
    if args.layer:
        print_banner()
        print(f"Katman {args.layer} Analizi Başlatılıyor...\n")
        layer_map = {
            1: analyze_layer_1,
            2: analyze_layer_2,
            3: analyze_layer_3,
            4: analyze_layer_4,
            5: analyze_layer_5
        }
        res = layer_map[args.layer](db)
        if args.json:
            print(json.dumps(res, indent=2, ensure_ascii=False))
        else:
            for k, v in res.items():
                print(f"🔹 {v.get('title', k)}:")
                for sub_k, sub_v in v.items():
                    if sub_k != 'title':
                        print(f"   • {sub_k}: {sub_v}")
                print("-" * 50)
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
        print("\nÖrnek İlk 5 Geçiş:")
        for s in segments[:5]:
            print(f"   [{s['location']}] {s['form']} ({s['lemma']}) - Sure {s['surah']}, Ayet {s['ayah']}")
        return
        
    if args.lemma:
        print_banner()
        segments = db.search_lemma(args.lemma)
        ayahs = set((s['surah'], s['ayah']) for s in segments)
        print(f"🔍 Lemma Arama Sonucu: [{args.lemma}]")
        print(f"• Toplam Geçiş Sayısı: {len(segments)}")
        print(f"• Farklı Ayet Sayısı: {len(ayahs)}")
        print("\nÖrnek İlk 5 Geçiş:")
        for s in segments[:5]:
            print(f"   [{s['location']}] {s['form']} - Sure {s['surah']}, Ayet {s['ayah']}")
        return
        
    if args.compare:
        print_banner()
        r1, r2 = args.compare[0], args.compare[1]
        c1 = len(db.search_root(r1))
        c2 = len(db.search_root(r2))
        z_res = z_test_equal_frequencies(c1, c2)
        print(f"⚖️ Kök Karşılaştırma Analizi: [{r1}] vs [{r2}]")
        print(f"• [{r1}] Frekansı: {c1}")
        print(f"• [{r2}] Frekansı: {c2}")
        print(f"• Toplam: {c1 + c2}")
        print(f"• Oran: %{round((c1/(c1+c2))*100, 2) if (c1+c2)>0 else 0} vs %{round((c2/(c1+c2))*100, 2) if (c1+c2)>0 else 0}")
        print(f"• Z-Skoru: {round(z_res['z_score'], 4)}")
        print(f"• p-Değeri: {round(z_res['p_value'], 4)}")
        print(f"• İstatistiki Simetri (p >= 0.05): {'EVET (Simetrik)' if z_res['is_symmetric'] else 'HAYIR (Asimetrik)'}")
        return

if __name__ == "__main__":
    main()
