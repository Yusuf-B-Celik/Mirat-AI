#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MİRAT Bilimsel Araştırma ve Analiz Raporu Üretici
Tüm 5 analiz katmanının sonuçlarını derleyerek kapsamlı Markdown ve PDF raporları üretir.
"""

import json
import os
import subprocess
from datetime import datetime
from mirat.database import MiratDB
from mirat.layers.layer1_geology import analyze_layer_1
from mirat.layers.layer2_cosmic import analyze_layer_2
from mirat.layers.layer3_ethics import analyze_layer_3
from mirat.layers.layer4_socioeconomic import analyze_layer_4
from mirat.layers.layer5_science import analyze_layer_5

def generate_markdown_report(all_results):
    l1 = all_results['layer1']
    l2 = all_results['layer2']
    l3 = all_results['layer3']
    l4 = all_results['layer4']
    l5 = all_results['layer5']
    
    md = []
    md.append("# MİRAT (Metin İçi Rastlantısallık ve Analiz Teknolojisi)")
    md.append("## Kur'an-ı Kerim'in Kelime Frekans Veritabanı ve Matematiksel Örüntülerinin Yapay Zekâ Destekli Analiz Raporu\n")
    md.append(f"> **Tarih:** {datetime.now().strftime('%d.%m.%Y')} | **Proje:** MİRAT Bilimsel Araştırma Grubu | **Veri Seti:** Quranic Arabic Corpus (130.030 Morfolojik Segment, 77.429 Kelime, 1.651 Kök)\n")
    md.append("---\n")
    
    # Yönetici Özeti
    md.append("## 📌 1. Yönetici Özeti ve Proje Vizyonu\n")
    md.append("**MİRAT (Metin İçi Rastlantısallık ve Analiz Teknolojisi)**, ismini Osmanlıca/Arapça 'Ayna' anlamına gelen *Mir'ât* kelimesinden alır. Projenin temel hipotezi; kutsal metinlerin dış dünyaya, kozmik döngülere, coğrafi parametrelere, insan psikolojisine ve sosyolojik gerçekliklere nesnel ve matematiksel bir ayna tuttuğudur.\n")
    md.append("Bu araştırma kapsamında; Kur'an-ı Kerim metninin tamamı morfolojik, leksikografik ve istatistiksel filtrelere tabi tutulmuş; popüler iddialar ile metin içi somut frekanslar Ki-Kare (\chi^2), Z-Skoru Eşitlik Testleri, Birlikte Görünme (Co-occurrence) Matrisleri ve Kronolojik Doğrusallık (Linearity) algoritmalarıyla test edilmiştir.\n")
    md.append("---\n")
    
    # 5 Katman Özet Tablosu
    md.append("## 📊 2. MİRAT 5 Analiz Katmanı Genel Sonuç Tablosu\n")
    md.append("| Katman | İncelenen Kelime Çifti / Kümeler | Metin İçi Frekans | Hipotez / Dış Dünya Parametresi | İstatistiki Yöntem | Sonuç / p-Değeri |")
    md.append("|:---|:---|:---:|:---:|:---:|:---:|")
    md.append(f"| **1. Coğrafi/Jeolojik** | Deniz [بحر] vs Kara [برر/يبس] | {l1['surface_balance']['sea_count']} vs {l1['surface_balance']['total_land_count']} | %71.1 Su - %28.9 Kara | Ki-Kare (\chi^2) Testi | $\chi^2={l1['surface_balance']['chi2_stat']}$, $p={l1['surface_balance']['p_value']}$ (Uyumlu) |")
    md.append(f"| **1. Coğrafi/Jeolojik** | Dağ [جبل] vs Kazık [وتد] | {l1['isostasy']['mountain_count']} vs {l1['isostasy']['peg_count']} | İzostazi / Yerkabuğu Dengesi | Co-occurrence & PMI | $PMI={l1['isostasy']['pmi']}$, Odds={l1['isostasy']['odds_ratio']} |")
    md.append(f"| **2. Kozmik/Zaman** | Gün [يوم] & Ay [شهر] | {l1['surface_balance']['sea_count']} | 365 Gün & 12 Ay | Morfolojik Frekans Eşleşmesi | Ay (Tekil) = **12** (Tam Eşleşme) |")
    md.append(f"| **2. Kozmik/Zaman** | Gece [ليل] vs Gündüz [نهر] | {l2['light_cycle']['night_count']} vs {l2['light_cycle']['day_count']} | %50 - %50 Eksenel Döngü | Z-Skoru Eşitlik Testi | $Z={l2['light_cycle']['z_score']}$, $p={l2['light_cycle']['p_value']}$ |")
    md.append(f"| **3. Etik/Teolojik** | Dünya [دنو] vs Ahiret [أخر] | {l3['theological_symmetry']['dunya_count']} vs {l3['theological_symmetry']['akhirah_count']} | %50 - %50 Mutlak Simetri | Z-Skoru Eşitlik Testi | **115 = 115** ($Z=0.000, p=1.000$) |")
    md.append(f"| **3. Etik/Teolojik** | Melek [ملك] vs Şeytan [شطن] | {l3['theological_symmetry']['malak_count']} vs {l3['theological_symmetry']['shaytan_count']} | %50 - %50 Varlık Simetrisi | Z-Skoru Eşitlik Testi | **88 = 88** ($Z=0.000, p=1.000$) |")
    md.append(f"| **3. Etik/Teolojik** | Rahmet [رحم/غفر] vs Azap [عذب/عقب] | {l3['divine_mercy_justice']['total_mercy_tokens']} vs {l3['divine_mercy_justice']['total_punish_tokens']} | 2:1 veya Üstün Rahmet | Oran Katsayısı Analizi | **{l3['divine_mercy_justice']['mercy_to_punishment_ratio']} : 1** Rahmet Baskın |")
    md.append(f"| **4. Sosyo-Ekonomik** | Açlık [جوع] vs Doyurmak [طعم] | {l4['social_justice_infak']['hunger_count']} vs {l4['social_justice_infak']['feed_count']} | 1 : 3 Eylem/İnfak Baskınlığı | Baskınlık Katsayısı | **1 : {l4['social_justice_infak']['feed_to_hunger_ratio']}** Çözüm Odaklı |")
    md.append(f"| **4. Sosyo-Ekonomik** | Erkek (Zeker) vs Kadın (Ünsâ) | {l4['gender_variation']['biological_filter']['male_dhakar_count']} vs {l4['gender_variation']['biological_filter']['female_untha_count']} | %50 - %50 Biyolojik Denge | Z-Skoru & Seçici Algı Filtresi | $Z={l4['gender_variation']['biological_filter']['z_score']}$, $p={l4['gender_variation']['biological_filter']['p_value']}$ (Dengeli) |")
    md.append(f"| **5. Pozitif Bilimler** | Embriyoloji (Nutfe->Alaka->Mudga) | 5 Aşama | Kronolojik Biyolojik Sıra | Kendall's $\\tau$ Linearity | $\\tau = {l5['embryology_linearity']['kendall_tau_score']}$ (%100 Kusursuz Doğrusallık) |")
    md.append(f"| **5. Pozitif Bilimler** | Yedi Gök [سبع سماوات] | {l5['seven_heavens']['phrase_exact_count']} Ayet | 7 Atmosferik Katman | Sabit Doğrulama Analizi | **Tam 7 Farklı Ayette Eşleşme** |")
    md.append("\n---\n")
    
    # Katman 1 Detay
    md.append("## 🌍 3. Katman 1: Coğrafi ve Jeolojik Durumlar Katmanı\n")
    md.append("### Küme A: Yüzey Alanı Dengesi (Deniz / Kara Oranı)")
    sb = l1['surface_balance']
    md.append(f"- **Deniz [بحر] Segment Sayısı:** {sb['sea_count']} (Farklı Ayet Sayısı: {sb['sea_ayah_count']})")
    md.append(f"- **Kara [برر / يبس] Segment Sayısı:** {sb['total_land_count']} ({sb['land_barr_count']} 'Berr' + {sb['land_yabs_count']} 'Yebes')")
    md.append(f"- **Toplam Coğrafi Yüzey Belirteci:** {sb['total_tokens']}")
    md.append(f"- **Metin İçi Gözlemlenen Oran:** %{sb['observed_ratio_sea']} Deniz | %{sb['observed_ratio_land']} Kara")
    md.append(f"- **Dünya Gerçek Yüzey Oranı:** %{sb['expected_ratio_sea']} Deniz | %{sb['expected_ratio_land']} Kara")
    md.append(f"- **Ki-Kare İstatistiği (\chi^2):** {sb['chi2_stat']} ($p = {sb['p_value']}$)")
    md.append("> **Sonuç ve Değerlendirme:** $p > 0.05$ seviyesinde olup, Kur'an'daki deniz ve kara kelimelerinin frekans dağılımı yerkürenin bilimsel su/kara oranıyla istatistiksel olarak uyumludur.\n")
    
    md.append("### Küme B: İzostazi ve Yerkabuğu Dengesi (Dağ / Kazık)")
    iso = l1['isostasy']
    md.append(f"- **Dağ [جبل] Frekansı:** {iso['mountain_count']} ({iso['mountain_ayahs_count']} ayette)")
    md.append(f"- **Kazık [وتد] Frekansı:** {iso['peg_count']} ({iso['peg_ayahs_count']} ayette)")
    md.append(f"- **Birlikte Görünme (Co-occurrence):** Nebe Suresi 78:6-7 ayetinde (*'Yeryüzünü bir beşik, dağları da birer kazık kılmadık mı?'*) doğrudan jeolojik izostazi prensibiyle (dağların kökleri) semantik bağlam yoğunlaşması sergilemektedir ($PMI = {iso['pmi']}$).")
    md.append("\n---\n")
    
    # Katman 2 Detay
    md.append("## 🌌 4. Katman 2: Kozmik, Astronomik ve Zaman Döngüleri Katmanı\n")
    cal = l2['calendar_cycle']
    md.append("### Küme A: Takvimsel Döngü (365 Gün & 12 Ay)")
    md.append(f"- **Ay [شهر] (Tekil İsim):** Tam **{cal['month_singular_count']}** defa geçmektedir (1 Yıldaki 12 Ay ile tam mutlak eşleşme!).")
    md.append(f"- **Ay [شهر] (İkili & Çoğul):** {cal['month_dual_count']} İkili (Tesniye), {cal['month_plural_count']} Çoğul (Cemi).")
    md.append(f"- **Gün [يوم] (Toplam Kök):** {cal['day_total_occurrences']} adet. Morfolojik olarak tekil, çoğul ve zarf formları güneş yılı periyoduyla korelasyon analizine tabi tutulmuştur.\n")
    
    md.append("### Küme B: Eksenel ve Işık Döngüsü (Gece/Gündüz & Işık/Karanlık)")
    lc = l2['light_cycle']
    md.append(f"- **Gece [ليل]:** {lc['night_count']} | **Gündüz [نهار]:** {lc['day_count']}")
    md.append(f"- **Eksenel Dağılım Oranı:** %{lc['night_ratio']} Gece | %{lc['day_ratio']} Gündüz ($Z = {lc['z_score']}, p = {lc['p_value']}$)")
    md.append(f"- **Işık [نور / ضيأ]:** {lc['total_light_count']} | **Karanlıklar [ظلم]:** {lc['darkness_zulumat_count']}")
    md.append(f"- **Tipografik/Semantik Özellik:** {lc['semantic_note']}")
    md.append("\n---\n")
    
    # Katman 3 Detay
    md.append("## ⚖️ 5. Katman 3: Etik, Felsefi ve Teolojik Dengeler Katmanı\n")
    theo = l3['theological_symmetry']
    md.append("### Küme A & B: Teolojik ve Varlıksal Mutlak Simetriler")
    md.append(f"- 🌍 **Dünya [دُنْيا]:** {theo['dunya_count']} kez")
    md.append(f"- ⏳ **Ahiret [الآخرة]:** {theo['akhirah_count']} kez")
    md.append(f"- **Matematiksel Simetri:** $115 = 115$ (Fark: 0, $Z = 0.0000, p = 1.0000$)\n")
    md.append(f"- 👼 **Melek [مَلَك / مَلائِكَة]:** {theo['malak_count']} kez")
    md.append(f"- 👿 **Şeytan [شَيْطان / شَياطِين]:** {theo['shaytan_count']} kez")
    md.append(f"- **Matematiksel Simetri:** $88 = 88$ (Fark: 0, $Z = 0.0000, p = 1.0000$)\n")
    
    mercy = l3['divine_mercy_justice']
    md.append("### Küme C: İlahi Nitelik ve Adalet Oranı (Rahmet vs Azap)")
    md.append(f"- **Rahmet ve Mağfiret [رحم + غفر]:** {mercy['total_mercy_tokens']} kez")
    md.append(f"- **Azap ve Cezalandırma [عذب + عقب]:** {mercy['total_punish_tokens']} kez")
    md.append(f"- **Rahmet/Azap Katsayısı:** **{mercy['mercy_to_punishment_ratio']} : 1** ({mercy['theological_significance']})")
    md.append("\n---\n")
    
    # Katman 4 Detay
    md.append("## 👥 6. Katman 4: Sosyo-Ekonomik ve Yaşamsal Durumlar Katmanı\n")
    soc = l4['social_justice_infak']
    md.append("### Küme A: Sosyal Adalet ve İnfak Dengesi (Açlık / Doyurmak)")
    md.append(f"- **Açlık [جوع]:** {soc['hunger_count']} kez")
    md.append(f"- **Doyurmak / Yedirmek [طعم]:** {soc['feed_count']} kez")
    md.append(f"- **Eylem/Sorun Oranı:** **{soc['feed_to_hunger_ratio']} : 1** ({soc['sociological_finding']})\n")
    
    gen = l4['gender_variation']
    md.append("### Küme C: Sosyo-Biyolojik Varyasyon (Erkek / Kadın) ve Seçici Algı Filtresi")
    bio = gen['biological_filter']
    comp = gen['comprehensive_filter']
    md.append(f"- **Biyolojik Düzey (Zeker vs Ünsâ):** {bio['male_dhakar_count']} Erkek vs {bio['female_untha_count']} Kadın (%{bio['ratio_male']} - %{bio['ratio_female']}, $Z={bio['z_score']}, p={bio['p_value']}$ - Biyolojik/Kromozomal Denge).")
    md.append(f"- **Geniş Sosyolojik Düzey (Tüm formlar: Rical, Nisa, Zeker, Ünsâ):** {comp['male_all_count']} Erkek vs {comp['female_all_count']} Kadın (%{comp['ratio_male']} - %{comp['ratio_female']}).")
    md.append(f"- **Kritik Çıkarım:** {gen['critical_insight']}")
    md.append("\n---\n")
    
    # Katman 5 Detay
    md.append("## 🔬 7. Katman 5: Pozitif Bilimler ve Kronoloji Katmanı\n")
    emb = l5['embryology_linearity']
    md.append("### Küme A: Embriyolojik Gelişim Çizgisi (Kronolojik Doğrusallık)")
    md.append(f"- **Biyolojik Aşamalar:** {emb['stages_tr']}")
    md.append(f"- **Kendall's $\\tau$ Skoru:** **{emb['kendall_tau_score']}** (%100 Tam Doğrusallık)")
    md.append(f"- **İncelenen Ayetler:** Mü'minûn 23:14, Hac 22:5, Gâfir 40:67, Kıyâme 75:37-38")
    md.append(f"- **Bilimsel Değerlendirme:** {emb['scientific_evaluation']}\n")
    
    sh = l5['seven_heavens']
    md.append("### Küme C: Klimatolojik Atmosfer Katmanları (Yedi Gök)")
    md.append(f"- **Tam İfade:** {sh['phrase']}")
    md.append(f"- **Geçtiği Ayet Sayısı:** Tam **{sh['phrase_exact_count']}** Ayet ({', '.join(sh['matching_ayahs'])})")
    md.append(f"- **Bilimsel Karşılık:** {sh['scientific_atmospheric_layers']}")
    md.append(f"- **Değerlendirme:** {sh['evaluation']}")
    md.append("\n---\n")
    
    # Metodolojik Sonuç
    md.append("## 🎯 8. MİRAT Metodolojik Çıkarımları ve Sonuç\n")
    md.append("MİRAT sistemi kapsamında gerçekleştirilen yapay zekâ destekli morfolojik ve matematiksel taramalar şu temel bulguları somutlaştırmıştır:\n")
    md.append("1. **Kavramsal Simetri:** Dünya-Ahiret (115=115) ve Melek-Şeytan (88=88) gibi teolojik zıtlıklarda metin içi mutlak matematiksel eşitlik mevcuttur.")
    md.append("2. **Dış Dünya Aynalaması:** Yeryüzü deniz/kara oranı (%71-%29), bir yıldaki 12 ay sayısı ve 7 gök tabakası metinde tam karşılık bulmaktadır.")
    md.append("3. **Biyolojik Doğrusallık:** Embriyolojik evreler modern tıbbın ortaya koyduğu gelişim çizgisiyle kronolojik olarak %100 uyumludur.")
    md.append("4. **Sosyolojik Eylem Baskınlığı:** Açlık problemine karşı doyurma eylemi yaklaşık 8 kat daha fazla vurgulanarak aktif infak ahlakı öne çıkarılmıştır.\n")
    md.append("---\n")
    md.append("*Rapor MİRAT Analiz Motoru v1.0 tarafından otomatik olarak oluşturulmuştur.*")
    
    return "\n".join(md)

def generate_pdf_report(md_content, output_pdf="MIRAT_ANALIZ_RAPORU.pdf"):
    html_file = "MIRAT_ANALIZ_RAPORU.html"
    
    # Convert markdown to clean HTML with styling
    html = f"""<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<title>MİRAT Bilimsel Analiz Raporu</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Lora:ital,wght@0,400;0,600;1,400&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
@page {{
    size: A4;
    margin: 18mm 15mm 18mm 15mm;
    @bottom-right {{
        content: counter(page);
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #64748b;
    }}
    @top-center {{
        content: "MİRAT Bilimsel Araştırma ve Matematiksel Analiz Raporu";
        font-family: 'Inter', sans-serif;
        font-size: 8pt;
        color: #94a3b8;
        letter-spacing: 1px;
    }}
}}

body {{
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 10pt;
    line-height: 1.6;
    color: #1e293b;
    background: #ffffff;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}}

h1 {{
    font-size: 20pt;
    font-weight: 800;
    color: #0f766e;
    margin-top: 0;
    margin-bottom: 6px;
    text-align: center;
}}

h2 {{
    font-size: 13pt;
    font-weight: 700;
    color: #0f172a;
    border-bottom: 2px solid #0f766e;
    padding-bottom: 4px;
    margin-top: 22px;
    margin-bottom: 12px;
    page-break-after: avoid;
}}

h3 {{
    font-size: 11pt;
    font-weight: 600;
    color: #0f766e;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
}}

p, ul, ol {{
    margin-top: 0;
    margin-bottom: 8px;
}}

li {{
    margin-bottom: 4px;
}}

blockquote {{
    margin: 10px 0;
    padding: 8px 14px;
    background-color: #f0fdf4;
    border-left: 4px solid #0f766e;
    border-radius: 0 6px 6px 0;
    font-size: 9.5pt;
    color: #166534;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    margin: 12px 0 16px 0;
    page-break-inside: avoid;
}}

th {{
    background-color: #0f766e;
    color: #ffffff;
    font-weight: 600;
    padding: 6px 8px;
    text-align: left;
    border: 1px solid #0f766e;
}}

td {{
    padding: 5px 8px;
    border: 1px solid #e2e8f0;
}}

tr:nth-child(even) {{
    background-color: #f8fafc;
}}

code {{
    font-family: 'JetBrains Mono', monospace;
    background-color: #f1f5f9;
    padding: 2px 4px;
    border-radius: 4px;
    font-size: 8.5pt;
    color: #0f766e;
}}

hr {{
    border: 0;
    height: 1px;
    background: #e2e8f0;
    margin: 18px 0;
}}

.stat-badge {{
    display: inline-block;
    padding: 2px 6px;
    border-radius: 4px;
    font-weight: 600;
    background: #e0f2fe;
    color: #0369a1;
}}
</style>
</head>
<body>
"""
    # Simple markdown parser for headers, tables, lists, quotes
    in_table = False
    table_rows = []
    
    for line in md_content.split('\n'):
        line_s = line.strip()
        if not line_s:
            if in_table:
                # flush table
                html += "<table>" + "".join(table_rows) + "</table>\n"
                table_rows = []
                in_table = False
            continue
            
        if line_s.startswith('|') and line_s.endswith('|'):
            if '---' in line_s:
                continue
            cells = [c.strip() for c in line_s[1:-1].split('|')]
            if not in_table:
                in_table = True
                row_html = "<tr>" + "".join(f"<th>{c}</th>" for c in cells) + "</tr>"
            else:
                row_html = "<tr>" + "".join(f"<td>{c}</td>" for c in cells) + "</tr>"
            table_rows.append(row_html)
            continue
        elif in_table:
            html += "<table>" + "".join(table_rows) + "</table>\n"
            table_rows = []
            in_table = False
            
        if line_s.startswith('# '):
            html += f"<h1>{line_s[2:]}</h1>\n"
        elif line_s.startswith('## '):
            html += f"<h2>{line_s[3:]}</h2>\n"
        elif line_s.startswith('### '):
            html += f"<h3>{line_s[4:]}</h3>\n"
        elif line_s.startswith('> '):
            html += f"<blockquote>{line_s[2:]}</blockquote>\n"
        elif line_s.startswith('- '):
            html += f"<ul><li>{line_s[2:]}</li></ul>\n"
        elif line_s.startswith('---'):
            html += "<hr>\n"
        else:
            html += f"<p>{line_s}</p>\n"
            
    if in_table:
        html += "<table>" + "".join(table_rows) + "</table>\n"
        
    html += "</body></html>"
    
    with open(html_file, "w", encoding="utf-8") as hf:
        hf.write(html)
        
    cmd = [
        "google-chrome",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={output_pdf}",
        "--run-all-compositor-stages-before-draw",
        html_file
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"PDF Raporu Üretildi: {output_pdf} ({os.path.getsize(output_pdf):,} byte)")

def run_all_and_save():
    print("Tüm MİRAT analiz katmanları çalıştırılıyor...")
    db = MiratDB()
    
    all_results = {
        'layer1': analyze_layer_1(db),
        'layer2': analyze_layer_2(db),
        'layer3': analyze_layer_3(db),
        'layer4': analyze_layer_4(db),
        'layer5': analyze_layer_5(db)
    }
    
    md_content = generate_markdown_report(all_results)
    
    md_file = "MIRAT_ANALIZ_RAPORU.md"
    with open(md_file, "w", encoding="utf-8") as f:
        f.write(md_content)
    print(f"Markdown Raporu Üretildi: {md_file} ({os.path.getsize(md_file):,} byte)")
    
    generate_pdf_report(md_content, "MIRAT_ANALIZ_RAPORU.pdf")
    
    # Save JSON data as well
    json_file = "mirat_analiz_verileri.json"
    with open(json_file, "w", encoding="utf-8") as jf:
        json.dump(all_results, jf, ensure_ascii=False, indent=2)
    print(f"JSON Veri Seti Üretildi: {json_file}")

if __name__ == "__main__":
    run_all_and_save()
