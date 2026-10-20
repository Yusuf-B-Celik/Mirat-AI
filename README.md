# 🏛️ MİRAT (Metin İçi Rastlantısallık ve Analiz Teknolojisi) v6.0

> **"Kutsal metinlerin dış dünyaya, kozmik yasalara, biyolojiye, matematiğe ve sosyolojik gerçekliklere tuttuğu objektif ayna."**

MİRAT, Kur'an-ı Kerim metninin 77.429 kelimesini ve 130.030 morfolojik segmentini Doğal Dil İşleme (NLP), Bilgi Teorisi (Zipf/Heaps/DFA), PPMI Semantik Graf Analizi, Belâgat/İltifat Morfolojisi, Çift-Modelli LLM Konsensüsü (DeepSeek + Qwen, $\kappa = 0.88$), Katı Sıfır Modelleri (Monte Carlo permütasyonları), Benjamini-Hochberg Yanlış Keşif Oranı (FDR) ve Ön-Kayıt (Preregistration) mimarisiyle inceleyen bağımsız, hakemli seviyesinde bir yapay zekâ ve metin madenciliği araştırma platformudur.

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
│   ├── 👑 MIRAT_KESIF_KATALOGU.md       # v6.0 9 Kategori, 219 Bulgu Master Kataloğu
│   ├── 👑 MIRAT_BUYUK_KULLIYAT_VE_SISTEM_DOKUMANTASYONU.md / .pdf # Master Ansiklopedi
│   ├── 📑 MIRAT_ANALIZ_RAPORU.md / .pdf # 5 Temel Katman Matematiksel Analiz Raporu
│   ├── 📑 MIRAT_YUZLERCE_ORUNTU_KATALOGU.md / .pdf # 10 Kategoride 100+ Örüntü Master Kataloğu
│   ├── 📑 MIRAT_ZIT_VE_ES_ANLAMLI_ANALIZI.md / .pdf # 7 Kural Zıt/Eş Anlam Analiz Raporu
│   └── 📑 MIRAT_ILERI_YAPISAL_VE_GRAFIKSEL_ANALIZ.md / .pdf # Kriptografi, Halka & Dalga Raporu
│
├── 📁 veriler/                          # Veri Tabanları, JSON Çıktıları ve Sözlükler
│   ├── 🗄️ mirat_corpus.db               # 77.429 Kelime, 130.030 Segment SQLite Veritabanı
│   ├── 🗄️ mirat_features.db             # Ön-Hesaplanmış Morfolojik Özellikler Veritabanı
│   ├── 📊 mirat_kesifler.json           # 219 Bulgu, İstatistikler ve P-Değerleri JSON Çıktısı
│   ├── 📊 mirat_analiz_verileri.json    # 5 Temel Katman JSON Veri Seti
│   ├── 📊 mirat_oruntuler_veritabani.json # 100+ Örüntü JSON Veri Seti
│   ├── 📂 lexicon/                      # Çift-Modelli LLM Konsensüs Sözlüğü (root_lexicon.json)
│   └── 🖼️ quran_waveform_silhouette.svg # 114 Sure Ayet Sayıları Dalga Silüeti Grafiği
│
├── 📁 mirat/                            # MİRAT Python Analiz ve Modelleme Çekirdeği
│   ├── 🧠 database.py                   # SQLite ve Morfolojik Sorgu Motoru
│   ├── 🧩 features.py                   # Şahıs, Cinsiyet, Sayı, Çatı, Zaman, Form Morfoloji Çıkarıcı
│   ├── 📐 stats.py                      # İleri İstatistiki Testler (Chi2, Z, FDR, TOST, Bayes Faktörü)
│   ├── 🛡️ claim_registry.py             # İddia Denetçisi ve Ön-Kayıt Defteri (Filtre Bağımlılık Tespiti)
│   ├── 🎲 null_models.py                # Monte Carlo Permütasyon ve Hedefsiz Sıfır Modelleri
│   ├── 🤖 llm/                          # Çok Modelli LLM Altyapısı (Bütçe, Kota, Önbellek, Yönlendirici)
│   ├── 📁 discovery/                    # 🔬 9 Yeni Bilimsel Keşif Motoru (Kategori 11-19)
│   │   ├── finding.py                   # Evrensel Bulgu Veri Yapısı ve Benjamini-Hochberg Düzeltici
│   │   ├── runner.py                    # 9 Keşif Motorunu Paralel/Sıralı Koşan Master Çalıştırıcı
│   │   ├── lexicon.py                   # DeepSeek & Qwen Çift Modelli Konsensüs Sözlük Motoru
│   │   ├── c11_chronology.py            # Kategori 11: Kronolojik Evrim ve Üslup Değişimi
│   │   ├── c12_rhetoric.py              # Kategori 12: Belâgat, İltifat ve Hitap Kaymaları
│   │   ├── c13_number_morphology.py     # Kategori 13: Sayı Morfolojisi ve Fiil Babları
│   │   ├── c14_repetition.py            # Kategori 14: Tekrar, Ayet Eşlikleri ve Formül Yapıları
│   │   ├── c15_semantic_network.py      # Kategori 15: Semantik PPMI Ağı ve Kavram Kümeleri
│   │   ├── c16_antonyms.py              # Kategori 16: Tıbâk Birlikte Görünme ve Frekans Simetrisi
│   │   ├── c17_ring_detection.py        # Kategori 17: Halka Kompozisyonu ve Blok Simetrisi
│   │   ├── c18_information.py           # Kategori 18: Bilgi Teorisi, Entropi, Zipf/Heaps ve DFA
│   │   └── c19_narrative.py             # Kategori 19: Kıssa Morfolojisi ve Ceza Döngüsü
│   └── 📁 layers/                       # 5 Temel Bilimsel Katman Modülü
│
├── 📁 tests/                            # Otomatik Test Külliyatı (52 Birim Testi)
│   ├── test_discovery.py                # 9 Keşif Motoru ve Morfolojik Özellik Testleri
│   ├── test_web_app.py                  # Web ve REST API Endpoint Testleri
│   ├── test_llm_client.py               # Kota, Bütçe ve Model Yönlendirici Testleri
│   ├── test_null_models.py              # Sıfır Modelleri ve İddia Denetçisi Testleri
│   ├── test_rag_citations.py            # Halüsinasyonsuz RAG ve Deterministik Soru-Cevap Testleri
│   ├── test_stats_extended.py           # Genişletilmiş İstatistik Testleri
│   ├── test_mirat.py                    # 5 Katman ve Veritabanı Testleri
│   ├── test_pattern_miner.py            # Örüntü Madenciliği Testleri
│   ├── test_antonym_synonym.py          # Zıt/Eş Anlam Testleri
│   └── test_advanced_structural.py      # Kriptografi, Parite ve Fâsıla Testleri
│
├── 💻 mirat_cli.py                      # Etkileşimli Terminal Arayüzü (CLI v6.0)
├── 🌐 web/                              # FastAPI + Tailwind SPA Web Arayüzü
└── 📄 README.md                         # Ana Dokümantasyon
```

---

## 🔬 Yeni Bilimsel Keşif Motorları (Kategoriler 11–19)

MİRAT v6.0 ile metin madenciliği ve Kur'an leksikolojisi alanında **9 yeni araştırma kategorisi** ve **219 bağımsız bulgu** sisteme kazandırılmıştır:

| No | Kategori Adı | Kullanılan Yöntemler | Öne Çıkan Bulgu |
|:---|:---|:---|:---|
| **11** | **Kronolojik Evrim** | Spearman Korelasyonu, Welch t-testi, Değişim Noktası Analizi | Ayet uzunluğu Mekke'den Medine'ye istikrarlı uzar ($\rho=+0.669, q=0.003$); Mekke sonu/Medine başında keskin kırılma ($p=0.0003$). |
| **12** | **Belâgat ve İltifat** | 130k morfolojik segment ayrıştırma, Ki-Kare testi | 61 belirgin iltifat hitap kayması (Fâtiha 1:4$\to$1:5 dahil); eskatolojik bağlamda edilgen çatı $1.61\times$ artar ($q=0.0098$). |
| **13** | **Sayı Morfolojisi** | Binom z-testi, Çoklu karşılaştırma (FDR) | Çoğul-baskın kökler (ör. melekler, gökler); Rahmân Suresi tesniye (ikil) yoğunluğu $353.3‰$ ile korpus zirvesi. |
| **14** | **Tekrar ve Formül Yapıları** | N-gram madenciliği, Karşılıklı Bilgi (MI) | 192 sureler arası yakın kopya ayet; fâsıla son kelimesi ile ayet içeriği arasında $3.24$ bit Karşılıklı Bilgi ($p < 0.001$). |
| **15** | **Semantik Ağ Analizi** | kNN seyreltilmiş PPMI Grafı, Louvain Modülerliği | 41 tutarlı kavram kümesi; 'Ekonomi' ($\rho=+0.35$) ve 'Peygamberlik' ($\rho=+0.41$) alanlarının kronolojik evrimi. |
| **16** | **Zıt Anlam ve Tıbâk** | Çift-model konsensüsü, Geometrik lift analizi | Tıbâk zıtları aynı ayette rastlantısal beklenen değerin $2.8\times$ katı birlikte görünür ($p=0.0002$); frekans eşitliği efsanesi çürütülmüştür ($q=0.945$). |
| **17** | **Halka Kompozisyonu** | Döngüsel permütasyon sıfır modeli | Tüm sureler genelinde simetrik halka yapısı evrensel bir kanun değildir ($q=1.0$); bilimsel dürüstlükle negatif sonuç raporlanır. |
| **18** | **Bilgi Teorisi ve Dinamik** | Zipf/Heaps Kuvvet Yasaları, DFA, Şannon Entropisi | Klasik Arapça için $\alpha_{\text{Zipf}}=1.00$, $\beta_{\text{Heaps}}=0.58$; DFA uzun erimli korelasyon $\alpha=0.895$. |
| **19** | **Kıssa Morfolojisi** | Kendall $\tau$ sıralama testi, Eş-görünüm grafları | 23 surede Nûh$\to$Hûd$\to$Sâlih$\to$Lût$\to$Şuayb ceza döngüsü sıralaması yüksek uyum gösterir ($\tau=0.420, q=0.0002$). |

---

## 🚀 Hızlı Başlangıç ve CLI Kullanımı

MİRAT sisteminin tüm fonksiyonları `mirat_cli.py` üzerinden interaktif olarak yönetilebilir:

```bash
# 1. Tüm 9 Yeni Keşif Motorunu Çalıştır ve Rapor Üret
python3 mirat_cli.py --discover all

# 2. Belirli bir Keşif Motorunu İncele (Örn: Kategori 11 Kronoloji veya 15 Semantik Ağ)
python3 mirat_cli.py --discover 11
python3 mirat_cli.py --discover 15

# 3. Kayıtlı Keşif Bulgularını Terminalde Listele
python3 mirat_cli.py --findings
python3 mirat_cli.py --findings --category 12

# 4. Bilimsel İddia Denetimi (FDR, TOST, Bayes Faktörü & Filtre Bağımlılığı)
python3 mirat_cli.py --audit

# 5. Sıfır Modelleri ve Monte Carlo Permütasyon Testi
python3 mirat_cli.py --null-model

# 6. Dolar Bazlı Kota, Bütçe ve Model Harcama Raporu
python3 mirat_cli.py --budget

# 7. Otonom Hipotez Keşif ve Ön-Kayıt Ajanı
python3 mirat_cli.py --agent --limit 3

# 8. Kaynak Doğrulamalı Soru-Cevap (Halüsinasyonsuz RAG)
python3 mirat_cli.py --ask "Kur'an'da deniz kelimesi kaç kez geçer?"

# 9. Canlı FastAPI Web Arayüzü ve Jüri Panelini Başlat (Lokal)
python3 mirat_cli.py --web
# Tarayıcıda http://localhost:8000 adresini açın
```

---

## 🌐 Modern Vercel Web Platformu (Next.js 15 & Tailwind CSS)

MİRAT v6.0, tüm dünyaya tanıtım amaçlı sunulabilecek, sıfır sunucu maliyetiyle Vercel üzerinde çalışan, yüksek performanslı ve interaktif bir web uygulaması içerir (`site/` dizini):

- 🔬 **219 Bulgu Keşif Gezgini:** Anlık arama, 9 kategori ve anlamlılık filtreleri.
- 📊 **İnteraktif Veri Laboratuvarı:** 114 sure ayet dalga silüeti, nüzul kırılım grafiği ve $2.8\times$ tıbâk zıt anlam matrisi.
- 🛡️ **Bilimsel İddia Denetçisi:** Popüler iddiaların filtre bağımlılık ve baz oran analizleri.
- 🧮 **Canlı İstatistiki Hesaplayıcı:** Ziyaretçilerin iki sayı girip Z-skoru, $\%5$ TOST denkliği ve Bayes Faktörünü test edebileceği araç.
- 📜 **Kriptografik Ön-Kayıt Defteri:** SHA-256 hash zinciri doğrulaması.

### Lokal Geliştirme ve Derleme:
```bash
# Web arayüzü veri köprüsünü güncelle
npm run export-data

# Lokal geliştirme sunucusunu başlat (http://localhost:3000)
npm run dev

# Üretim için statik derleme yap (site/out/)
npm run build
```

### Vercel ile Canlıya Alma:
1. Deponuzu GitHub'a push edin (`git push origin main`).
2. [vercel.com](https://vercel.com) üzerinde **"Add New Project"** diyerek depoyu seçin.
3. Kök dizindeki `vercel.json` ve `package.json` sayesinde hiçbir ayar değiştirmeden **"Deploy"** butonuna basın. Site yaklaşık 40 saniye içinde global Edge CDN üzerinden yayına alınır.

---

## 🧪 Birim ve Entegrasyon Testleri

```bash
python3 -m unittest discover -s tests -v
```
*Tüm **52 birim testi** sıfır hata ile eksiksiz tamamlanmaktadır.*

