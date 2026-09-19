# 🏛️ MİRAT (Metin İçi Rastlantısallık ve Analiz Teknolojisi) v4.0

> **"Kutsal metinlerin dış dünyaya, kozmik yasalara, biyolojiye, matematiğe ve sosyolojik gerçekliklere tuttuğu objektif ayna."**

MİRAT, Kur'an-ı Kerim metninin 77.429 kelimesini ve 130.030 morfolojik segmentini Doğal Dil İşleme (NLP), Ki-Kare ($\chi^2$), Z-Skoru, Birlikte Görünme (Co-occurrence/PMI), Halka Yapısı (Chiasmus), Kriptografik Parite ve Grafiksel Dalga Analizi yöntemleriyle inceleyen ileri düzey bir yapay zekâ ve metin madenciliği platformudur.

---

## 📂 Düzenli Proje Dizin Mimarisi

```
Mirat-AI/
├── 📁 kuran/                            # Kur'an-ı Kerim Dijital Mushaf ve Mealleri
│   ├── 📕 KURAN-I_KERIM_MEALI.pdf       # 1.589 Sayfalık Hat ve Mealli Master PDF
│   ├── 📖 KURAN-I_KERIM_MEALI.md        # 114 Sure Arapça + Okunuş + Meal Tek Dosya
│   ├── 📜 KURAN-I_KERIM_ARAPCA.md       # Harekeli Osmanî Hatlı Salt Arapça Mushaf
│   ├── 🇹🇷 KURAN-I_KERIM_SADECE_MEAL.md  # Kesintisiz Akıcı Salt Türkçe Meal
│   ├── 📑 Kuran.pdf                     # Orijinal Kaynak Tarama PDF'i
│   ├── 📂 sureler/ (114 MD)             # 114 Ayrı Mealli Sure Dosyası
│   ├── 📂 arapca_sureler/ (114 MD)      # 114 Ayrı Salt Arapça Sure Dosyası
│   └── 📂 cuzler/ (30 MD)               # 30 Cüz Dosyası (1. Cüz - 30. Cüz)
│
├── 📁 raporlar/                         # Bilimsel Araştırma Raporları ve PDF Külliyatı
│   ├── 📑 MIRAT_ANALIZ_RAPORU.md / .pdf # 5 Temel Katman Matematiksel Analiz Raporu
│   ├── 📑 MIRAT_YUZLERCE_ORUNTU_KATALOGU.md / .pdf # 10 Kategoride 100+ Örüntü Master Kataloğu
│   ├── 📑 MIRAT_ZIT_VE_ES_ANLAMLI_ANALIZI.md / .pdf # 7 Kural Zıt/Eş Anlam Analiz Raporu
│   └── 📑 MIRAT_ILERI_YAPISAL_VE_GRAFIKSEL_ANALIZ.md / .pdf # Kriptografi, Halka & Dalga Raporu
│
├── 📁 veriler/                          # Veri Tabanları, JSON Çıktıları ve Vektörel Grafikler
│   ├── 🗄️ mirat_corpus.db               # 77.429 Kelime, 130.030 Segment SQLite Veritabanı
│   ├── 📄 quran-morphology.txt          # Quranic Corpus Ham Morfoloji Kaynağı
│   ├── 📊 mirat_analiz_verileri.json    # 5 Temel Katman JSON Veri Seti
│   ├── 📊 mirat_oruntuler_veritabani.json # 100+ Örüntü JSON Veri Seti
│   ├── 📊 mirat_zit_ve_es_anlamlilar.json # Zıt ve Eş Anlamlılar JSON Veri Seti
│   ├── 📊 mirat_ileri_yapisal_veriler.json # Kriptografik ve Yapısal JSON Veri Seti
│   └── 🖼️ quran_waveform_silhouette.svg # 114 Sure Ayet Sayıları Dalga Silüeti Grafiği
│
├── 📁 mirat/                            # MİRAT Python Analiz ve Modelleme Çekirdeği
│   ├── 🧠 database.py                   # SQLite ve Morfolojik Sorgu Motoru
│   ├── 📐 stats.py                      # İleri İstatistiki Testler (Chi2, Z, PMI, Kendall Tau)
│   ├── 🔍 pattern_miner.py              # 100+ Örüntü Madenciliği ve Keşif Motoru
│   ├── ⚖️ antonym_synonym_engine.py     # 7 Kural Zıt/Eş Anlam Modelleme Motoru
│   ├── 🔐 advanced_structural_engine.py # Kriptografik, Fonetik, Halka ve Dalga Motoru
│   ├── 📑 report_generator.py           # PDF ve Markdown Rapor Üreteci
│   └── 📁 layers/                       # 5 Temel Bilimsel Katman Modülü
│       ├── layer1_geology.py            # Yüzey Alanı (%71-%29) ve İzostazi
│       ├── layer2_cosmic.py             # Zaman, Gün (365), Ay (12), Işık/Karanlık
│       ├── layer3_ethics.py             # Dünya=Ahiret (115=115), Melek=Şeytan (88=88)
│       ├── layer4_socioeconomic.py      # Açlık/Doyurmak (1:8), Cinsiyet Dengesi
│       └── layer5_science.py            # Embriyoloji 5 Aşama (\tau=1.000), 7 Gök
│
├── 📁 scripts/                          # Kur'an ve Cüz Derleme Betikleri
│   ├── build_quran_markdown.py          # Sure ve Cüz MD üreteci
│   └── generate_pdf.py                  # Chrome Headless PDF motoru
│
├── 📁 tests/                            # Otomatik Test Külliyatı (18 Birim Testi)
│   ├── test_mirat.py
│   ├── test_pattern_miner.py
│   ├── test_antonym_synonym.py
│   └── test_advanced_structural.py
│
├── 💻 mirat_cli.py                      # Etkileşimli Terminal Arayüzü (CLI v4.0)
└── 📄 README.md                         # Ana Dokümantasyon
```

---

## 🚀 Hızlı Başlangıç ve CLI Kullanımı

MİRAT sisteminin tüm fonksiyonları `mirat_cli.py` üzerinden interaktif olarak yönetilebilir:

```bash
# 1. Grafiksel Dalga Formu ve Lafza-i Celal Silüeti
python3 mirat_cli.py --waveform

# 2. Kriptografik Parite Kilidi ve Palindromik Ayetler
python3 mirat_cli.py --crypto

# 3. Âyetü'l-Kürsî ve Bakara Suresi Halka Yapısı (Chiasmus)
python3 mirat_cli.py --chiasmus

# 4. Fonetik ve Akustik Fâsıla Harfleri Dağılımı
python3 mirat_cli.py --phonetics

# 5. Zıt ve Eş Anlamlı Kelimelerin 7 Kural Analizi
python3 mirat_cli.py --antonyms
python3 mirat_cli.py --synonyms

# 6. 100+ Örüntü Madenciliği Kategorilerinden Birini İncele
python3 mirat_cli.py --category 4     # Kategori 4: Biyoloji ve Tıp
python3 mirat_cli.py --category 5     # Kategori 5: Kimya ve Elementler

# 7. Kök ve Lemma Sorgulama
python3 mirat_cli.py --root بحر       # Deniz kökü analizi
python3 mirat_cli.py --compare حيي موت # Yaşam ve Ölüm köklerini karşılaştır

# 8. Tüm Raporları ve PDF Kataloglarını Baştan Derle
python3 mirat_cli.py --report
```

---

## 🧪 Birim ve Entegrasyon Testleri

```bash
python3 -m unittest discover tests
```
*Tüm 18 birim testi sıfır hata ile yaklaşık 1.3 saniyede tamamlanmaktadır.*
