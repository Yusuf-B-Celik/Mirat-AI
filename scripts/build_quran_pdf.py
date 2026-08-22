#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kur'an-ı Kerim Türkçe Meali PDF Üretici
Bu script, 114 surenin tamamını içeren yüksek kaliteli, şık ve tipografik olarak optimize edilmiş
baskı/okuma kalitesinde bir PDF dokümanı oluşturur.
"""

import json
import os
import subprocess
import time
from build_quran_markdown import SURAH_METADATA, fetch_json_with_retry, clean_arabic_ayah, get_surah_filename

HTML_TEMPLATE_HEADER = """<!DOCTYPE html>
<html lang="tr">
<head>
<meta charset="utf-8">
<title>Kur'an-ı Kerim ve Yüce Meali</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Amiri:ital,wght@0,400;0,700;1,400&family=Cinzel:wght@600;800&family=Lora:ital,wght@0,400;0,600;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
@page {
    size: A4;
    margin: 18mm 15mm 18mm 15mm;
    @bottom-right {
        content: counter(page);
        font-family: 'Inter', sans-serif;
        font-size: 9pt;
        color: #64748b;
    }
    @top-center {
        content: "Kur'an-ı Kerim ve Yüce Meali";
        font-family: 'Lora', serif;
        font-size: 8pt;
        color: #94a3b8;
        letter-spacing: 1px;
    }
}

*, *:before, *:after {
    box-sizing: border-box;
}

body {
    font-family: 'Lora', 'Georgia', serif;
    font-size: 11pt;
    line-height: 1.6;
    color: #1e293b;
    background-color: #ffffff;
    margin: 0;
    padding: 0;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
}

/* Cover Page */
.cover-page {
    page-break-before: always;
    page-break-after: always;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 40px 20px;
    border: 8px double #0f766e;
    border-radius: 12px;
    background: radial-gradient(circle at center, #ffffff 0%, #f0fdf4 100%);
    box-shadow: inset 0 0 40px rgba(15, 118, 110, 0.05);
}

.cover-bismillah {
    font-family: 'Amiri', serif;
    font-size: 32pt;
    color: #0f766e;
    margin-bottom: 30px;
    direction: rtl;
    line-height: 1.8;
}

.cover-title {
    font-family: 'Cinzel', 'Lora', serif;
    font-size: 28pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: 3px;
    margin: 10px 0;
    text-transform: uppercase;
}

.cover-subtitle {
    font-family: 'Inter', sans-serif;
    font-size: 13pt;
    font-weight: 500;
    color: #0f766e;
    margin-top: 15px;
    letter-spacing: 1px;
}

.cover-divider {
    width: 140px;
    height: 3px;
    background: linear-gradient(90deg, transparent, #0f766e, transparent);
    margin: 35px auto;
}

.cover-details {
    font-family: 'Inter', sans-serif;
    font-size: 10pt;
    color: #475569;
    line-height: 2;
    max-width: 480px;
}

.cover-footer {
    margin-top: 60px;
    font-family: 'Inter', sans-serif;
    font-size: 9pt;
    color: #64748b;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* Table of Contents */
.toc-page {
    page-break-before: always;
    page-break-after: always;
    padding: 10px 0;
}

.section-title {
    font-family: 'Cinzel', serif;
    font-size: 20pt;
    color: #0f766e;
    text-align: center;
    border-bottom: 2px solid #0f766e;
    padding-bottom: 8px;
    margin-bottom: 20px;
}

.toc-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.5pt;
    font-family: 'Inter', sans-serif;
}

.toc-table th {
    background-color: #0f766e;
    color: #ffffff;
    font-weight: 600;
    padding: 6px 8px;
    text-align: left;
    border: 1px solid #0f766e;
}

.toc-table td {
    padding: 5px 8px;
    border: 1px solid #e2e8f0;
}

.toc-table tr:nth-child(even) {
    background-color: #f8fafc;
}

.toc-arabic {
    font-family: 'Amiri', serif;
    font-size: 11pt;
    direction: rtl;
    text-align: right;
}

/* Surah Page */
.surah-container {
    page-break-before: always;
    padding-top: 10px;
    margin-bottom: 30px;
}

.surah-header-card {
    border: 2px solid #0f766e;
    border-radius: 8px;
    background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);
    padding: 16px 20px;
    margin-bottom: 20px;
    text-align: center;
    page-break-inside: avoid;
}

.surah-title-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #cbd5e1;
    padding-bottom: 10px;
    margin-bottom: 10px;
}

.surah-title-tr {
    font-family: 'Lora', serif;
    font-size: 18pt;
    font-weight: 700;
    color: #0f172a;
    text-align: left;
}

.surah-title-ar {
    font-family: 'Amiri', serif;
    font-size: 22pt;
    font-weight: 700;
    color: #0f766e;
    direction: rtl;
}

.surah-meta-badges {
    display: flex;
    justify-content: center;
    flex-wrap: wrap;
    gap: 8px;
    font-family: 'Inter', sans-serif;
    font-size: 8.5pt;
    color: #334155;
    margin-bottom: 10px;
}

.meta-badge {
    background-color: #e2e8f0;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: 500;
}

.meta-badge strong {
    color: #0f766e;
}

.surah-summary-box {
    font-size: 9.5pt;
    color: #475569;
    line-height: 1.5;
    text-align: justify;
    background: rgba(255, 255, 255, 0.8);
    border-left: 3px solid #0f766e;
    padding: 8px 12px;
    border-radius: 0 4px 4px 0;
}

.bismillah-card {
    text-align: center;
    padding: 14px;
    margin: 15px 0 25px 0;
    background: #fdfaf6;
    border-top: 1px dashed #cbd5e1;
    border-bottom: 1px dashed #cbd5e1;
    page-break-inside: avoid;
}

.bismillah-ar {
    font-family: 'Amiri', serif;
    font-size: 20pt;
    color: #0f766e;
    direction: rtl;
    margin-bottom: 4px;
}

.bismillah-tr {
    font-size: 9.5pt;
    font-style: italic;
    color: #64748b;
}

/* Ayah Card */
.ayah-card {
    margin-bottom: 16px;
    padding: 12px 16px;
    border-bottom: 1px solid #e2e8f0;
    page-break-inside: avoid;
}

.ayah-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 8px;
}

.ayah-badge {
    font-family: 'Inter', sans-serif;
    font-size: 8pt;
    font-weight: 700;
    background-color: #0f766e;
    color: #ffffff;
    padding: 2px 7px;
    border-radius: 12px;
    letter-spacing: 0.5px;
}

.ayah-ar {
    font-family: 'Amiri', 'Traditional Arabic', 'Scheherazade', serif;
    font-size: 16pt;
    line-height: 2.2;
    direction: rtl;
    text-align: right;
    color: #0f172a;
    margin-bottom: 6px;
    font-weight: 500;
}

.ayah-trans {
    font-family: 'Lora', serif;
    font-size: 9.5pt;
    font-style: italic;
    color: #64748b;
    margin-bottom: 6px;
    line-height: 1.4;
}

.ayah-meal {
    font-family: 'Lora', serif;
    font-size: 10.5pt;
    color: #1e293b;
    line-height: 1.6;
    text-align: justify;
}
</style>
</head>
<body>
"""

def generate_pdf():
    print("PDF oluşturma başlatılıyor...")
    
    # 1. Arabic Uthmani
    print("1. Osmanî Arapça metin çekiliyor...")
    uthmani_data = fetch_json_with_retry('http://api.alquran.cloud/v1/quran/quran-uthmani')['data']['surahs']
    
    # 2. Turkish Transliteration
    print("2. Türkçe Okunuş çekiliyor...")
    trans_data = fetch_json_with_retry('http://api.alquran.cloud/v1/quran/tr.transliteration')['data']['surahs']
    
    # 3. Turkish Translation (Diyanet)
    print("3. Türkçe Meal çekiliyor...")
    diyanet_data = fetch_json_with_retry('http://api.alquran.cloud/v1/quran/tr.vakfi')['data']['surahs']
    
    html_parts = [HTML_TEMPLATE_HEADER]
    
    # Cover Page
    cover_html = """
    <div class="cover-page">
        <div class="cover-bismillah">بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ</div>
        <div class="cover-title">Kur'an-ı Kerim<br><span style="font-size: 20pt; color: #0f766e;">ve Yüce Meali</span></div>
        <div class="cover-subtitle">Arapça Metin • Türkçe Okunuş • Akıcı Türkçe Meal</div>
        <div class="cover-divider"></div>
        <div class="cover-details">
            Bu eser, Kur'an-ı Kerim'in 114 suresini ve 6.236 ayetini eksiksiz olarak ihtiva eden,
            duru, akıcı ve edebi bir Türkçe üslupla hazırlanmış dijital külliyattır.
        </div>
        <div class="cover-footer">
            Mirat-AI Yayınları • 1446 / 2026
        </div>
    </div>
    """
    html_parts.append(cover_html)
    
    # Table of Contents
    toc_html = ["""
    <div class="toc-page">
        <div class="section-title">İçindekiler / Fihrist</div>
        <table class="toc-table">
            <thead>
                <tr>
                    <th style="width: 35px; text-align: center;">No</th>
                    <th>Sure Adı</th>
                    <th style="text-align: right;">Arapça</th>
                    <th>Anlamı</th>
                    <th>İniş</th>
                    <th style="text-align: center;">Ayet</th>
                    <th>Cüz</th>
                </tr>
            </thead>
            <tbody>
    """]
    
    for s_idx in range(114):
        s_num = s_idx + 1
        meta = SURAH_METADATA[s_num]
        toc_row = f"""
            <tr>
                <td style="text-align: center; font-weight: bold;">{s_num:03d}</td>
                <td><strong>{meta['name_tr']}</strong></td>
                <td class="toc-arabic">{meta['name_ar']}</td>
                <td>{meta['meaning']}</td>
                <td>{meta['place']}</td>
                <td style="text-align: center;">{meta['verses']}</td>
                <td>{meta['juz']}</td>
            </tr>
        """
        toc_html.append(toc_row)
        
    toc_html.append("""
            </tbody>
        </table>
    </div>
    """)
    html_parts.append("".join(toc_html))
    
    # Surahs
    print("Sureler HTML formatında derleniyor...")
    for s_idx in range(114):
        s_num = s_idx + 1
        meta = SURAH_METADATA[s_num]
        
        ar_surah = uthmani_data[s_idx]
        tr_trans_surah = trans_data[s_idx]
        tr_meal_surah = diyanet_data[s_idx]
        
        num_ayahs = len(ar_surah['ayahs'])
        
        surah_html = [f"""
        <div class="surah-container">
            <div class="surah-header-card">
                <div class="surah-title-row">
                    <div class="surah-title-tr">{s_num}. {meta['name_tr']} Suresi</div>
                    <div class="surah-title-ar">{meta['name_ar']}</div>
                </div>
                <div class="surah-meta-badges">
                    <span class="meta-badge"><strong>Anlamı:</strong> {meta['meaning']}</span>
                    <span class="meta-badge"><strong>İniş Yeri:</strong> {meta['place']}</span>
                    <span class="meta-badge"><strong>Nüzul Sırası:</strong> {meta['order']}</span>
                    <span class="meta-badge"><strong>Ayet Sayısı:</strong> {meta['verses']}</span>
                    <span class="meta-badge"><strong>Cüz:</strong> {meta['juz']}</span>
                </div>
                <div class="surah-summary-box">
                    <strong>Sure Hakkında:</strong> {meta['summary']}
                </div>
            </div>
        """]
        
        # Bismillah
        if s_num != 9 and s_num != 1:
            surah_html.append("""
            <div class="bismillah-card">
                <div class="bismillah-ar">بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ</div>
                <div class="bismillah-tr">Rahmân ve Rahîm olan Allah'ın adıyla.</div>
            </div>
            """)
        elif s_num == 9:
            surah_html.append("""
            <div class="bismillah-card" style="font-style: italic; color: #64748b; font-size: 9pt;">
                (Tevbe Suresi'nin başında Besmele bulunmamaktadır.)
            </div>
            """)
            
        # Ayahs
        for a_idx in range(num_ayahs):
            a_num = a_idx + 1
            raw_ar = ar_surah['ayahs'][a_idx]['text']
            ar_text = clean_arabic_ayah(s_num, a_num, raw_ar)
            tr_trans = tr_trans_surah['ayahs'][a_idx]['text'].strip()
            tr_meal = tr_meal_surah['ayahs'][a_idx]['text'].strip()
            
            ayah_card = f"""
            <div class="ayah-card">
                <div class="ayah-header">
                    <span class="ayah-badge">{s_num}:{a_num}</span>
                </div>
                <div class="ayah-ar">{ar_text}</div>
                <div class="ayah-trans">{tr_trans}</div>
                <div class="ayah-meal">{tr_meal}</div>
            </div>
            """
            surah_html.append(ayah_card)
            
        surah_html.append("</div>")
        html_parts.append("".join(surah_html))
        
    html_parts.append("</body></html>")
    
    html_content = "\n".join(html_parts)
    html_file = "KURAN-I_KERIM_MEALI.html"
    pdf_file = "KURAN-I_KERIM_MEALI.pdf"
    
    print(f"HTML dosyası yazılıyor: {html_file}...")
    with open(html_file, "w", encoding="utf-8") as hf:
        hf.write(html_content)
        
    print(f"HTML hazır ({os.path.getsize(html_file):,} byte). Chrome ile PDF'ye dönüştürülüyor...")
    
    cmd = [
        "google-chrome",
        "--headless",
        "--disable-gpu",
        "--no-sandbox",
        f"--print-to-pdf={pdf_file}",
        "--run-all-compositor-stages-before-draw",
        html_file
    ]
    
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print(f"Chrome PDF generation error: {res.stderr}")
    else:
        print(f"PDF Başarıyla Oluşturuldu: {pdf_file} ({os.path.getsize(pdf_file):,} byte)")

if __name__ == "__main__":
    generate_pdf()
