# 🏛️ MİRAT (Metin İçi Rastlantısallık ve Analiz Teknolojisi) & Kur'an-ı Kerim Dijital Külliyatı

> **Kur'an-ı Kerim Morfolojik Veritabanı, Matematiksel/Bilimsel Örüntü Madenciliği ve Kapsamlı Dijital Külliyatı (Markdown & PDF)**

---

## 🔬 MİRAT Morfolojik Analiz ve Örüntü Madenciliği Motoru

MİRAT, *Quranic Arabic Corpus* morfolojik veritabanını SQLite üzerinde yapılandırarak ayet, kelime, kök (root) ve lemma bazında çok katmanlı matematiksel, istatistiksel ve anlambilimsel analizler gerçekleştiren açık kaynaklı bir araştırma platformudur.

### 🌟 MİRAT Analiz Katmanları:
- 🌍 **Katman 1 (Jeoloji & Hidroloji)**: Deniz/Kara oranları, su döngüsü ve yer kabuğu kelime frekans dağılımları.
- 🌌 **Katman 2 (Kozmik & Astronomi)**: Güneş, ay, yörünge, gece/gündüz ve zaman döngülerinin matematiksel dengesi.
- ⚖️ **Katman 3 (Ahlak & Teoloji)**: Dünya / Ahiret, Melek / Şeytan gibi karşıt kavram simetrileri ve z-skoru / ki-kare anlamlılık testleri.
- 🏛️ **Katman 4 (Sosyoekonomik & Hukuk)**: Zekat, infak, adalet ve toplum düzeni terimlerinin korelasyonu.
- 🧬 **Katman 5 (Biyoloji & İnsan)**: Embriyoloji, yaratılış aşamaları ve genetik/biyolojik terim dağılımı.

### 💻 MİRAT CLI Kullanımı:
```bash
# 1. 100+ Örüntü içeren dev madencilik kataloğunu çalıştırın ve raporları derleyin:
python3 mirat_cli.py --mine

# 2. Tüm 5 temel analiz katmanını çalıştırın:
python3 mirat_cli.py --all

# 3. Belirli bir Arapça kökü ve frekansını sorgulayın:
python3 mirat_cli.py --root بحر

# 4. İki kavram kökünü istatistiksel olarak karşılaştırın:
python3 mirat_cli.py --compare دني اخر

# 5. Birim testlerini çalıştırın:
python3 -m unittest discover tests
```

---

## 📚 Kur'an-ı Kerim Dijital Külliyatı (Markdown & PDF)

Bu proje aynı zamanda; Yüce Kitabımız **Kur'an-ı Kerim**'in 114 suresini ve 6.236 ayetini farklı kullanım ihtiyaçlarına göre hazırlanmış kapsamlı dijital formatlarda sunar.

## 📚 Külliyatın Dosya ve Format Yapısı

| Eser / Format | Dosya Yolu | Açıklama |
|:---|:---|:---|
| 📕 **Baskı Kalitesinde PDF** | [KURAN-I_KERIM_MEALI.pdf](KURAN-I_KERIM_MEALI.pdf) | 1.589 sayfalık, kapaklı, fihristli, Arapça hat ve Türkçe mealli tam PDF. |
| 📖 **Tam Mealli Külliyat (MD)** | [KURAN-I_KERIM_MEALI.md](KURAN-I_KERIM_MEALI.md) | Arapça + Okunuş + Meal içeren tek parça ana Markdown kitabı. |
| 📜 **Arapça Mushaf-ı Şerif (MD)** | [KURAN-I_KERIM_ARAPCA.md](KURAN-I_KERIM_ARAPCA.md) | Harekeli Osmanî hat ile ayet numaralı salt Arapça Kur'an metni. |
| 🇹🇷 **Salt Türkçe Meal (MD)** | [KURAN-I_KERIM_SADECE_MEAL.md](KURAN-I_KERIM_SADECE_MEAL.md) | Kesintisiz ve akıcı Türkçe meal okuması için salt Türkçe metin. |
| 📂 **Sure Sure Dosyalar (114 MD)** | [sureler/](sureler/) | Her surenin özel ayrılmış modüler Markdown dosyaları. |
| 📂 **Arapça Sureler (114 MD)** | [arapca_sureler/](arapca_sureler/) | 114 surenin ayrı ayrı salt Arapça Osmanî Mushaf dosyaları. |
| 🕋 **30 Cüz Dosyaları (30 MD)** | [cuzler/](cuzler/) | 1. Cüz'den 30. Cüz'e kadar cüz cüz düzenlenmiş Markdown dosyaları. |

## 🕋 30 Cüz Tablosu ve Hızlı Erişim

| Cüz No | Cüz Başlangıcı | Cüz Bitişi | Modüler Cüz Dosyası |
|:---:|:---|:---|:---:|
| **01. Cüz** | 1. Fâtiha 1 | 2. Bakara 141 | [📖 01. Cüzü Oku](cuzler/01_Cuz.md) |
| **02. Cüz** | 2. Bakara 142 | 2. Bakara 252 | [📖 02. Cüzü Oku](cuzler/02_Cuz.md) |
| **03. Cüz** | 2. Bakara 253 | 3. Âl-i İmrân 92 | [📖 03. Cüzü Oku](cuzler/03_Cuz.md) |
| **04. Cüz** | 3. Âl-i İmrân 93 | 4. Nisâ 23 | [📖 04. Cüzü Oku](cuzler/04_Cuz.md) |
| **05. Cüz** | 4. Nisâ 24 | 4. Nisâ 147 | [📖 05. Cüzü Oku](cuzler/05_Cuz.md) |
| **06. Cüz** | 4. Nisâ 148 | 5. Mâide 81 | [📖 06. Cüzü Oku](cuzler/06_Cuz.md) |
| **07. Cüz** | 5. Mâide 82 | 6. En'âm 110 | [📖 07. Cüzü Oku](cuzler/07_Cuz.md) |
| **08. Cüz** | 6. En'âm 111 | 7. A'râf 87 | [📖 08. Cüzü Oku](cuzler/08_Cuz.md) |
| **09. Cüz** | 7. A'râf 88 | 8. Enfâl 40 | [📖 09. Cüzü Oku](cuzler/09_Cuz.md) |
| **10. Cüz** | 8. Enfâl 41 | 9. Tevbe 92 | [📖 10. Cüzü Oku](cuzler/10_Cuz.md) |
| **11. Cüz** | 9. Tevbe 93 | 11. Hûd 5 | [📖 11. Cüzü Oku](cuzler/11_Cuz.md) |
| **12. Cüz** | 11. Hûd 6 | 12. Yûsuf 52 | [📖 12. Cüzü Oku](cuzler/12_Cuz.md) |
| **13. Cüz** | 12. Yûsuf 53 | 14. İbrâhîm 52 | [📖 13. Cüzü Oku](cuzler/13_Cuz.md) |
| **14. Cüz** | 15. Hicr 1 | 16. Nahl 128 | [📖 14. Cüzü Oku](cuzler/14_Cuz.md) |
| **15. Cüz** | 17. İsrâ 1 | 18. Kehf 74 | [📖 15. Cüzü Oku](cuzler/15_Cuz.md) |
| **16. Cüz** | 18. Kehf 75 | 20. Tâhâ 135 | [📖 16. Cüzü Oku](cuzler/16_Cuz.md) |
| **17. Cüz** | 21. Enbiyâ 1 | 22. Hac 78 | [📖 17. Cüzü Oku](cuzler/17_Cuz.md) |
| **18. Cüz** | 23. Mü'minûn 1 | 25. Furkân 20 | [📖 18. Cüzü Oku](cuzler/18_Cuz.md) |
| **19. Cüz** | 25. Furkân 21 | 27. Neml 55 | [📖 19. Cüzü Oku](cuzler/19_Cuz.md) |
| **20. Cüz** | 27. Neml 56 | 29. Ankebût 45 | [📖 20. Cüzü Oku](cuzler/20_Cuz.md) |
| **21. Cüz** | 29. Ankebût 46 | 33. Ahzâb 30 | [📖 21. Cüzü Oku](cuzler/21_Cuz.md) |
| **22. Cüz** | 33. Ahzâb 31 | 36. Yâsîn 27 | [📖 22. Cüzü Oku](cuzler/22_Cuz.md) |
| **23. Cüz** | 36. Yâsîn 28 | 39. Zümer 31 | [📖 23. Cüzü Oku](cuzler/23_Cuz.md) |
| **24. Cüz** | 39. Zümer 32 | 41. Fussilet 46 | [📖 24. Cüzü Oku](cuzler/24_Cuz.md) |
| **25. Cüz** | 41. Fussilet 47 | 45. Câsiye 37 | [📖 25. Cüzü Oku](cuzler/25_Cuz.md) |
| **26. Cüz** | 46. Ahkâf 1 | 51. Zâriyât 30 | [📖 26. Cüzü Oku](cuzler/26_Cuz.md) |
| **27. Cüz** | 51. Zâriyât 31 | 57. Hadîd 29 | [📖 27. Cüzü Oku](cuzler/27_Cuz.md) |
| **28. Cüz** | 58. Mücâdele 1 | 66. Tahrîm 12 | [📖 28. Cüzü Oku](cuzler/28_Cuz.md) |
| **29. Cüz** | 67. Mülk 1 | 77. Mürselât 50 | [📖 29. Cüzü Oku](cuzler/29_Cuz.md) |
| **30. Cüz** | 78. Nebe' 1 | 114. Nâs 6 | [📖 30. Cüzü Oku](cuzler/30_Cuz.md) |

---

## 📋 114 Sure Fihristi ve Doğrudan Erişim

| No | Sure Adı | Arapça | Anlamı | İniş | Sıra | Ayet | Cüz | Mealli Dosya | Arapça Dosya |
|:---:|:---|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|
| 001 | **Fâtiha** | سُورَةُ الفَاتِحَةِ | Açılış, Başlangıç | Mekke | 5 | 7 | 1. Cüz | [📄 Meal](sureler/001_Fatiha.md) | [📜 Arapça](arapca_sureler/001_Fatiha_Ar.md) |
| 002 | **Bakara** | سُورَةُ البَقَرَةِ | Sığır, İnek | Medine | 87 | 286 | 1, 2, 3. Cüz | [📄 Meal](sureler/002_Bakara.md) | [📜 Arapça](arapca_sureler/002_Bakara_Ar.md) |
| 003 | **Âl-i İmrân** | سُورَةُ آلِ عِمْرَانَ | İmrân Ailesi | Medine | 89 | 200 | 3, 4. Cüz | [📄 Meal](sureler/003_Al-i_İmran.md) | [📜 Arapça](arapca_sureler/003_Al-i_İmran_Ar.md) |
| 004 | **Nisâ** | سُورَةُ النِّسَاءِ | Kadınlar | Medine | 92 | 176 | 4, 5, 6. Cüz | [📄 Meal](sureler/004_Nisa.md) | [📜 Arapça](arapca_sureler/004_Nisa_Ar.md) |
| 005 | **Mâide** | سُورَةُ المَائِدَةِ | Donatılmış Sofra | Medine | 112 | 120 | 6, 7. Cüz | [📄 Meal](sureler/005_Maide.md) | [📜 Arapça](arapca_sureler/005_Maide_Ar.md) |
| 006 | **En'âm** | سُورَةُ الأَنْعَامِ | Ehli Hayvanlar (Davarlar) | Mekke | 55 | 165 | 7, 8. Cüz | [📄 Meal](sureler/006_Enam.md) | [📜 Arapça](arapca_sureler/006_Enam_Ar.md) |
| 007 | **A'râf** | سُورَةُ الأَعْرَافِ | Yüksek Yerler, Tepe Noktaları | Mekke | 39 | 206 | 8, 9. Cüz | [📄 Meal](sureler/007_Araf.md) | [📜 Arapça](arapca_sureler/007_Araf_Ar.md) |
| 008 | **Enfâl** | سُورَةُ الأَنْفَالِ | Savaş Ganimetleri | Medine | 88 | 75 | 9, 10. Cüz | [📄 Meal](sureler/008_Enfal.md) | [📜 Arapça](arapca_sureler/008_Enfal_Ar.md) |
| 009 | **Tevbe** | سُورَةُ التَّوْبَةِ | Tövbe, Pişmanlık | Medine | 113 | 129 | 10, 11. Cüz | [📄 Meal](sureler/009_Tevbe.md) | [📜 Arapça](arapca_sureler/009_Tevbe_Ar.md) |
| 010 | **Yûnus** | سُورَةُ يُونُسَ | Hz. Yûnus Peygamber | Mekke | 51 | 109 | 11. Cüz | [📄 Meal](sureler/010_Yunus.md) | [📜 Arapça](arapca_sureler/010_Yunus_Ar.md) |
| 011 | **Hûd** | سُورَةُ هُودٍ | Hz. Hûd Peygamber | Mekke | 52 | 123 | 11, 12. Cüz | [📄 Meal](sureler/011_Hud.md) | [📜 Arapça](arapca_sureler/011_Hud_Ar.md) |
| 012 | **Yûsuf** | سُورَةُ يُوسُفَ | Hz. Yûsuf Peygamber | Mekke | 53 | 111 | 12, 13. Cüz | [📄 Meal](sureler/012_Yusuf.md) | [📜 Arapça](arapca_sureler/012_Yusuf_Ar.md) |
| 013 | **Ra'd** | سُورَةُ الرَّعْدِ | Gök Gürültüsü | Medine | 96 | 43 | 13. Cüz | [📄 Meal](sureler/013_Rad.md) | [📜 Arapça](arapca_sureler/013_Rad_Ar.md) |
| 014 | **İbrâhîm** | سُورَةُ إِبْرَاهِيمَ | Hz. İbrâhîm Peygamber | Mekke | 72 | 52 | 13. Cüz | [📄 Meal](sureler/014_İbrahim.md) | [📜 Arapça](arapca_sureler/014_İbrahim_Ar.md) |
| 015 | **Hicr** | سُورَةُ الحِجْرِ | Hicr Bölgesi (Semûd Kavmi Yurdu) | Mekke | 54 | 99 | 14. Cüz | [📄 Meal](sureler/015_Hicr.md) | [📜 Arapça](arapca_sureler/015_Hicr_Ar.md) |
| 016 | **Nahl** | سُورَةُ النَّحْلِ | Bal Arısı | Mekke | 70 | 128 | 14. Cüz | [📄 Meal](sureler/016_Nahl.md) | [📜 Arapça](arapca_sureler/016_Nahl_Ar.md) |
| 017 | **İsrâ** | سُورَةُ الإِسْرَاءِ | Gece Yürüyüşü | Mekke | 50 | 111 | 15. Cüz | [📄 Meal](sureler/017_İsra.md) | [📜 Arapça](arapca_sureler/017_İsra_Ar.md) |
| 018 | **Kehf** | سُورَةُ الكَهْفِ | Mağara | Mekke | 69 | 110 | 15, 16. Cüz | [📄 Meal](sureler/018_Kehf.md) | [📜 Arapça](arapca_sureler/018_Kehf_Ar.md) |
| 019 | **Meryem** | سُورَةُ مَرْيَمَ | Hz. Meryem | Mekke | 44 | 98 | 16. Cüz | [📄 Meal](sureler/019_Meryem.md) | [📜 Arapça](arapca_sureler/019_Meryem_Ar.md) |
| 020 | **Tâhâ** | سُورَةُ طه | Tâ-Hâ Harfleri | Mekke | 45 | 135 | 16. Cüz | [📄 Meal](sureler/020_Taha.md) | [📜 Arapça](arapca_sureler/020_Taha_Ar.md) |
| 021 | **Enbiyâ** | سُورَةُ الأَنْبِيَاءِ | Peygamberler | Mekke | 73 | 112 | 17. Cüz | [📄 Meal](sureler/021_Enbiya.md) | [📜 Arapça](arapca_sureler/021_Enbiya_Ar.md) |
| 022 | **Hac** | سُورَةُ الحَجِّ | Hac İbadeti | Medine | 103 | 78 | 17. Cüz | [📄 Meal](sureler/022_Hac.md) | [📜 Arapça](arapca_sureler/022_Hac_Ar.md) |
| 023 | **Mü'minûn** | سُورَةُ المُؤْمِنُونَ | Müminler, İnananlar | Mekke | 74 | 118 | 18. Cüz | [📄 Meal](sureler/023_Müminun.md) | [📜 Arapça](arapca_sureler/023_Müminun_Ar.md) |
| 024 | **Nûr** | سُورَةُ النُّورِ | İlahî Nur, Işık | Medine | 102 | 64 | 18. Cüz | [📄 Meal](sureler/024_Nur.md) | [📜 Arapça](arapca_sureler/024_Nur_Ar.md) |
| 025 | **Furkân** | سُورَةُ الفُرْقَانِ | Hak ile Bâtılı Ayıran | Mekke | 42 | 77 | 18, 19. Cüz | [📄 Meal](sureler/025_Furkan.md) | [📜 Arapça](arapca_sureler/025_Furkan_Ar.md) |
| 026 | **Şuarâ** | سُورَةُ الشُّعَرَاءِ | Şairler | Mekke | 47 | 227 | 19. Cüz | [📄 Meal](sureler/026_Şuara.md) | [📜 Arapça](arapca_sureler/026_Şuara_Ar.md) |
| 027 | **Neml** | سُورَةُ النَّمْلِ | Karınca | Mekke | 48 | 93 | 19, 20. Cüz | [📄 Meal](sureler/027_Neml.md) | [📜 Arapça](arapca_sureler/027_Neml_Ar.md) |
| 028 | **Kasas** | سُورَةُ القَصَصِ | Tarihî Kıssalar ve Anlatılar | Mekke | 49 | 88 | 20. Cüz | [📄 Meal](sureler/028_Kasas.md) | [📜 Arapça](arapca_sureler/028_Kasas_Ar.md) |
| 029 | **Ankebût** | سُورَةُ العَنْكَبُوتِ | Örümcek | Mekke | 85 | 69 | 20, 21. Cüz | [📄 Meal](sureler/029_Ankebut.md) | [📜 Arapça](arapca_sureler/029_Ankebut_Ar.md) |
| 030 | **Rûm** | سُورَةُ الرُّومِ | Romalılar (Bizans) | Mekke | 84 | 60 | 21. Cüz | [📄 Meal](sureler/030_Rum.md) | [📜 Arapça](arapca_sureler/030_Rum_Ar.md) |
| 031 | **Lokmân** | سُورَةُ لُقْمَانَ | Hz. Lokmân Hekim | Mekke | 57 | 34 | 21. Cüz | [📄 Meal](sureler/031_Lokman.md) | [📜 Arapça](arapca_sureler/031_Lokman_Ar.md) |
| 032 | **Secde** | سُورَةُ السَّجْدَةِ | Secde Etmek | Mekke | 75 | 30 | 21. Cüz | [📄 Meal](sureler/032_Secde.md) | [📜 Arapça](arapca_sureler/032_Secde_Ar.md) |
| 033 | **Ahzâb** | سُورَةُ الأَحْزَابِ | Gruplar, Birleşik Ordular | Medine | 90 | 73 | 21, 22. Cüz | [📄 Meal](sureler/033_Ahzab.md) | [📜 Arapça](arapca_sureler/033_Ahzab_Ar.md) |
| 034 | **Sebe'** | سُورَةُ سَبَإٍ | Sebe Kavmi / Diyarı | Mekke | 58 | 54 | 22. Cüz | [📄 Meal](sureler/034_Sebe.md) | [📜 Arapça](arapca_sureler/034_Sebe_Ar.md) |
| 035 | **Fâtır** | سُورَةُ فَاطِرٍ | Yoktan Yaratan, Var Eden | Mekke | 43 | 45 | 22. Cüz | [📄 Meal](sureler/035_Fatır.md) | [📜 Arapça](arapca_sureler/035_Fatır_Ar.md) |
| 036 | **Yâsîn** | سُورَةُ يس | Yâ-Sîn Harfleri | Mekke | 41 | 83 | 22, 23. Cüz | [📄 Meal](sureler/036_Yasin.md) | [📜 Arapça](arapca_sureler/036_Yasin_Ar.md) |
| 037 | **Sâffât** | سُورَةُ الصَّافَّاتِ | Sıra Sıra Dizilenler (Melekler) | Mekke | 56 | 182 | 23. Cüz | [📄 Meal](sureler/037_Saffat.md) | [📜 Arapça](arapca_sureler/037_Saffat_Ar.md) |
| 038 | **Sâd** | سُورَةُ ص | Sâd Harfi | Mekke | 38 | 88 | 23. Cüz | [📄 Meal](sureler/038_Sad.md) | [📜 Arapça](arapca_sureler/038_Sad_Ar.md) |
| 039 | **Zümer** | سُورَةُ الزُّمَرِ | Zümreler, Bölükler | Mekke | 59 | 75 | 23, 24. Cüz | [📄 Meal](sureler/039_Zümer.md) | [📜 Arapça](arapca_sureler/039_Zümer_Ar.md) |
| 040 | **Mü'min (Gâfir)** | سُورَةُ غَافِرٍ | İnanan Kişi / Günahları Bağışlayan | Mekke | 60 | 85 | 24. Cüz | [📄 Meal](sureler/040_Mümin_Gafir.md) | [📜 Arapça](arapca_sureler/040_Mümin_Gafir_Ar.md) |
| 041 | **Fussilet** | سُورَةُ فُصِّلَتْ | Ayrıntılı Olarak Açıklanmış | Mekke | 61 | 54 | 24, 25. Cüz | [📄 Meal](sureler/041_Fussilet.md) | [📜 Arapça](arapca_sureler/041_Fussilet_Ar.md) |
| 042 | **Şûrâ** | سُورَةُ الشُّورَى | Danışma, İstişare | Mekke | 62 | 53 | 25. Cüz | [📄 Meal](sureler/042_Şura.md) | [📜 Arapça](arapca_sureler/042_Şura_Ar.md) |
| 043 | **Zuhruf** | سُورَةُ الزُّخْرُفِ | Altın, Mücevher ve Yaldız | Mekke | 63 | 89 | 25. Cüz | [📄 Meal](sureler/043_Zuhruf.md) | [📜 Arapça](arapca_sureler/043_Zuhruf_Ar.md) |
| 044 | **Duhân** | سُورَةُ الدُّخَانِ | Duman | Mekke | 64 | 59 | 25. Cüz | [📄 Meal](sureler/044_Duhan.md) | [📜 Arapça](arapca_sureler/044_Duhan_Ar.md) |
| 045 | **Câsiye** | سُورَةُ الجَاثِيَةِ | Diz Üstü Çöken Topluluk | Mekke | 65 | 37 | 25. Cüz | [📄 Meal](sureler/045_Casiye.md) | [📜 Arapça](arapca_sureler/045_Casiye_Ar.md) |
| 046 | **Ahkâf** | سُورَةُ الأَحْقَافِ | Kum Tepeleri (Âd Kavmi Yurdu) | Mekke | 66 | 35 | 26. Cüz | [📄 Meal](sureler/046_Ahkaf.md) | [📜 Arapça](arapca_sureler/046_Ahkaf_Ar.md) |
| 047 | **Muhammed** | سُورَةُ مُحَمَّدٍ | Hz. Muhammed (s.a.v.) | Medine | 95 | 38 | 26. Cüz | [📄 Meal](sureler/047_Muhammed.md) | [📜 Arapça](arapca_sureler/047_Muhammed_Ar.md) |
| 048 | **Fetih** | سُورَةُ الفَتْحِ | Zafer, Açılış (Hudeybiye Barışı) | Medine | 111 | 29 | 26. Cüz | [📄 Meal](sureler/048_Fetih.md) | [📜 Arapça](arapca_sureler/048_Fetih_Ar.md) |
| 049 | **Hucurât** | سُورَةُ الحُجُرَاتِ | Odalar, Hücreler | Medine | 106 | 18 | 26. Cüz | [📄 Meal](sureler/049_Hucurat.md) | [📜 Arapça](arapca_sureler/049_Hucurat_Ar.md) |
| 050 | **Kâf** | سُورَةُ ق | Kâf Harfi | Mekke | 34 | 45 | 26. Cüz | [📄 Meal](sureler/050_Kaf.md) | [📜 Arapça](arapca_sureler/050_Kaf_Ar.md) |
| 051 | **Zâriyât** | سُورَةُ الذَّارِيَاتِ | Toz Kaldırıp Savuran Rüzgârlar | Mekke | 67 | 60 | 26, 27. Cüz | [📄 Meal](sureler/051_Zariyat.md) | [📜 Arapça](arapca_sureler/051_Zariyat_Ar.md) |
| 052 | **Tûr** | سُورَةُ الطُّورِ | Tur Dağı (Sînâ Dağı) | Mekke | 76 | 49 | 27. Cüz | [📄 Meal](sureler/052_Tur.md) | [📜 Arapça](arapca_sureler/052_Tur_Ar.md) |
| 053 | **Necm** | سُورَةُ النَّجْمِ | Kayan Yıldız | Mekke | 23 | 62 | 27. Cüz | [📄 Meal](sureler/053_Necm.md) | [📜 Arapça](arapca_sureler/053_Necm_Ar.md) |
| 054 | **Kamer** | سُورَةُ القَمَرِ | Ay | Mekke | 37 | 55 | 27. Cüz | [📄 Meal](sureler/054_Kamer.md) | [📜 Arapça](arapca_sureler/054_Kamer_Ar.md) |
| 055 | **Rahmân** | سُورَةُ الرَّحْمَٰنِ | Sonsuz Merhamet Sahibi Allah | Medine | 97 | 78 | 27. Cüz | [📄 Meal](sureler/055_Rahman.md) | [📜 Arapça](arapca_sureler/055_Rahman_Ar.md) |
| 056 | **Vâkı'a** | سُورَةُ الوَاقِعَةِ | Kesinlikle Gerçekleşecek Olan (Kıyamet) | Mekke | 46 | 96 | 27. Cüz | [📄 Meal](sureler/056_Vakıa.md) | [📜 Arapça](arapca_sureler/056_Vakıa_Ar.md) |
| 057 | **Hadîd** | سُورَةُ الحَدِيدِ | Demir | Medine | 94 | 29 | 27. Cüz | [📄 Meal](sureler/057_Hadid.md) | [📜 Arapça](arapca_sureler/057_Hadid_Ar.md) |
| 058 | **Mücâdele** | سُورَةُ المُجَادَلَةِ | Tartışan, Hakkını Arayan Kadın | Medine | 105 | 22 | 28. Cüz | [📄 Meal](sureler/058_Mücadele.md) | [📜 Arapça](arapca_sureler/058_Mücadele_Ar.md) |
| 059 | **Haşr** | سُورَةُ الحَشْرِ | Toplanma, Sürgün | Medine | 101 | 24 | 28. Cüz | [📄 Meal](sureler/059_Haşr.md) | [📜 Arapça](arapca_sureler/059_Haşr_Ar.md) |
| 060 | **Mümtehine** | سُورَةُ المُمْتَحَنَةِ | İmtihan Edilen Kadın | Medine | 91 | 13 | 28. Cüz | [📄 Meal](sureler/060_Mümtehine.md) | [📜 Arapça](arapca_sureler/060_Mümtehine_Ar.md) |
| 061 | **Saf** | سُورَةُ الصَّفِّ | Sıra Sıra Saf Tutmak | Medine | 109 | 14 | 28. Cüz | [📄 Meal](sureler/061_Saf.md) | [📜 Arapça](arapca_sureler/061_Saf_Ar.md) |
| 062 | **Cuma** | سُورَةُ الجُمُعَةِ | Cuma Günü ve Toplanma | Medine | 110 | 11 | 28. Cüz | [📄 Meal](sureler/062_Cuma.md) | [📜 Arapça](arapca_sureler/062_Cuma_Ar.md) |
| 063 | **Münâfikûn** | سُورَةُ المُنَافِقُونَ | İkiyüzlü Münafıklar | Medine | 104 | 11 | 28. Cüz | [📄 Meal](sureler/063_Münafikun.md) | [📜 Arapça](arapca_sureler/063_Münafikun_Ar.md) |
| 064 | **Tegâbün** | سُورَةُ التَّغَابُنِ | Aldanma ve Kâr-Zararın Ortaya Çıkması | Medine | 108 | 18 | 28. Cüz | [📄 Meal](sureler/064_Tegabün.md) | [📜 Arapça](arapca_sureler/064_Tegabün_Ar.md) |
| 065 | **Talâk** | سُورَةُ الطَّلَاقِ | Boşanma Hükümleri | Medine | 99 | 12 | 28. Cüz | [📄 Meal](sureler/065_Talak.md) | [📜 Arapça](arapca_sureler/065_Talak_Ar.md) |
| 066 | **Tahrîm** | سُورَةُ التَّحْرِيمِ | Haram Kılma, Men Etme | Medine | 107 | 12 | 28. Cüz | [📄 Meal](sureler/066_Tahrim.md) | [📜 Arapça](arapca_sureler/066_Tahrim_Ar.md) |
| 067 | **Mülk** | سُورَةُ المُلْكِ | Mülk, Hükümranlık (Tebâreke) | Mekke | 77 | 30 | 29. Cüz | [📄 Meal](sureler/067_Mülk.md) | [📜 Arapça](arapca_sureler/067_Mülk_Ar.md) |
| 068 | **Kalem** | سُورَةُ القَلَمِ | Kalem (Nûn) | Mekke | 2 | 52 | 29. Cüz | [📄 Meal](sureler/068_Kalem.md) | [📜 Arapça](arapca_sureler/068_Kalem_Ar.md) |
| 069 | **Hâkka** | سُورَةُ الحَاقَّةِ | Kaçınılmaz Hakikat (Kıyamet) | Mekke | 78 | 52 | 29. Cüz | [📄 Meal](sureler/069_Hakka.md) | [📜 Arapça](arapca_sureler/069_Hakka_Ar.md) |
| 070 | **Meâric** | سُورَةُ المَعَارِجِ | Yükselme Dereceleri ve Yolları | Mekke | 79 | 44 | 29. Cüz | [📄 Meal](sureler/070_Mearic.md) | [📜 Arapça](arapca_sureler/070_Mearic_Ar.md) |
| 071 | **Nûh** | سُورَةُ نُوحٍ | Hz. Nûh Peygamber | Mekke | 71 | 28 | 29. Cüz | [📄 Meal](sureler/071_Nuh.md) | [📜 Arapça](arapca_sureler/071_Nuh_Ar.md) |
| 072 | **Cin** | سُورَةُ الجِنِّ | Cin Varlıkları | Mekke | 40 | 28 | 29. Cüz | [📄 Meal](sureler/072_Cin.md) | [📜 Arapça](arapca_sureler/072_Cin_Ar.md) |
| 073 | **Müzzemmil** | سُورَةُ المُزَّمِّلِ | Örtünüp Bürünen (Hz. Peygamber) | Mekke | 3 | 20 | 29. Cüz | [📄 Meal](sureler/073_Müzzemmil.md) | [📜 Arapça](arapca_sureler/073_Müzzemmil_Ar.md) |
| 074 | **Müddessir** | سُورَةُ المُدَّثِّرِ | Örtüsüne Sarınan (Hz. Peygamber) | Mekke | 4 | 56 | 29. Cüz | [📄 Meal](sureler/074_Müddessir.md) | [📜 Arapça](arapca_sureler/074_Müddessir_Ar.md) |
| 075 | **Kıyâme** | سُورَةُ القِيَامَةِ | Kıyamet ve Diriliş Günü | Mekke | 31 | 40 | 29. Cüz | [📄 Meal](sureler/075_Kıyame.md) | [📜 Arapça](arapca_sureler/075_Kıyame_Ar.md) |
| 076 | **İnsân (Dehr)** | سُورَةُ الإِنْسَانِ | İnsan / Zaman | Medine | 98 | 31 | 29. Cüz | [📄 Meal](sureler/076_İnsan_Dehr.md) | [📜 Arapça](arapca_sureler/076_İnsan_Dehr_Ar.md) |
| 077 | **Mürselât** | سُورَةُ المُرْسَلَاتِ | Birbiri Ardınca Gönderilenler (Rüzgârlar / Melekler) | Mekke | 33 | 50 | 29. Cüz | [📄 Meal](sureler/077_Mürselat.md) | [📜 Arapça](arapca_sureler/077_Mürselat_Ar.md) |
| 078 | **Nebe'** | سُورَةُ النَّبَإِ | Büyük Haber (Amme) | Mekke | 80 | 40 | 30. Cüz | [📄 Meal](sureler/078_Nebe.md) | [📜 Arapça](arapca_sureler/078_Nebe_Ar.md) |
| 079 | **Nâziât** | سُورَةُ النَّازِعَاتِ | Söküp Çıkaranlar (Can Alan Melekler) | Mekke | 81 | 46 | 30. Cüz | [📄 Meal](sureler/079_Naziat.md) | [📜 Arapça](arapca_sureler/079_Naziat_Ar.md) |
| 080 | **Abese** | سُورَةُ عَبَسَ | Yüzünü Ekşitti | Mekke | 24 | 42 | 30. Cüz | [📄 Meal](sureler/080_Abese.md) | [📜 Arapça](arapca_sureler/080_Abese_Ar.md) |
| 081 | **Tekvîr** | سُورَةُ التَّكْوِيرِ | Güneşin Dürülmesi | Mekke | 7 | 29 | 30. Cüz | [📄 Meal](sureler/081_Tekvir.md) | [📜 Arapça](arapca_sureler/081_Tekvir_Ar.md) |
| 082 | **İnfitâr** | سُورَةُ الإِنْفِطَارِ | Göğün Yarılması | Mekke | 82 | 19 | 30. Cüz | [📄 Meal](sureler/082_İnfitar.md) | [📜 Arapça](arapca_sureler/082_İnfitar_Ar.md) |
| 083 | **Mutaffifîn** | سُورَةُ المُطَفِّفِينَ | Ölçü ve Tartıda Hile Yapanlar | Mekke | 86 | 36 | 30. Cüz | [📄 Meal](sureler/083_Mutaffifin.md) | [📜 Arapça](arapca_sureler/083_Mutaffifin_Ar.md) |
| 084 | **İnşikâk** | سُورَةُ الإِنْشِقَاقِ | Göğün Yarılıp Parçalanması | Mekke | 83 | 25 | 30. Cüz | [📄 Meal](sureler/084_İnşikak.md) | [📜 Arapça](arapca_sureler/084_İnşikak_Ar.md) |
| 085 | **Bürûc** | سُورَةُ البُرُوجِ | Burçlar, Takımyıldızları | Mekke | 27 | 22 | 30. Cüz | [📄 Meal](sureler/085_Büruc.md) | [📜 Arapça](arapca_sureler/085_Büruc_Ar.md) |
| 086 | **Târık** | سُورَةُ الطَّارِقِ | Gece Doğan Parlak Yıldız (Delip Geçen Işık) | Mekke | 36 | 17 | 30. Cüz | [📄 Meal](sureler/086_Tarık.md) | [📜 Arapça](arapca_sureler/086_Tarık_Ar.md) |
| 087 | **A'lâ** | سُورَةُ الأَعْلَى | En Yüce Olan Allah | Mekke | 8 | 19 | 30. Cüz | [📄 Meal](sureler/087_Ala.md) | [📜 Arapça](arapca_sureler/087_Ala_Ar.md) |
| 088 | **Gâşiye** | سُورَةُ الغَاشِيَةِ | Her Şeyi Kuşatan Kıyamet | Mekke | 68 | 26 | 30. Cüz | [📄 Meal](sureler/088_Gaşiye.md) | [📜 Arapça](arapca_sureler/088_Gaşiye_Ar.md) |
| 089 | **Fecr** | سُورَةُ الفَجْرِ | Tan Yeri Ağarması, Şafak Vakti | Mekke | 10 | 30 | 30. Cüz | [📄 Meal](sureler/089_Fecr.md) | [📜 Arapça](arapca_sureler/089_Fecr_Ar.md) |
| 090 | **Beled** | سُورَةُ البَلَدِ | Şehir, Belde (Mekke) | Mekke | 35 | 20 | 30. Cüz | [📄 Meal](sureler/090_Beled.md) | [📜 Arapça](arapca_sureler/090_Beled_Ar.md) |
| 091 | **Şems** | سُورَةُ الشَّمْسِ | Güneş | Mekke | 26 | 15 | 30. Cüz | [📄 Meal](sureler/091_Şems.md) | [📜 Arapça](arapca_sureler/091_Şems_Ar.md) |
| 092 | **Leyl** | سُورَةُ اللَّيْلِ | Gece | Mekke | 9 | 21 | 30. Cüz | [📄 Meal](sureler/092_Leyl.md) | [📜 Arapça](arapca_sureler/092_Leyl_Ar.md) |
| 093 | **Duhâ** | سُورَةُ الضُّحَى | Kuşluk Vakti | Mekke | 11 | 11 | 30. Cüz | [📄 Meal](sureler/093_Duha.md) | [📜 Arapça](arapca_sureler/093_Duha_Ar.md) |
| 094 | **İnşirâh** | سُورَةُ الشَّرْحِ | Gönül Ferahlığı, Göğsün Açılması | Mekke | 12 | 8 | 30. Cüz | [📄 Meal](sureler/094_İnşirah.md) | [📜 Arapça](arapca_sureler/094_İnşirah_Ar.md) |
| 095 | **Tîn** | سُورَةُ التِّينِ | İncir Ağacı | Mekke | 28 | 8 | 30. Cüz | [📄 Meal](sureler/095_Tin.md) | [📜 Arapça](arapca_sureler/095_Tin_Ar.md) |
| 096 | **Alak** | سُورَةُ العَلَقِ | Aşılanmış Yumurta, Embriyo | Mekke | 1 | 19 | 30. Cüz | [📄 Meal](sureler/096_Alak.md) | [📜 Arapça](arapca_sureler/096_Alak_Ar.md) |
| 097 | **Kadir** | سُورَةُ القَدْرِ | Kadir Gecesi, Değer ve Hüküm | Mekke | 25 | 5 | 30. Cüz | [📄 Meal](sureler/097_Kadir.md) | [📜 Arapça](arapca_sureler/097_Kadir_Ar.md) |
| 098 | **Beyyine** | سُورَةُ البَيِّنَةِ | Apaçık Delil, Kesin Belge | Medine | 100 | 8 | 30. Cüz | [📄 Meal](sureler/098_Beyyine.md) | [📜 Arapça](arapca_sureler/098_Beyyine_Ar.md) |
| 099 | **Zilzâl** | سُورَةُ الزَّلْزَلَةِ | Büyük Deprem, Sarsıntı | Medine | 93 | 8 | 30. Cüz | [📄 Meal](sureler/099_Zilzal.md) | [📜 Arapça](arapca_sureler/099_Zilzal_Ar.md) |
| 100 | **Âdiyât** | سُورَةُ العَادِيَاتِ | Soluk Soluğa Koşan Savaş Atları | Mekke | 14 | 11 | 30. Cüz | [📄 Meal](sureler/100_Adiyat.md) | [📜 Arapça](arapca_sureler/100_Adiyat_Ar.md) |
| 101 | **Kâria** | سُورَةُ القَارِعَةِ | Kapı Çalan / Çarpan Büyük Felaket | Mekke | 30 | 11 | 30. Cüz | [📄 Meal](sureler/101_Karia.md) | [📜 Arapça](arapca_sureler/101_Karia_Ar.md) |
| 102 | **Tekâsür** | سُورَةُ التَّكَاثُرِ | Çoklukla Övünme Yarışı | Mekke | 16 | 8 | 30. Cüz | [📄 Meal](sureler/102_Tekasür.md) | [📜 Arapça](arapca_sureler/102_Tekasür_Ar.md) |
| 103 | **Asr** | سُورَةُ العَصْرِ | Asır, Zaman, İkindi Vakti | Mekke | 13 | 3 | 30. Cüz | [📄 Meal](sureler/103_Asr.md) | [📜 Arapça](arapca_sureler/103_Asr_Ar.md) |
| 104 | **Hümeze** | سُورَةُ الهُمَزَةِ | Arkadan Çekiştiren, Dedikoducu | Mekke | 32 | 9 | 30. Cüz | [📄 Meal](sureler/104_Hümeze.md) | [📜 Arapça](arapca_sureler/104_Hümeze_Ar.md) |
| 105 | **Fîl** | سُورَةُ الفِيلِ | Fil Hadisesi | Mekke | 19 | 5 | 30. Cüz | [📄 Meal](sureler/105_Fil.md) | [📜 Arapça](arapca_sureler/105_Fil_Ar.md) |
| 106 | **Kureyş** | سُورَةُ قُرَيْشٍ | Kureyş Kabilesi | Mekke | 29 | 4 | 30. Cüz | [📄 Meal](sureler/106_Kureyş.md) | [📜 Arapça](arapca_sureler/106_Kureyş_Ar.md) |
| 107 | **Mâûn** | سُورَةُ المَاعُونِ | Küçük Bir Yardım, Zekât | Mekke | 17 | 7 | 30. Cüz | [📄 Meal](sureler/107_Maun.md) | [📜 Arapça](arapca_sureler/107_Maun_Ar.md) |
| 108 | **Kevser** | سُورَةُ الكَوْثَرِ | Bitmez Tükenmez Nimet, Kevser Havuzu | Mekke | 15 | 3 | 30. Cüz | [📄 Meal](sureler/108_Kevser.md) | [📜 Arapça](arapca_sureler/108_Kevser_Ar.md) |
| 109 | **Kâfirûn** | سُورَةُ الكَافِرُونَ | İnkârcılar | Mekke | 18 | 6 | 30. Cüz | [📄 Meal](sureler/109_Kafirun.md) | [📜 Arapça](arapca_sureler/109_Kafirun_Ar.md) |
| 110 | **Nasr** | سُورَةُ النَّصْرِ | Yardım, Zafer (İzâ Câe) | Medine | 114 | 3 | 30. Cüz | [📄 Meal](sureler/110_Nasr.md) | [📜 Arapça](arapca_sureler/110_Nasr_Ar.md) |
| 111 | **Tebbet (Mesed)** | سُورَةُ المَسَدِ | Kurumak, Helak Olmak / Bükülmüş İp | Mekke | 6 | 5 | 30. Cüz | [📄 Meal](sureler/111_Tebbet_Mesed.md) | [📜 Arapça](arapca_sureler/111_Tebbet_Mesed_Ar.md) |
| 112 | **İhlâs** | سُورَةُ الإِخْلَاصِ | Samimiyet, Katıksız Tevhid İnancı | Mekke | 22 | 4 | 30. Cüz | [📄 Meal](sureler/112_İhlas.md) | [📜 Arapça](arapca_sureler/112_İhlas_Ar.md) |
| 113 | **Felak** | سُورَةُ الفَلَقِ | Sabah Aydınlığı, Şafak | Mekke | 20 | 5 | 30. Cüz | [📄 Meal](sureler/113_Felak.md) | [📜 Arapça](arapca_sureler/113_Felak_Ar.md) |
| 114 | **Nâs** | سُورَةُ النَّاسِ | İnsanlar | Mekke | 21 | 6 | 30. Cüz | [📄 Meal](sureler/114_Nas.md) | [📜 Arapça](arapca_sureler/114_Nas_Ar.md) |