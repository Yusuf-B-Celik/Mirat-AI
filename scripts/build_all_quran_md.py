#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kur'an-ı Kerim Çoklu Markdown Formatı Oluşturucu:
1. KURAN-I_KERIM_ARAPCA.md (Orijinal Osmanî Arapça Mushaf-ı Şerif)
2. arapca_sureler/ (114 Adet Salt Arapça Sure Dosyası)
3. cuzler/ (30 Cüz Dosyası - Hem Arapça hem Türkçe Meal ile)
4. KURAN-I_KERIM_SADECE_MEAL.md (Salt Akıcı Türkçe Meal Kitabı)
5. KURAN-I_KERIM_MEALI.md (Arapça + Okunuş + Meal Külliyatı)
"""

import os
import re
import json
from build_quran_markdown import (
    SURAH_METADATA, fetch_json_with_retry, clean_arabic_ayah, get_surah_filename
)

def to_arabic_num(n):
    mapping = str.maketrans("0123456789", "٠١٢٣٤٥٦٧٨٩")
    return str(n).translate(mapping)

def get_surah_ar_filename(s_num, name_tr):
    clean = name_tr.replace(" ", "_").replace("'", "").replace("(", "").replace(")", "")
    accents = {
        "â": "a", "î": "i", "û": "u",
        "Â": "A", "Î": "I", "Û": "U"
    }
    for k, v in accents.items():
        clean = clean.replace(k, v)
    return f"{s_num:03d}_{clean}_Ar.md"

def build_all():
    print("Kur'an-ı Kerim verileri yükleniyor...")
    
    uthmani_data = fetch_json_with_retry('http://api.alquran.cloud/v1/quran/quran-uthmani')['data']['surahs']
    trans_data = fetch_json_with_retry('http://api.alquran.cloud/v1/quran/tr.transliteration')['data']['surahs']
    vakfi_data = fetch_json_with_retry('http://api.alquran.cloud/v1/quran/tr.vakfi')['data']['surahs']
    
    os.makedirs("arapca_sureler", exist_ok=True)
    os.makedirs("cuzler", exist_ok=True)
    os.makedirs("sureler", exist_ok=True)
    
    # -------------------------------------------------------------
    # 1. KURAN-I_KERIM_ARAPCA.md & arapca_sureler/
    # -------------------------------------------------------------
    print("1. Arapça Mushaf Markdown dosyaları oluşturuluyor...")
    ar_master_lines = []
    ar_master_lines.append("# القُرْآن الكَرِيم (Kur'an-ı Kerîm - Arapça Mushaf)\n")
    ar_master_lines.append("> **الرَّسْم العُثْمَانِيّ المُنَقَّط وَالمَشْكُول (Harekeli Osmanî Mushaf Hattı)**\n")
    ar_master_lines.append("---\n")
    
    # Arapça Fihrist
    ar_master_lines.append("## فِهْرِس السُّوَر (Sure Fihristi)\n")
    ar_master_lines.append("| No | السورة (Sure Adı) | النزول (İniş) | آياتها (Ayet) | Türkçe Adı | Anlamı |")
    ar_master_lines.append("|:---:|:---|:---:|:---:|:---|:---|")
    
    for s_idx in range(114):
        s_num = s_idx + 1
        meta = SURAH_METADATA[s_num]
        anchor = f"surah-ar-{s_num:03d}"
        place_ar = "مكية" if meta['place'] == "Mekke" else "مدنية"
        row = f"| {s_num:03d} | [{meta['name_ar']}](#{anchor}) | {place_ar} | {meta['verses']} | {meta['name_tr']} | {meta['meaning']} |"
        ar_master_lines.append(row)
        
    ar_master_lines.append("\n---\n")
    
    for s_idx in range(114):
        s_num = s_idx + 1
        meta = SURAH_METADATA[s_num]
        ar_surah = uthmani_data[s_idx]
        num_ayahs = len(ar_surah['ayahs'])
        
        anchor = f"surah-ar-{s_num:03d}"
        place_ar = "مَكِّيَّة" if meta['place'] == "Mekke" else "مَدَنِيَّة"
        
        # Surah Header
        header_block = f"""<a id="{anchor}"></a>
# {s_num}. {meta['name_ar']} ({meta['name_tr']} Suresi)

> **{place_ar} • عدد الآيات: {meta['verses']} • {meta['juz']}**  
> **Türkçe Anlamı:** {meta['meaning']} | **Nüzul Sırası:** {meta['order']}

---
"""
        ar_master_lines.append(header_block)
        
        # Single surah file lines
        ar_single_lines = [header_block]
        
        # Navigation in single surah
        prev_f = get_surah_ar_filename(s_num - 1, SURAH_METADATA[s_num - 1]['name_tr']) if s_num > 1 else ""
        next_f = get_surah_ar_filename(s_num + 1, SURAH_METADATA[s_num + 1]['name_tr']) if s_num < 114 else ""
        nav_ar = ["[🏠 Ana Dizin](../README.md)", "[📚 Bütün Sureler (Arapça)](../KURAN-I_KERIM_ARAPCA.md)"]
        if prev_f: nav_ar.append(f"[← Önceki Sure]({prev_f})")
        if next_f: nav_ar.append(f"[Sonraki Sure →]({next_f})")
        ar_single_lines.append(" | ".join(nav_ar) + "\n\n---\n")
        
        # Bismillah
        if s_num != 9 and s_num != 1:
            besmele_text = "### بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ\n"
            ar_master_lines.append(besmele_text)
            ar_single_lines.append(besmele_text)
            
        # Verse stream (Mushaf format)
        surah_verse_parts = []
        for a_idx in range(num_ayahs):
            a_num = a_idx + 1
            raw_ar = ar_surah['ayahs'][a_idx]['text']
            clean_ar = clean_arabic_ayah(s_num, a_num, raw_ar)
            sajda_mark = " ۩" if ar_surah['ayahs'][a_idx].get('sajda') else ""
            verse_str = f"{clean_ar}{sajda_mark} ﴿{to_arabic_num(a_num)}﴾"
            surah_verse_parts.append(verse_str)
            
        full_surah_text = "<div dir=\"rtl\" style=\"font-family: 'Amiri', serif; font-size: 1.5rem; line-height: 2.5; text-align: justify; padding: 15px 0;\">\n\n"
        full_surah_text += " ".join(surah_verse_parts)
        full_surah_text += "\n\n</div>\n"
        
        ar_master_lines.append(full_surah_text)
        ar_single_lines.append(full_surah_text)
        
        ar_master_lines.append("\n[Başa Dön ↑ (#فهرس-السور-sure-fihristi)](#فهرس-السور-sure-fihristi)\n\n---\n")
        ar_single_lines.append("\n" + " | ".join(nav_ar) + "\n")
        
        # Save individual arabic surah file
        ar_file_name = get_surah_ar_filename(s_num, meta['name_tr'])
        ar_file_path = os.path.join("arapca_sureler", ar_file_name)
        with open(ar_file_path, "w", encoding="utf-8") as asf:
            asf.write("\n".join(ar_single_lines))
            
    with open("KURAN-I_KERIM_ARAPCA.md", "w", encoding="utf-8") as amf:
        amf.write("\n".join(ar_master_lines))
        
    print("KURAN-I_KERIM_ARAPCA.md ve arapca_sureler/ oluşturuldu.")

    # -------------------------------------------------------------
    # 2. KURAN-I_KERIM_SADECE_MEAL.md (Salt Akıcı Türkçe Meal)
    # -------------------------------------------------------------
    print("2. Salt Türkçe Meal Markdown dosyası oluşturuluyor...")
    meal_only_lines = []
    meal_only_lines.append("# Kur'an-ı Kerim Yüce Meali (Salt Türkçe Metin)\n")
    meal_only_lines.append("> **Kesintisiz ve Akıcı Türkçe Meal Okuması İçin Özel Hazırlanmıştır**\n")
    meal_only_lines.append("---\n")
    
    meal_only_lines.append("## 📑 Sure Listesi (Fihrist)\n")
    meal_only_lines.append("| No | Sure Adı | Anlamı | İniş Yeri | Ayet Sayısı | Cüz |")
    meal_only_lines.append("|:---:|:---|:---|:---:|:---:|:---:|")
    for s_idx in range(114):
        s_num = s_idx + 1
        meta = SURAH_METADATA[s_num]
        meal_only_lines.append(f"| {s_num:03d} | [{meta['name_tr']} Suresi](#meal-sure-{s_num:03d}) | {meta['meaning']} | {meta['place']} | {meta['verses']} | {meta['juz']} |")
        
    meal_only_lines.append("\n---\n")
    
    for s_idx in range(114):
        s_num = s_idx + 1
        meta = SURAH_METADATA[s_num]
        tr_meal_surah = vakfi_data[s_idx]
        num_ayahs = len(tr_meal_surah['ayahs'])
        
        anchor = f"meal-sure-{s_num:03d}"
        meal_only_lines.append(f"<a id=\"{anchor}\"></a>")
        meal_only_lines.append(f"# {s_num}. {meta['name_tr']} Suresi ({meta['name_ar']})\n")
        meal_only_lines.append(f"> **Anlamı:** {meta['meaning']} | **İniş:** {meta['place']} | **Ayet:** {meta['verses']} | **Cüz:** {meta['juz']}\n")
        meal_only_lines.append(f"**Sure Hakkında:** {meta['summary']}\n")
        
        if s_num != 9 and s_num != 1:
            meal_only_lines.append("> *Rahmân ve Rahîm olan Allah'ın adıyla.*\n")
            
        for a_idx in range(num_ayahs):
            a_num = a_idx + 1
            meal_text = tr_meal_surah['ayahs'][a_idx]['text'].strip()
            meal_only_lines.append(f"**[{a_num}]** {meal_text}\n")
            
        meal_only_lines.append("\n[Başa Dön ↑](#sure-listesi-fihrist)\n\n---\n")
        
    with open("KURAN-I_KERIM_SADECE_MEAL.md", "w", encoding="utf-8") as smf:
        smf.write("\n".join(meal_only_lines))
        
    print("KURAN-I_KERIM_SADECE_MEAL.md oluşturuldu.")

    # -------------------------------------------------------------
    # 3. cuzler/ (30 Cüz Dosyaları)
    # -------------------------------------------------------------
    print("3. 30 Cüz Markdown dosyaları oluşturuluyor...")
    
    juz_ayahs = {j: [] for j in range(1, 31)}
    
    for s_idx in range(114):
        s_num = s_idx + 1
        meta = SURAH_METADATA[s_num]
        ar_surah = uthmani_data[s_idx]
        trans_surah = trans_data[s_idx]
        meal_surah = vakfi_data[s_idx]
        
        for a_idx in range(len(ar_surah['ayahs'])):
            a_num = a_idx + 1
            juz_num = ar_surah['ayahs'][a_idx].get('juz', 1)
            raw_ar = ar_surah['ayahs'][a_idx]['text']
            clean_ar = clean_arabic_ayah(s_num, a_num, raw_ar)
            tr_trans = trans_surah['ayahs'][a_idx]['text'].strip()
            tr_meal = meal_surah['ayahs'][a_idx]['text'].strip()
            page_num = ar_surah['ayahs'][a_idx].get('page', 1)
            sajda = ar_surah['ayahs'][a_idx].get('sajda', False)
            
            juz_ayahs[juz_num].append({
                'surah_num': s_num,
                'surah_name_tr': meta['name_tr'],
                'surah_name_ar': meta['name_ar'],
                'ayah_num': a_num,
                'arabic': clean_ar,
                'trans': tr_trans,
                'meal': tr_meal,
                'page': page_num,
                'sajda': sajda
            })
            
    for j_num in range(1, 31):
        j_lines = []
        j_lines.append(f"# Kur'an-ı Kerim {j_num}. Cüz (الجزء {to_arabic_num(j_num)})\n")
        
        prev_juz_link = f"[← {j_num-1}. Cüz]({j_num-1:02d}_Cuz.md)" if j_num > 1 else ""
        next_juz_link = f"[{j_num+1}. Cüz →]({j_num+1:02d}_Cuz.md)" if j_num < 30 else ""
        nav_juz = ["[🏠 Ana Dizin](../README.md)", "[📚 Bütün Sureler](../KURAN-I_KERIM_MEALI.md)"]
        if prev_juz_link: nav_juz.append(prev_juz_link)
        if next_juz_link: nav_juz.append(next_juz_link)
        
        j_lines.append(" | ".join(nav_juz) + "\n\n---\n")
        
        current_surah = None
        current_page = None
        
        for ay in juz_ayahs[j_num]:
            if ay['surah_num'] != current_surah:
                current_surah = ay['surah_num']
                j_lines.append(f"\n## {current_surah}. {ay['surah_name_tr']} Suresi ({ay['surah_name_ar']})\n")
                if current_surah != 9 and current_surah != 1 and ay['ayah_num'] == 1:
                    j_lines.append("> **بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ**  \n> *Rahmân ve Rahîm olan Allah'ın adıyla.*\n\n---\n")
                    
            if ay['page'] != current_page:
                current_page = ay['page']
                j_lines.append(f"\n> 📄 *[Sayfa {current_page}]*\n")
                
            sajda_badge = " **[۩ Secde Ayeti]**" if ay['sajda'] else ""
            ayah_entry = f"""### [{ay['surah_num']}:{ay['ayah_num']}]{sajda_badge}
**Arapça:**
> {ay['arabic']}

**Okunuş:**
*{ay['trans']}*

**Meal:**
{ay['meal']}
---
"""
            j_lines.append(ayah_entry)
            
        j_lines.append("\n" + " | ".join(nav_juz) + "\n")
        
        juz_file_path = os.path.join("cuzler", f"{j_num:02d}_Cuz.md")
        with open(juz_file_path, "w", encoding="utf-8") as jf:
            jf.write("\n".join(j_lines))
            
    print("30 Cüz dosyası cuzler/ altında oluşturuldu.")

    # -------------------------------------------------------------
    # 4. Update README.md with all formats
    # -------------------------------------------------------------
    print("README.md güncelleniyor...")
    readme_lines = []
    readme_lines.append("# Kur'an-ı Kerim Dijital Külliyatı (Markdown & PDF)\n")
    readme_lines.append("Bu proje; Yüce Kitabımız **Kur'an-ı Kerim**'in 114 suresini ve 6.236 ayetini farklı kullanım ihtiyaçlarına göre hazırlanmış kapsamlı dijital formatlarda sunar.\n")
    readme_lines.append("## 📚 Külliyatın Dosya ve Format Yapısı\n")
    readme_lines.append("| Eser / Format | Dosya Yolu | Açıklama |")
    readme_lines.append("|:---|:---|:---|")
    readme_lines.append("| 📕 **Baskı Kalitesinde PDF** | [KURAN-I_KERIM_MEALI.pdf](KURAN-I_KERIM_MEALI.pdf) | 1.589 sayfalık, kapaklı, fihristli, Arapça hat ve Türkçe mealli tam PDF. |")
    readme_lines.append("| 📖 **Tam Mealli Külliyat (MD)** | [KURAN-I_KERIM_MEALI.md](KURAN-I_KERIM_MEALI.md) | Arapça + Okunuş + Meal içeren tek parça ana Markdown kitabı. |")
    readme_lines.append("| 📜 **Arapça Mushaf-ı Şerif (MD)** | [KURAN-I_KERIM_ARAPCA.md](KURAN-I_KERIM_ARAPCA.md) | Harekeli Osmanî hat ile ayet numaralı salt Arapça Kur'an metni. |")
    readme_lines.append("| 🇹🇷 **Salt Türkçe Meal (MD)** | [KURAN-I_KERIM_SADECE_MEAL.md](KURAN-I_KERIM_SADECE_MEAL.md) | Kesintisiz ve akıcı Türkçe meal okuması için salt Türkçe metin. |")
    readme_lines.append("| 📂 **Sure Sure Dosyalar (114 MD)** | [sureler/](sureler/) | Her surenin özel ayrılmış modüler Markdown dosyaları. |")
    readme_lines.append("| 📂 **Arapça Sureler (114 MD)** | [arapca_sureler/](arapca_sureler/) | 114 surenin ayrı ayrı salt Arapça Osmanî Mushaf dosyaları. |")
    readme_lines.append("| 🕋 **30 Cüz Dosyaları (30 MD)** | [cuzler/](cuzler/) | 1. Cüz'den 30. Cüz'e kadar cüz cüz düzenlenmiş Markdown dosyaları. |\n")
    
    readme_lines.append("## 🕋 30 Cüz Tablosu ve Hızlı Erişim\n")
    readme_lines.append("| Cüz No | Cüz Başlangıcı | Cüz Bitişi | Modüler Cüz Dosyası |")
    readme_lines.append("|:---:|:---|:---|:---:|")
    
    juz_boundaries = [
        (1, "1. Fâtiha 1", "2. Bakara 141"),
        (2, "2. Bakara 142", "2. Bakara 252"),
        (3, "2. Bakara 253", "3. Âl-i İmrân 92"),
        (4, "3. Âl-i İmrân 93", "4. Nisâ 23"),
        (5, "4. Nisâ 24", "4. Nisâ 147"),
        (6, "4. Nisâ 148", "5. Mâide 81"),
        (7, "5. Mâide 82", "6. En'âm 110"),
        (8, "6. En'âm 111", "7. A'râf 87"),
        (9, "7. A'râf 88", "8. Enfâl 40"),
        (10, "8. Enfâl 41", "9. Tevbe 92"),
        (11, "9. Tevbe 93", "11. Hûd 5"),
        (12, "11. Hûd 6", "12. Yûsuf 52"),
        (13, "12. Yûsuf 53", "14. İbrâhîm 52"),
        (14, "15. Hicr 1", "16. Nahl 128"),
        (15, "17. İsrâ 1", "18. Kehf 74"),
        (16, "18. Kehf 75", "20. Tâhâ 135"),
        (17, "21. Enbiyâ 1", "22. Hac 78"),
        (18, "23. Mü'minûn 1", "25. Furkân 20"),
        (19, "25. Furkân 21", "27. Neml 55"),
        (20, "27. Neml 56", "29. Ankebût 45"),
        (21, "29. Ankebût 46", "33. Ahzâb 30"),
        (22, "33. Ahzâb 31", "36. Yâsîn 27"),
        (23, "36. Yâsîn 28", "39. Zümer 31"),
        (24, "39. Zümer 32", "41. Fussilet 46"),
        (25, "41. Fussilet 47", "45. Câsiye 37"),
        (26, "46. Ahkâf 1", "51. Zâriyât 30"),
        (27, "51. Zâriyât 31", "57. Hadîd 29"),
        (28, "58. Mücâdele 1", "66. Tahrîm 12"),
        (29, "67. Mülk 1", "77. Mürselât 50"),
        (30, "78. Nebe' 1", "114. Nâs 6"),
    ]
    
    for j_num, start_a, end_a in juz_boundaries:
        readme_lines.append(f"| **{j_num:02d}. Cüz** | {start_a} | {end_a} | [📖 {j_num:02d}. Cüzü Oku](cuzler/{j_num:02d}_Cuz.md) |")
        
    readme_lines.append("\n---\n")
    readme_lines.append("## 📋 114 Sure Fihristi ve Doğrudan Erişim\n")
    readme_lines.append("| No | Sure Adı | Arapça | Anlamı | İniş | Sıra | Ayet | Cüz | Mealli Dosya | Arapça Dosya |")
    readme_lines.append("|:---:|:---|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|")
    
    for s_idx in range(114):
        s_num = s_idx + 1
        meta = SURAH_METADATA[s_num]
        clean_tr_name = get_surah_filename(s_num, meta['name_tr'])
        ar_file_name = get_surah_ar_filename(s_num, meta['name_tr'])
        readme_lines.append(f"| {s_num:03d} | **{meta['name_tr']}** | {meta['name_ar']} | {meta['meaning']} | {meta['place']} | {meta['order']} | {meta['verses']} | {meta['juz']} | [📄 Meal](sureler/{clean_tr_name}) | [📜 Arapça](arapca_sureler/{ar_file_name}) |")
        
    with open("README.md", "w", encoding="utf-8") as rf:
        rf.write("\n".join(readme_lines))
        
    print("Tüm Markdown külliyatı başarıyla tamamlandı!")

if __name__ == "__main__":
    build_all()
