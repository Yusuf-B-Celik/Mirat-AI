# MİRAT v6 — Keşif Kataloğu

_Üretim: 2026-10-20T19:22:11 · Tüm sayılar deterministik koddan; LLM yalnızca etiket (anlam, zıt kök, anlam alanı) üretir ve bu bulgular 🤖 ile işaretlidir._

| Kategori | Bulgu | Test | Anlamlı (q<0.05) | Anlamsız / negatif |
|---|---:|---:|---:|---:|
| 11. Kronolojik Evrim (Nüzul Sırası) | 38 | 35 | 16 | 19 |
| 12. Belâgat Örüntüleri (İltifat, Edilgen, Açılış, Edat İşlevleri) | 50 | 48 | 26 | 22 |
| 13. Sayı Morfolojisi (Tekil-İkil-Çoğul) ve Fiil Babları | 29 | 24 | 18 | 6 |
| 14. Tekrar ve Formül Yapıları | 42 | 18 | 17 | 1 |
| 15. Kavram Ağı ve Anlam Alanları | 16 | 14 | 6 | 8 |
| 16. Zıt Anlam (Tıbâk) Sayımı | 5 | 4 | 3 | 1 |
| 17. Halka (Ayna) Kompozisyon Taraması | 17 | 17 | 0 | 17 |
| 18. Bilgi Kuramı ve Metin Dinamiği | 5 | 3 | 2 | 1 |
| 19. Kıssa (Anlatı) Ağı | 17 | 14 | 14 | 0 |
| **Toplam** | **219** | **177** | **102** | **75** |

> [!NOTE]
> q-değerleri kategori içi Benjamini-Hochberg düzeltmesidir. Kök/çift taramalarında yalnızca en güçlü bulgular listelenir; tarama özetleri toplam test sayısını verir. "Anlamsız" sütunu, raporlanan ama hipotezi desteklemeyen testleri sayar — bunlar bilinçli olarak katalogda tutulur.


## 11. Kronolojik Evrim (Nüzul Sırası)

_Çalışma süresi: 4.71 s_

### ✅ Ortalama ayet uzunluğu (kelime): nüzul sırası ilerledikçe artıyor
**Yöntem:** Spearman rho, nüzul sırası (114 sure), 2000 permütasyon · **Ölçüt:** Spearman rho = 0.669 · **p:** 0.0005 · **q:** 0.0030 · **Etki:** 0.669

Mekkî ort. 8.10 | Medenî ort. 16.93 (oran 2.09x)

### ✅ Ortalama ayet uzunluğu (kelime): nüzul sırasında kırılma noktası 37. sure civarında
**Yöntem:** En güçlü tek ikili bölünme (|Welch t|), 300 permütasyon · **Ölçüt:** |t| (bölünme) = 12.279 · **p:** 0.0033 · **q:** 0.0125

Bulunan kırılma: nüzul sırası 37 | gerçek ilk Medenî sure konumu: 86

<details><summary>Kanıt (1)</summary>

- nüzul#37: Sâd

</details>

### ✅ Ayet sayısı: nüzul sırası ilerledikçe artıyor
**Yöntem:** Spearman rho, nüzul sırası (114 sure), 2000 permütasyon · **Ölçüt:** Spearman rho = 0.248 · **p:** 0.0065 · **q:** 0.0217 · **Etki:** 0.248

Mekkî ort. 53.64 | Medenî ort. 57.96 (oran 1.08x)

### ✅ Ayet sayısı: nüzul sırasında kırılma noktası 32. sure civarında
**Yöntem:** En güçlü tek ikili bölünme (|Welch t|), 300 permütasyon · **Ölçüt:** |t| (bölünme) = 7.666 · **p:** 0.0033 · **q:** 0.0125

Bulunan kırılma: nüzul sırası 32 | gerçek ilk Medenî sure konumu: 86

<details><summary>Kanıt (1)</summary>

- nüzul#32: Mürselât

</details>

### ✅ Yeni lemma oranı (ilk 60 içerik kelimesinde tekil lemma): nüzul sırası ilerledikçe azalıyor
**Yöntem:** Spearman rho, nüzul sırası (114 sure), 2000 permütasyon · **Ölçüt:** Spearman rho = -0.342 · **p:** 0.0005 · **q:** 0.0030 · **Etki:** -0.342

Mekkî ort. 0.81 | Medenî ort. 0.75 (oran 0.93x)

### ✅ Yeni lemma oranı (ilk 60 içerik kelimesinde tekil lemma): nüzul sırasında kırılma noktası 81. sure civarında
**Yöntem:** En güçlü tek ikili bölünme (|Welch t|), 300 permütasyon · **Ölçüt:** |t| (bölünme) = 4.534 · **p:** 0.0100 · **q:** 0.0299

Bulunan kırılma: nüzul sırası 81 | gerçek ilk Medenî sure konumu: 86

<details><summary>Kanıt (1)</summary>

- nüzul#81: İnfitâr

</details>

### ⚪ "Biz" kipi fiil oranı (1P, ‰ fiil): nüzul sırası ilerledikçe azalıyor
**Yöntem:** Spearman rho, nüzul sırası (114 sure), 2000 permütasyon · **Ölçüt:** Spearman rho = -0.082 · **p:** 0.3883 · **q:** 0.4393 · **Etki:** -0.082

Mekkî ort. 109.83 | Medenî ort. 43.82 (oran 0.40x)

### ✅ "Biz" kipi fiil oranı (1P, ‰ fiil): nüzul sırasında kırılma noktası 104. sure civarında
**Yöntem:** En güçlü tek ikili bölünme (|Welch t|), 300 permütasyon · **Ölçüt:** |t| (bölünme) = 6.717 · **p:** 0.0033 · **q:** 0.0125

Bulunan kırılma: nüzul sırası 104 | gerçek ilk Medenî sure konumu: 86

<details><summary>Kanıt (1)</summary>

- nüzul#104: Mücâdele

</details>

### ⚪ "Ben" kipi fiil oranı (1S, ‰ fiil): nüzul sırası ilerledikçe azalıyor
**Yöntem:** Spearman rho, nüzul sırası (114 sure), 2000 permütasyon · **Ölçüt:** Spearman rho = -0.045 · **p:** 0.6272 · **q:** 0.6346 · **Etki:** -0.045

Mekkî ort. 36.90 | Medenî ort. 9.99 (oran 0.27x)

### ⚪ "Ben" kipi fiil oranı (1S, ‰ fiil): nüzul sırasında kırılma noktası 83. sure civarında (Mekke→Medine sınırıyla örtüşüyor)
**Yöntem:** En güçlü tek ikili bölünme (|Welch t|), 300 permütasyon · **Ölçüt:** |t| (bölünme) = 3.612 · **p:** 0.0365 · **q:** 0.0664

Bulunan kırılma: nüzul sırası 83 | gerçek ilk Medenî sure konumu: 86

<details><summary>Kanıt (1)</summary>

- nüzul#83: Rûm

</details>

### ⚪ Peygambere tekil hitap (2. tekil, ‰ fiil): nüzul sırası ilerledikçe azalıyor
**Yöntem:** Spearman rho, nüzul sırası (114 sure), 2000 permütasyon · **Ölçüt:** Spearman rho = -0.172 · **p:** 0.0715 · **q:** 0.1021 · **Etki:** -0.172

Mekkî ort. 106.77 | Medenî ort. 75.14 (oran 0.70x)

### ⚪ Peygambere tekil hitap (2. tekil, ‰ fiil): nüzul sırasında kırılma noktası 22. sure civarında
**Yöntem:** En güçlü tek ikili bölünme (|Welch t|), 300 permütasyon · **Ölçüt:** |t| (bölünme) = 2.931 · **p:** 0.1429 · **q:** 0.1863

Bulunan kırılma: nüzul sırası 22 | gerçek ilk Medenî sure konumu: 86

<details><summary>Kanıt (1)</summary>

- nüzul#22: Necm

</details>

### ✅ Topluluğa hitap (2. çoğul, ‰ fiil): nüzul sırası ilerledikçe artıyor
**Yöntem:** Spearman rho, nüzul sırası (114 sure), 2000 permütasyon · **Ölçüt:** Spearman rho = 0.488 · **p:** 0.0005 · **q:** 0.0030 · **Etki:** 0.488

Mekkî ort. 92.60 | Medenî ort. 171.46 (oran 1.85x)

### ⚪ Topluluğa hitap (2. çoğul, ‰ fiil): nüzul sırasında kırılma noktası 15. sure civarında
**Yöntem:** En güçlü tek ikili bölünme (|Welch t|), 300 permütasyon · **Ölçüt:** |t| (bölünme) = 3.858 · **p:** 0.0266 · **q:** 0.0613

Bulunan kırılma: nüzul sırası 15 | gerçek ilk Medenî sure konumu: 86

<details><summary>Kanıt (1)</summary>

- nüzul#15: Tekâsür

</details>

### ⚪ Emir kipi oranı (‰ fiil): nüzul sırası ilerledikçe artıyor
**Yöntem:** Spearman rho, nüzul sırası (114 sure), 2000 permütasyon · **Ölçüt:** Spearman rho = 0.105 · **p:** 0.2519 · **q:** 0.3070 · **Etki:** 0.105

Mekkî ort. 91.90 | Medenî ort. 100.34 (oran 1.09x)

### ⚪ Emir kipi oranı (‰ fiil): nüzul sırasında kırılma noktası 104. sure civarında
**Yöntem:** En güçlü tek ikili bölünme (|Welch t|), 300 permütasyon · **Ölçüt:** |t| (bölünme) = 1.776 · **p:** 0.6346 · **q:** 0.6346

Bulunan kırılma: nüzul sırası 104 | gerçek ilk Medenî sure konumu: 86

<details><summary>Kanıt (1)</summary>

- nüzul#104: Mücâdele

</details>

### ⚪ Edilgen çatı oranı (‰ fiil): nüzul sırası ilerledikçe artıyor
**Yöntem:** Spearman rho, nüzul sırası (114 sure), 2000 permütasyon · **Ölçüt:** Spearman rho = 0.202 · **p:** 0.0310 · **q:** 0.0620 · **Etki:** 0.202

Mekkî ort. 72.97 | Medenî ort. 60.45 (oran 0.83x)

### ⚪ Edilgen çatı oranı (‰ fiil): nüzul sırasında kırılma noktası 103. sure civarında
**Yöntem:** En güçlü tek ikili bölünme (|Welch t|), 300 permütasyon · **Ölçüt:** |t| (bölünme) = 2.195 · **p:** 0.3953 · **q:** 0.4393

Bulunan kırılma: nüzul sırası 103 | gerçek ilk Medenî sure konumu: 86

<details><summary>Kanıt (1)</summary>

- nüzul#103: Münâfikûn

</details>

### ⚪ Geçmiş zaman (PERF) oranı (‰ fiil): nüzul sırası ilerledikçe azalıyor
**Yöntem:** Spearman rho, nüzul sırası (114 sure), 2000 permütasyon · **Ölçüt:** Spearman rho = -0.221 · **p:** 0.0215 · **q:** 0.0537 · **Etki:** -0.221

Mekkî ort. 506.76 | Medenî ort. 434.20 (oran 0.86x)

### ⚪ Geçmiş zaman (PERF) oranı (‰ fiil): nüzul sırasında kırılma noktası 86. sure civarında (Mekke→Medine sınırıyla örtüşüyor)
**Yöntem:** En güçlü tek ikili bölünme (|Welch t|), 300 permütasyon · **Ölçüt:** |t| (bölünme) = 3.062 · **p:** 0.0399 · **q:** 0.0664

Bulunan kırılma: nüzul sırası 86 | gerçek ilk Medenî sure konumu: 86

<details><summary>Kanıt (1)</summary>

- nüzul#86: Bakara

</details>

### ⚪ Soru edatı yoğunluğu (‰ kelime): nüzul sırası ilerledikçe azalıyor
**Yöntem:** Spearman rho, nüzul sırası (114 sure), 2000 permütasyon · **Ölçüt:** Spearman rho = -0.204 · **p:** 0.0290 · **q:** 0.0620 · **Etki:** -0.204

Mekkî ort. 19.93 | Medenî ort. 9.59 (oran 0.48x)

### ✅ Soru edatı yoğunluğu (‰ kelime): nüzul sırasında kırılma noktası 97. sure civarında
**Yöntem:** En güçlü tek ikili bölünme (|Welch t|), 300 permütasyon · **Ölçüt:** |t| (bölünme) = 5.414 · **p:** 0.0133 · **q:** 0.0362

Bulunan kırılma: nüzul sırası 97 | gerçek ilk Medenî sure konumu: 86

<details><summary>Kanıt (1)</summary>

- nüzul#97: İnsân (Dehr)

</details>

### ✅ Şart edatı yoğunluğu (‰ kelime): nüzul sırası ilerledikçe artıyor
**Yöntem:** Spearman rho, nüzul sırası (114 sure), 2000 permütasyon · **Ölçüt:** Spearman rho = 0.397 · **p:** 0.0005 · **q:** 0.0030 · **Etki:** 0.397

Mekkî ort. 8.13 | Medenî ort. 16.96 (oran 2.09x)

### ⚪ Şart edatı yoğunluğu (‰ kelime): nüzul sırasında kırılma noktası 86. sure civarında (Mekke→Medine sınırıyla örtüşüyor)
**Yöntem:** En güçlü tek ikili bölünme (|Welch t|), 300 permütasyon · **Ölçüt:** |t| (bölünme) = 3.383 · **p:** 0.0997 · **q:** 0.1359

Bulunan kırılma: nüzul sırası 86 | gerçek ilk Medenî sure konumu: 86

<details><summary>Kanıt (1)</summary>

- nüzul#86: Bakara

</details>

### ⚪ Olumsuzluk edatı yoğunluğu (‰ kelime): nüzul sırası ilerledikçe azalıyor
**Yöntem:** Spearman rho, nüzul sırası (114 sure), 2000 permütasyon · **Ölçüt:** Spearman rho = -0.173 · **p:** 0.0675 · **q:** 0.1012 · **Etki:** -0.173

Mekkî ort. 36.91 | Medenî ort. 26.39 (oran 0.72x)

### ⚪ Olumsuzluk edatı yoğunluğu (‰ kelime): nüzul sırasında kırılma noktası 91. sure civarında
**Yöntem:** En güçlü tek ikili bölünme (|Welch t|), 300 permütasyon · **Ölçüt:** |t| (bölünme) = 3.287 · **p:** 0.0399 · **q:** 0.0664

Bulunan kırılma: nüzul sırası 91 | gerçek ilk Medenî sure konumu: 86

<details><summary>Kanıt (1)</summary>

- nüzul#91: Nisâ

</details>

### ✅ Nida (ey!) yoğunluğu (‰ kelime): nüzul sırası ilerledikçe artıyor
**Yöntem:** Spearman rho, nüzul sırası (114 sure), 2000 permütasyon · **Ölçüt:** Spearman rho = 0.370 · **p:** 0.0005 · **q:** 0.0030 · **Etki:** 0.370

Mekkî ort. 2.86 | Medenî ort. 6.21 (oran 2.17x)

### ⚪ Nida (ey!) yoğunluğu (‰ kelime): nüzul sırasında kırılma noktası 81. sure civarında
**Yöntem:** En güçlü tek ikili bölünme (|Welch t|), 300 permütasyon · **Ölçüt:** |t| (bölünme) = 2.677 · **p:** 0.2558 · **q:** 0.3070

Bulunan kırılma: nüzul sırası 81 | gerçek ilk Medenî sure konumu: 86

<details><summary>Kanıt (1)</summary>

- nüzul#81: İnfitâr

</details>

### ⚪ Tekit/vurgu edatı yoğunluğu (‰ kelime): nüzul sırası ilerledikçe azalıyor
**Yöntem:** Spearman rho, nüzul sırası (114 sure), 2000 permütasyon · **Ölçüt:** Spearman rho = -0.067 · **p:** 0.4743 · **q:** 0.5081 · **Etki:** -0.067

Mekkî ort. 24.76 | Medenî ort. 13.34 (oran 0.54x)

### ⚪ Tekit/vurgu edatı yoğunluğu (‰ kelime): nüzul sırasında kırılma noktası 104. sure civarında
**Yöntem:** En güçlü tek ikili bölünme (|Welch t|), 300 permütasyon · **Ölçüt:** |t| (bölünme) = 3.559 · **p:** 0.0532 · **q:** 0.0839

Bulunan kırılma: nüzul sırası 104 | gerçek ilk Medenî sure konumu: 86

<details><summary>Kanıt (1)</summary>

- nüzul#104: Mücâdele

</details>

### ✅ Kök ربب (Rab, efendi): Mekkî dönemde yoğunlaşıyor
**Yöntem:** Medenî token payı vs Medenî kelime payı (0.387), binom z / sqrt(phi=9.10), BH-FDR · **Ölçüt:** düzeltilmiş z = -3.513 · **p:** 0.0004 · **q:** 0.0278 · **Etki:** -1.142

Frekans 980 | Medenî pay 0.22 (beklenen 0.39) | token ağırlıklı ort. nüzul sırası 62.0 (genel 70.7)

<details><summary>Kanıt (5)</summary>

- 96:1
- 96:3
- 96:8
- 68:19
- 68:2

</details>

### ✅ Kök قتل: Medenî dönemde yoğunlaşıyor
**Yöntem:** Medenî token payı vs Medenî kelime payı (0.387), binom z / sqrt(phi=9.10), BH-FDR · **Ölçüt:** düzeltilmiş z = 3.506 · **p:** 0.0005 · **q:** 0.0278 · **Etki:** 2.493

Frekans 170 | Medenî pay 0.78 (beklenen 0.39) | token ağırlıklı ort. nüzul sırası 84.6 (genel 70.7)

<details><summary>Kanıt (5)</summary>

- 9:83
- 9:5
- 9:36
- 9:36
- 9:30

</details>

### ✅ Kök نفق: Medenî dönemde yoğunlaşıyor
**Yöntem:** Medenî token payı vs Medenî kelime payı (0.387), binom z / sqrt(phi=9.10), BH-FDR · **Ölçüt:** düzeltilmiş z = 3.554 · **p:** 0.0004 · **q:** 0.0278 · **Etki:** 3.529

Frekans 111 | Medenî pay 0.88 (beklenen 0.39) | token ağırlıklı ort. nüzul sırası 92.7 (genel 70.7)

<details><summary>Kanıt (5)</summary>

- 9:99
- 9:98
- 9:97
- 9:92
- 9:91

</details>

### ✅ Kök أمن (iman etmek, güvenmek): Medenî dönemde yoğunlaşıyor
**Yöntem:** Medenî token payı vs Medenî kelime payı (0.387), binom z / sqrt(phi=9.10), BH-FDR · **Ölçüt:** düzeltilmiş z = 3.663 · **p:** 0.0003 · **q:** 0.0278 · **Etki:** 1.061

Frekans 879 | Medenî pay 0.57 (beklenen 0.39) | token ağırlıklı ort. nüzul sırası 79.3 (genel 70.7)

<details><summary>Kanıt (5)</summary>

- 9:99
- 9:94
- 9:88
- 9:86
- 9:79

</details>

### ✅ Kök أله (Allah, ilah): Medenî dönemde yoğunlaşıyor
**Yöntem:** Medenî token payı vs Medenî kelime payı (0.387), binom z / sqrt(phi=9.10), BH-FDR · **Ölçüt:** düzeltilmiş z = 8.346 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 1.349

Frekans 2851 | Medenî pay 0.62 (beklenen 0.39) | token ağırlıklı ort. nüzul sırası 81.9 (genel 70.7)

<details><summary>Kanıt (5)</summary>

- 110:2
- 110:1
- 9:99
- 9:99
- 9:99

</details>

### 📋 305 sık kökün 5 tanesi Mekkî/Medenî dönemlerden birinde anlamlı yoğunlaşıyor (q<0.05)
**Yöntem:** Kök dönem taraması özeti (quasi-binom) · **Ölçüt:** anlamlı kök sayısı = 5

Medenî yoğunlaşan: 4 | Mekkî yoğunlaşan: 1 | aşırı yayılım phi=9.10

### 📋 En belirgin Mekkî kökler (etki büyüklüğü sıralaması, frekans>=50)
**Yöntem:** log2(Medenî/Mekkî token oranı ÷ kelime oranı); betimsel, test değil · **Ölçüt:** log2 oran = -3.063

<details><summary>Kanıt (15)</summary>

- سحر (-3.06)
- جرم (-2.56)
- قرأ (-2.24)
- وحي (-2.21)
- فري (-2.17)
- نذر (-2.04)
- ندي (-1.76)
- هلك (-1.66)
- عبد (kul, köle) (-1.57)
- خلق (yaratmak) (-1.55)
- قري (-1.52)
- عود (-1.38)
- ليل (-1.35)
- نجو (-1.29)
- أبو (-1.27)

</details>

### 📋 En belirgin Medenî kökler (etki büyüklüğü sıralaması, frekans>=50)
**Yöntem:** log2(Medenî/Mekkî token oranı ÷ kelime oranı); betimsel, test değil · **Ölçüt:** log2 oran = 3.529

<details><summary>Kanıt (15)</summary>

- نفق (+3.53)
- نسو (+3.07)
- قتل (+2.49)
- حلل (+2.17)
- توب (+2.12)
- عرف (+1.99)
- رضو (+1.95)
- صوب (+1.70)
- قلب (+1.58)
- حبب (+1.50)
- عدد (+1.43)
- فسق (+1.41)
- مول (+1.41)
- أله (Allah, ilah) (+1.35)
- بيت (+1.34)

</details>


## 12. Belâgat Örüntüleri (İltifat, Edilgen, Açılış, Edat İşlevleri)

_Çalışma süresi: 2.17 s_

### 📋 Gaibden muhataba iltifat: 61 geçiş tespit edildi (Allah'tan 3. şahısla söz → doğrudan hitap)
**Yöntem:** Önceki 1-3 ayette ilahî isim (Allah/Rab/Rahmân) + bu ayette 'iyyâke' ya da 'Rabbenâ/Rabbî'+2. tekil · **Ölçüt:** geçiş sayısı = 61

Allah'a doğrudan hitap içeren toplam ayet: 163. Kural tabanlı aday listesidir; Fâtiha 1:4→1:5 klasik örneği yakalandı.

<details><summary>Kanıt (40)</summary>

- 1:4→1:5
- 2:125→2:126
- 2:138→2:139
- 2:199→2:200
- 2:249→2:250
- 2:284→2:285
- 3:15→3:16
- 3:37→3:38
- 3:40→3:41
- 3:52→3:53
- 5:24→5:25
- 5:113→5:114
- 6:56→6:57
- 6:127→6:128
- 6:160→6:161

</details>

### ✅ İlahî referans 'Allah/O' ↔ 'Biz' arasında ardışık ayetlerde 152 kez kayıyor; rastgele sıralamada beklenen 183 — kayma rastlantıdan SEYREK (referans kümeleniyor)
**Yöntem:** Ayet etiketleri G (ilahî isim, 'Biz' yok) / W ('Biz' fiili, söz aktarımı yok); sure içi karıştırma, 1000 permütasyon · **Ölçüt:** z (gözlenen-null) = -2.669 · **p:** 0.0080 · **q:** 0.0277 · **Etki:** 0.832

Gözlenen 152 | null ort. 182.7 ± 11.5 | aynı ayet içinde hem ilahî isim hem 'Biz': 76 ayet. 'Biz' etiketi sezgiseldir (insan konuşması kısmen 'qâle' filtresiyle ayıklanır).

<details><summary>Kanıt (25)</summary>

- 2:62(G)→63(W)
- 2:105(G)→106(W)
- 2:124(G)→125(W)
- 2:130(W)→131(G)
- 2:146(W)→147(G)
- 3:43(G)→44(W)
- 4:64(W)→65(G)
- 4:65(G)→66(W)
- 5:64(G)→65(W)
- 5:65(W)→66(G)
- 6:44(W)→45(G)
- 6:54(G)→55(W)
- 6:75(W)→76(G)
- 6:106(G)→107(W)
- 6:145(G)→146(W)

</details>

### ✅ Ahiret sahnelerinde edilgen çatı 1.61 kat daha sık (fail gizlenir: 'sûra üfürülür', 'defterler açılır')
**Yöntem:** Ahiret sözcüklü ayetler (kıyamet, ahiret, cehennem, cennet, ateş, sûr, hesap...) vs diğerleri; sure içi etiket permütasyonu (1000) · **Ölçüt:** edilgen oranı farkı = 0.035 · **p:** 0.0020 · **q:** 0.0098 · **Etki:** 1.614

Ahiret ayetleri: 287 ayet, 1066 fiil, edilgen %9.3 | Diğer: 18287 fiil, %5.8

<details><summary>Kanıt (20)</summary>

- 2:24
- 2:85
- 2:119
- 2:212
- 3:19
- 3:131
- 3:161
- 3:180
- 3:185
- 3:199
- 5:4
- 5:14
- 5:36
- 5:64
- 6:27

</details>

### ✅ Kök نزل (indirmek): fiilleri %26 edilgen (genel %5.9)
**Yöntem:** Kök bazında edilgen payı, binom z / sqrt(phi=5.14), BH-FDR · **Ölçüt:** düzeltilmiş z = 6.112 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 4.432

68/258 edilgen

### ✅ Kök رجع: fiilleri %41 edilgen (genel %5.9)
**Yöntem:** Kök bazında edilgen payı, binom z / sqrt(phi=5.14), BH-FDR · **Ölçüt:** düzeltilmiş z = 5.887 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 6.936

33/80 edilgen

### ✅ Kök ردد: fiilleri %49 edilgen (genel %5.9)
**Yöntem:** Kök bazında edilgen payı, binom z / sqrt(phi=5.14), BH-FDR · **Ölçüt:** düzeltilmiş z = 5.370 · **p:** 0.0000 · **q:** 5.0e-06 · **Etki:** 8.220

22/45 edilgen

### ✅ Kök تلو: fiilleri %39 edilgen (genel %5.9)
**Yöntem:** Kök bazında edilgen payı, binom z / sqrt(phi=5.14), BH-FDR · **Ölçüt:** düzeltilmiş z = 4.863 · **p:** 1.0e-06 · **q:** 4.9e-05 · **Etki:** 6.615

24/61 edilgen

### ✅ Kök حشر: fiilleri %49 edilgen (genel %5.9)
**Yöntem:** Kök bazında edilgen payı, binom z / sqrt(phi=5.14), BH-FDR · **Ölçüt:** düzeltilmiş z = 4.843 · **p:** 1.0e-06 · **q:** 4.9e-05 · **Etki:** 8.180

18/37 edilgen

### ✅ Kök وعد: fiilleri %36 edilgen (genel %5.9)
**Yöntem:** Kök bazında edilgen payı, binom z / sqrt(phi=5.14), BH-FDR · **Ölçüt:** düzeltilmiş z = 4.807 · **p:** 2.0e-06 · **q:** 4.9e-05 · **Etki:** 5.973

27/76 edilgen

### ✅ Kök وحي: fiilleri %36 edilgen (genel %5.9)
**Yöntem:** Kök bazında edilgen payı, binom z / sqrt(phi=5.14), BH-FDR · **Ölçüt:** düzeltilmiş z = 4.772 · **p:** 2.0e-06 · **q:** 5.0e-05 · **Etki:** 6.072

26/72 edilgen

### ✅ Kök قضي: fiilleri %39 edilgen (genel %5.9)
**Yöntem:** Kök bazında edilgen payı, binom z / sqrt(phi=5.14), BH-FDR · **Ölçüt:** düzeltilmiş z = 4.731 · **p:** 2.0e-06 · **q:** 5.3e-05 · **Etki:** 6.555

23/59 edilgen

### ✅ Kök جزي: fiilleri %31 edilgen (genel %5.9)
**Yöntem:** Kök bazında edilgen payı, binom z / sqrt(phi=5.14), BH-FDR · **Ölçüt:** düzeltilmiş z = 4.031 · **p:** 5.6e-05 · **q:** 0.0011 · **Etki:** 5.226

23/74 edilgen

### ✅ Kök أمر (emir, buyruk): fiilleri %29 edilgen (genel %5.9)
**Yöntem:** Kök bazında edilgen payı, binom z / sqrt(phi=5.14), BH-FDR · **Ölçüt:** düzeltilmiş z = 3.839 · **p:** 0.0001 · **q:** 0.0021 · **Etki:** 4.895

23/79 edilgen

### ✅ Kök زين: fiilleri %37 edilgen (genel %5.9)
**Yöntem:** Kök bazında edilgen payı, binom z / sqrt(phi=5.14), BH-FDR · **Ölçüt:** düzeltilmiş z = 3.012 · **p:** 0.0026 · **q:** 0.0413 · **Etki:** 6.227

10/27 edilgen

### ✅ Kök قبل (önce): fiilleri %36 edilgen (genel %5.9)
**Yöntem:** Kök bazında edilgen payı, binom z / sqrt(phi=5.14), BH-FDR · **Ölçüt:** düzeltilmiş z = 2.937 · **p:** 0.0033 · **q:** 0.0472 · **Etki:** 6.005

10/28 edilgen

### ✅ Kök أتي (vermek): fiilleri %13 edilgen (genel %5.9)
**Yöntem:** Kök bazında edilgen payı, binom z / sqrt(phi=5.14), BH-FDR · **Ölçüt:** düzeltilmiş z = 2.916 · **p:** 0.0035 · **q:** 0.0472 · **Etki:** 2.137

68/535 edilgen

### ✅ Kök ظلم (zulmetmek, haksızlık): fiilleri %21 edilgen (genel %5.9)
**Yöntem:** Kök bazında edilgen payı, binom z / sqrt(phi=5.14), BH-FDR · **Ölçüt:** düzeltilmiş z = 2.902 · **p:** 0.0037 · **q:** 0.0472 · **Etki:** 3.484

23/111 edilgen

### 📋 191 fiil kökünün 14 tanesi anlamlı biçimde edilgene yatkın (q<0.05)
**Yöntem:** Kök bazında edilgen taraması özeti · **Ölçüt:** anlamlı kök = 14

<details><summary>Kanıt (14)</summary>

- نزل (indirmek) (68/258 edilgen)
- رجع (33/80 edilgen)
- ردد (22/45 edilgen)
- تلو (24/61 edilgen)
- حشر (18/37 edilgen)
- وعد (27/76 edilgen)
- وحي (26/72 edilgen)
- قضي (23/59 edilgen)
- جزي (23/74 edilgen)
- أمر (emir, buyruk) (23/79 edilgen)
- زين (10/27 edilgen)
- قبل (önce) (10/28 edilgen)
- أتي (vermek) (68/535 edilgen)
- ظلم (zulmetmek, haksızlık) (23/111 edilgen)

</details>

### ⚪ 'Hurûf-ı mukattaa' açılışlı 29 sure: ort. nüzul sırası 58 (diğerleri 57), 26/29 Mekkî
**Yöntem:** Sure açılış türü vs nüzul sırası, Mann-Whitney U · **Ölçüt:** z = 0.101 · **p:** 0.9197 · **q:** 0.9475

<details><summary>Kanıt (29)</summary>

- Bakara
- Âl-i İmrân
- A'râf
- Yûnus
- Hûd
- Yûsuf
- Ra'd
- İbrâhîm
- Hicr
- Meryem
- Tâhâ
- Şuarâ
- Neml
- Kasas
- Ankebût

</details>

### ⚪ 'Nida (Ey ...)' açılışlı 10 sure: ort. nüzul sırası 81 (diğerleri 55), 2/10 Mekkî
**Yöntem:** Sure açılış türü vs nüzul sırası, Mann-Whitney U · **Ölçüt:** z = 2.324 · **p:** 0.0201 · **q:** 0.0527

<details><summary>Kanıt (10)</summary>

- Nisâ
- Mâide
- Hac
- Ahzâb
- Hucurât
- Mümtehine
- Talâk
- Tahrîm
- Müzzemmil
- Müddessir

</details>

### ⚪ 'Hamd/Tesbih' açılışlı 13 sure: ort. nüzul sırası 71 (diğerleri 56), 8/13 Mekkî
**Yöntem:** Sure açılış türü vs nüzul sırası, Mann-Whitney U · **Ölçüt:** z = 1.573 · **p:** 0.1156 · **q:** 0.1965

<details><summary>Kanıt (13)</summary>

- En'âm
- İsrâ
- Kehf
- Furkân
- Sebe'
- Fâtır
- Hadîd
- Haşr
- Saf
- Cuma
- Tegâbün
- Mülk
- A'lâ

</details>

### ✅ 'Yemin' açılışlı 15 sure: ort. nüzul sırası 29 (diğerleri 62), 15/15 Mekkî
**Yöntem:** Sure açılış türü vs nüzul sırası, Mann-Whitney U · **Ölçüt:** z = -3.600 · **p:** 0.0003 · **q:** 0.0027

<details><summary>Kanıt (15)</summary>

- Sâffât
- Necm
- Kıyâme
- Mürselât
- Nâziât
- Bürûc
- Târık
- Fecr
- Beled
- Şems
- Leyl
- Duhâ
- Tîn
- Âdiyât
- Asr

</details>

### ✅ 'Emir (Kul/İkra)' açılışlı 6 sure: ort. nüzul sırası 20 (diğerleri 60), 6/6 Mekkî
**Yöntem:** Sure açılış türü vs nüzul sırası, Mann-Whitney U · **Ölçüt:** z = -2.830 · **p:** 0.0047 · **q:** 0.0198

<details><summary>Kanıt (6)</summary>

- Cin
- Alak
- Kâfirûn
- İhlâs
- Felak
- Nâs

</details>

### ⚪ 'Soru' açılışlı 6 sure: ort. nüzul sırası 49 (diğerleri 58), 5/6 Mekkî
**Yöntem:** Sure açılış türü vs nüzul sırası, Mann-Whitney U · **Ölçüt:** z = -0.647 · **p:** 0.5175 · **q:** 0.6284

<details><summary>Kanıt (6)</summary>

- İnsân (Dehr)
- Nebe'
- Gâşiye
- İnşirâh
- Fîl
- Mâûn

</details>

### ✅ Hurûf-ı mukattaa ile açılan 29 surenin 26'ü hemen ardından Kitap/vahye atıf yapıyor (diğer surelerde 20/85)
**Yöntem:** Mukattaa sonrası ilk 2 ayet vs diğer surelerin ilk 2 ayeti; kökler: كتب نزل قرأ ذكر وحي آيي; tek yönlü Fisher · **Ölçüt:** oran farkı = 0.661 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 3.810

Kanıt listesi: atıf YAPMAYAN mukattaa sureleri (istisnalar).

<details><summary>Kanıt (3)</summary>

- Ankebût
- Rûm
- Kalem

</details>

### ⚪ Hasr/sınırlama (innemâ vb.): Medenî/Mekkî yoğunluk oranı 0.47x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = -1.086 · **p:** 0.2774 · **q:** 0.4076 · **Etki:** 0.472

Toplam 557 | Mekkî 9.04‰ | Medenî 4.27‰

### ⚪ İstisna (illâ): Medenî/Mekkî yoğunluk oranı 2.57x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = 0.797 · **p:** 0.4257 · **q:** 0.5361 · **Etki:** 2.570

Toplam 105 | Mekkî 0.84‰ | Medenî 2.17‰

### ⚪ Şaşırtma (izâ el-fucâiyye): Medenî/Mekkî yoğunluk oranı 0.13x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = -1.063 · **p:** 0.2877 · **q:** 0.4076 · **Etki:** 0.128

Toplam 40 | Mekkî 0.78‰ | Medenî 0.10‰

### ⚪ Sakındırma/kınama (kellâ): Medenî/Mekkî yoğunluk oranı 0.00x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = -1.382 · **p:** 0.1668 · **q:** 0.2701 · **Etki:** 0.000

Toplam 33 | Mekkî 0.70‰ | Medenî 0.00‰

### ⚪ Teşvik (hallâ, levlâ): Medenî/Mekkî yoğunluk oranı 0.65x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = 1.116 · **p:** 0.2645 · **q:** 0.4076 · **Etki:** 0.655

Toplam 41 | Mekkî 0.61‰ | Medenî 0.40‰

### ⚪ İstidrak/iptal (bel): Medenî/Mekkî yoğunluk oranı 0.31x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = -2.258 · **p:** 0.0240 · **q:** 0.0554 · **Etki:** 0.310

Toplam 122 | Mekkî 2.15‰ | Medenî 0.67‰

### ⚪ Cevap (neam, belâ): Medenî/Mekkî yoğunluk oranı 0.50x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = -0.615 · **p:** 0.5382 · **q:** 0.6310 · **Etki:** 0.503

Toplam 58 | Mekkî 0.93‰ | Medenî 0.47‰

### ⚪ Başlangıç (ellâ, emâ): Medenî/Mekkî yoğunluk oranı 0.44x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = -0.270 · **p:** 0.7872 · **q:** 0.8634 · **Etki:** 0.435

Toplam 51 | Mekkî 0.84‰ | Medenî 0.37‰

### ✅ Amaç (li, key): Medenî/Mekkî yoğunluk oranı 1.12x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = 2.462 · **p:** 0.0138 · **q:** 0.0391 · **Etki:** 1.117

Toplam 319 | Mekkî 3.94‰ | Medenî 4.40‰

### ⚪ Sebep: Medenî/Mekkî yoğunluk oranı 1.15x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = 1.682 · **p:** 0.0926 · **q:** 0.1749 · **Etki:** 1.148

Toplam 88 | Mekkî 1.08‰ | Medenî 1.23‰

### ✅ Hâl vavı: Medenî/Mekkî yoğunluk oranı 2.01x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = 3.087 · **p:** 0.0020 · **q:** 0.0098 · **Etki:** 2.011

Toplam 293 | Mekkî 2.72‰ | Medenî 5.47‰

### ⚪ Netice fâsı: Medenî/Mekkî yoğunluk oranı 6.94x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = 2.248 · **p:** 0.0246 · **q:** 0.0554 · **Etki:** 6.936

Toplam 350 | Mekkî 1.37‰ | Medenî 9.50‰

### ⚪ Tefsir/açıklama: Medenî/Mekkî yoğunluk oranı 0.37x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = -0.049 · **p:** 0.9606 · **q:** 0.9606 · **Etki:** 0.375

Toplam 47 | Mekkî 0.80‰ | Medenî 0.30‰

### ⚪ Düzeltme (lâkin): Medenî/Mekkî yoğunluk oranı 1.44x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = 0.981 · **p:** 0.3267 · **q:** 0.4443 · **Etki:** 1.442

Toplam 65 | Mekkî 0.72‰ | Medenî 1.03‰

### ⚪ Ek/zâid edat: Medenî/Mekkî yoğunluk oranı 0.66x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = -1.633 · **p:** 0.1026 · **q:** 0.1835 · **Etki:** 0.663

Toplam 237 | Mekkî 3.52‰ | Medenî 2.33‰

### ⚪ Engelleme: Medenî/Mekkî yoğunluk oranı 1.06x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = 2.172 · **p:** 0.0298 · **q:** 0.0597 · **Etki:** 1.060

Toplam 162 | Mekkî 2.04‰ | Medenî 2.17‰

### ⚪ Gelecek (se/sevfe): Medenî/Mekkî yoğunluk oranı 0.71x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = -0.876 · **p:** 0.3813 · **q:** 0.4986 · **Etki:** 0.713

Toplam 161 | Mekkî 2.34‰ | Medenî 1.67‰

### ✅ Yasaklama (lâ nâhiye): Medenî/Mekkî yoğunluk oranı 1.66x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = 2.646 · **p:** 0.0081 · **q:** 0.0277 · **Etki:** 1.660

Toplam 332 | Mekkî 3.41‰ | Medenî 5.67‰

### ⚪ Tahkik (kad): Medenî/Mekkî yoğunluk oranı 0.85x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = 0.441 · **p:** 0.6592 · **q:** 0.7471 · **Etki:** 0.850

Toplam 415 | Mekkî 5.69‰ | Medenî 4.83‰

### ⚪ Tekit (le, inne): Medenî/Mekkî yoğunluk oranı 0.56x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = -2.225 · **p:** 0.0261 · **q:** 0.0554 · **Etki:** 0.559

Toplam 1244 | Mekkî 19.37‰ | Medenî 10.84‰

### ✅ Soru: Medenî/Mekkî yoğunluk oranı 0.56x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = -3.598 · **p:** 0.0003 · **q:** 0.0027 · **Etki:** 0.557

Toplam 902 | Mekkî 14.06‰ | Medenî 7.84‰

### ✅ Olumsuzluk: Medenî/Mekkî yoğunluk oranı 0.84x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = -2.508 · **p:** 0.0121 · **q:** 0.0375 · **Etki:** 0.836

Toplam 2696 | Mekkî 37.18‰ | Medenî 31.08‰

### ✅ Şart: Medenî/Mekkî yoğunluk oranı 1.89x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = 3.884 · **p:** 0.0001 · **q:** 0.0017 · **Etki:** 1.889

Toplam 1029 | Mekkî 9.89‰ | Medenî 18.67‰

### ✅ Nida: Medenî/Mekkî yoğunluk oranı 1.34x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = 3.226 · **p:** 0.0013 · **q:** 0.0085 · **Etki:** 1.342

Toplam 366 | Mekkî 4.17‰ | Medenî 5.60‰

### ⚪ Açıklama/ayrıntı (emmâ): Medenî/Mekkî yoğunluk oranı 0.65x
**Yöntem:** Sure bazında ‰ kelime yoğunluğu, Mekkî (86) vs Medenî (28), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = -0.181 · **p:** 0.8563 · **q:** 0.9099 · **Etki:** 0.646

Toplam 69 | Mekkî 1.03‰ | Medenî 0.67‰


## 13. Sayı Morfolojisi (Tekil-İkil-Çoğul) ve Fiil Babları

_Çalışma süresi: 0.09 s_

### 📋 156 sık isim lemmasının 66 tanesi Kur'an'da hiç çoğul/ikil kullanılmıyor
**Yöntem:** İsim lemmaları (>= 30 token), sayı etiketi; sayısız eril/dişil etiket tekil sayılır · **Ölçüt:** yalnız tekil lemma = 66

Genel dağılım: tekil %73.2, ikil %0.9, çoğul %25.9. Not: kırık çoğulların bir kısmı korpus tarafından ayrı lemma olarak kaydedilmiş olabilir.

<details><summary>Kanıt (30)</summary>

- أَرْض (461)
- قَوْم (383)
- كُلّ (359)
- عَذاب (322)
- حَقّ (242)
- بَعْض (157)
- نار (145)
- غَيْر (144)
- أَهْل (121)
- رَحْمَة (114)
- عِلْم (105)
- قَوْل (92)
- دِين (85)
- هُدًى (85)
- فَضْل (84)

</details>

### 📋 38 sık isim lemması ağırlıkla (>= %60) çoğul kullanılıyor
**Yöntem:** İsim lemmaları (>= 30 token), çoğul payı · **Ölçüt:** çoğul baskın lemma = 38

<details><summary>Kanıt (30)</summary>

- عالَم (%100 çoğul, n=73)
- مُتَّقي (%100 çoğul, n=49)
- ناس (%100 çoğul, n=241)
- صالِحَة (%100 çoğul, n=62)
- خاسِر (%100 çoğul, n=32)
- أَصْحاب (%100 çoğul, n=78)
- نِساء (%100 çoğul, n=59)
- آباء (%100 çoğul, n=64)
- آلاء (%100 çoğul, n=34)
- نَعَم (%97 çoğul, n=33)
- كافِر (%97 çoğul, n=146)
- ظالِم (%96 çoğul, n=105)
- مُشْرِك (%95 çoğul, n=44)
- مُجْرِم (%95 çoğul, n=44)
- صادِق (%95 çoğul, n=59)

</details>

### ✅ 'سَماء' yanında 'أَرْض' varken %79 çoğul, yokken %9 çoğul
**Yöntem:** b'nin ortak ayetlerdeki vs diğer ayetlerdeki tekil/çoğul sayımı; iki yönlü Fisher, BH-FDR · **Ölçüt:** çoğul oranı farkı = 0.694 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 0.694

Ortak 222 ayet | 'سَماء' ortak: 183 çoğul/50 tekil | diğer: 7 çoğul/70 tekil | 'أَرْض' çoğul payı genel %0

<details><summary>Kanıt (12)</summary>

- 2:22
- 2:29
- 2:33
- 2:107
- 2:116
- 2:117
- 2:164
- 2:255
- 2:284
- 3:5
- 3:29
- 3:83

</details>

### ✅ 'ابْن' yanında 'نِساء' varken %100 çoğul, yokken %17 çoğul
**Yöntem:** b'nin ortak ayetlerdeki vs diğer ayetlerdeki tekil/çoğul sayımı; iki yönlü Fisher, BH-FDR · **Ölçüt:** çoğul oranı farkı = 0.833 · **p:** 0.0000 · **q:** 1.0e-06 · **Etki:** 0.833

Ortak 11 ayet | 'ابْن' ortak: 15 çoğul/0 tekil | diğer: 8 çoğul/40 tekil | 'نِساء' çoğul payı genel %100

<details><summary>Kanıt (11)</summary>

- 2:49
- 3:61
- 4:11
- 4:23
- 7:127
- 7:141
- 14:6
- 24:31
- 28:4
- 33:55
- 40:25

</details>

### ✅ 'ذُو' yanında 'أَلْباب' varken %100 çoğul, yokken %25 çoğul
**Yöntem:** b'nin ortak ayetlerdeki vs diğer ayetlerdeki tekil/çoğul sayımı; iki yönlü Fisher, BH-FDR · **Ölçüt:** çoğul oranı farkı = 0.748 · **p:** 0.0000 · **q:** 1.0e-06 · **Etki:** 0.748

Ortak 15 ayet | 'ذُو' ortak: 15 çoğul/0 tekil | diğer: 35 çoğul/104 tekil | 'أَلْباب' çoğul payı genel %100

<details><summary>Kanıt (12)</summary>

- 2:179
- 2:197
- 2:269
- 3:7
- 3:190
- 5:100
- 13:19
- 14:52
- 38:29
- 38:43
- 39:9
- 39:18

</details>

### ✅ 'آيَة' yanında 'أَكْثَر' varken %8 çoğul, yokken %80 çoğul
**Yöntem:** b'nin ortak ayetlerdeki vs diğer ayetlerdeki tekil/çoğul sayımı; iki yönlü Fisher, BH-FDR · **Ölçüt:** çoğul oranı farkı = -0.723 · **p:** 0.0000 · **q:** 6.0e-06 · **Etki:** -0.723

Ortak 11 ayet | 'آيَة' ortak: 1 çoğul/12 tekil | diğer: 295 çoğul/74 tekil | 'أَكْثَر' çoğul payı genel %0

<details><summary>Kanıt (11)</summary>

- 6:37
- 13:1
- 16:101
- 26:8
- 26:67
- 26:103
- 26:121
- 26:139
- 26:158
- 26:174
- 26:190

</details>

### ✅ 'سَماء' yanında 'ماء' varken %18 çoğul, yokken %66 çoğul
**Yöntem:** b'nin ortak ayetlerdeki vs diğer ayetlerdeki tekil/çoğul sayımı; iki yönlü Fisher, BH-FDR · **Ölçüt:** çoğul oranı farkı = -0.482 · **p:** 0.0000 · **q:** 7.0e-06 · **Etki:** -0.482

Ortak 27 ayet | 'سَماء' ortak: 6 çoğul/27 tekil | diğer: 184 çoğul/93 tekil | 'ماء' çoğul payı genel %0

<details><summary>Kanıt (12)</summary>

- 2:22
- 2:164
- 6:99
- 8:11
- 10:24
- 11:7
- 11:44
- 13:17
- 14:32
- 15:22
- 16:10
- 16:65

</details>

### ✅ 'رَسُول' yanında 'بَيِّنَة' varken %76 çoğul, yokken %25 çoğul
**Yöntem:** b'nin ortak ayetlerdeki vs diğer ayetlerdeki tekil/çoğul sayımı; iki yönlü Fisher, BH-FDR · **Ölçüt:** çoğul oranı farkı = 0.506 · **p:** 1.0e-06 · **q:** 2.7e-05 · **Etki:** 0.506

Ortak 21 ayet | 'رَسُول' ortak: 19 çoğul/6 tekil | diğer: 78 çoğul/229 tekil | 'بَيِّنَة' çoğul payı genel %69

<details><summary>Kanıt (12)</summary>

- 2:87
- 2:253
- 3:86
- 3:183
- 3:184
- 5:32
- 7:101
- 9:70
- 10:13
- 10:74
- 14:9
- 30:9

</details>

### ✅ 'آيَة' yanında 'مُؤْمِن' varken %30 çoğul, yokken %81 çoğul
**Yöntem:** b'nin ortak ayetlerdeki vs diğer ayetlerdeki tekil/çoğul sayımı; iki yönlü Fisher, BH-FDR · **Ölçüt:** çoğul oranı farkı = -0.501 · **p:** 1.0e-06 · **q:** 3.1e-05 · **Etki:** -0.501

Ortak 21 ayet | 'آيَة' ortak: 7 çoğul/16 tekil | diğer: 289 çoğul/70 tekil | 'مُؤْمِن' çoğul payı genel %90

<details><summary>Kanıt (12)</summary>

- 2:248
- 3:49
- 3:164
- 6:27
- 6:118
- 7:72
- 7:132
- 8:2
- 15:77
- 26:8
- 26:67
- 26:103

</details>

### ✅ 'أَخ' yanında 'آباء' varken %100 çoğul, yokken %20 çoğul
**Yöntem:** b'nin ortak ayetlerdeki vs diğer ayetlerdeki tekil/çoğul sayımı; iki yönlü Fisher, BH-FDR · **Ölçüt:** çoğul oranı farkı = 0.800 · **p:** 1.0e-06 · **q:** 4.5e-05 · **Etki:** 0.800

Ortak 8 ayet | 'أَخ' ortak: 10 çoğul/0 tekil | diğer: 13 çoğul/52 tekil | 'آباء' çoğul payı genel %100

<details><summary>Kanıt (8)</summary>

- 6:87
- 9:23
- 9:24
- 24:31
- 24:61
- 33:5
- 33:55
- 58:22

</details>

### ✅ 'سَماء' yanında 'مُلْك' varken %100 çoğul, yokken %58 çoğul
**Yöntem:** b'nin ortak ayetlerdeki vs diğer ayetlerdeki tekil/çoğul sayımı; iki yönlü Fisher, BH-FDR · **Ölçüt:** çoğul oranı farkı = 0.417 · **p:** 1.5e-05 · **q:** 0.0004 · **Etki:** 0.417

Ortak 22 ayet | 'سَماء' ortak: 22 çoğul/0 tekil | diğer: 168 çoğul/120 tekil | 'مُلْك' çoğul payı genel %0

<details><summary>Kanıt (12)</summary>

- 2:107
- 3:189
- 5:17
- 5:18
- 5:40
- 5:120
- 6:73
- 7:158
- 9:116
- 12:101
- 24:42
- 25:2

</details>

### ✅ 'بَيِّنَة' yanında 'رَسُول' varken %100 çoğul, yokken %48 çoğul
**Yöntem:** b'nin ortak ayetlerdeki vs diğer ayetlerdeki tekil/çoğul sayımı; iki yönlü Fisher, BH-FDR · **Ölçüt:** çoğul oranı farkı = 0.515 · **p:** 1.8e-05 · **q:** 0.0005 · **Etki:** 0.515

Ortak 21 ayet | 'بَيِّنَة' ortak: 22 çoğul/0 tekil | diğer: 16 çoğul/17 tekil | 'رَسُول' çoğul payı genel %29

<details><summary>Kanıt (12)</summary>

- 2:87
- 2:253
- 3:86
- 3:183
- 3:184
- 5:32
- 7:101
- 9:70
- 10:13
- 10:74
- 14:9
- 30:9

</details>

### ✅ 'بَيِّنَة' yanında 'رَبّ' varken %27 çoğul, yokken %85 çoğul
**Yöntem:** b'nin ortak ayetlerdeki vs diğer ayetlerdeki tekil/çoğul sayımı; iki yönlü Fisher, BH-FDR · **Ölçüt:** çoğul oranı farkı = -0.583 · **p:** 8.1e-05 · **q:** 0.0019 · **Etki:** -0.583

Ortak 15 ayet | 'بَيِّنَة' ortak: 4 çoğul/11 tekil | diğer: 34 çoğul/6 tekil | 'رَبّ' çoğul payı genel %0

<details><summary>Kanıt (12)</summary>

- 6:57
- 6:157
- 7:73
- 7:85
- 7:105
- 10:15
- 11:17
- 11:28
- 11:63
- 11:88
- 20:133
- 40:28

</details>

### ✅ 'نَفْس' yanında 'مال' varken %94 çoğul, yokken %50 çoğul
**Yöntem:** b'nin ortak ayetlerdeki vs diğer ayetlerdeki tekil/çoğul sayımı; iki yönlü Fisher, BH-FDR · **Ölçüt:** çoğul oranı farkı = 0.446 · **p:** 0.0001 · **q:** 0.0028 · **Etki:** 0.446

Ortak 17 ayet | 'نَفْس' ortak: 17 çoğul/1 tekil | diğer: 138 çoğul/139 tekil | 'مال' çoğul payı genel %71

<details><summary>Kanıt (12)</summary>

- 2:155
- 2:265
- 3:186
- 4:29
- 4:95
- 6:152
- 8:72
- 9:20
- 9:41
- 9:44
- 9:55
- 9:81

</details>

### ✅ 'وَلِيّ' yanında 'نَصِير' varken %6 çoğul, yokken %59 çoğul
**Yöntem:** b'nin ortak ayetlerdeki vs diğer ayetlerdeki tekil/çoğul sayımı; iki yönlü Fisher, BH-FDR · **Ölçüt:** çoğul oranı farkı = -0.523 · **p:** 0.0002 · **q:** 0.0030 · **Etki:** -0.523

Ortak 15 ayet | 'وَلِيّ' ortak: 1 çoğul/15 tekil | diğer: 41 çoğul/29 tekil | 'نَصِير' çoğul payı genel %32

<details><summary>Kanıt (12)</summary>

- 2:107
- 2:120
- 4:45
- 4:75
- 4:89
- 4:123
- 4:173
- 9:74
- 9:116
- 29:22
- 33:17
- 33:65

</details>

### ✅ 'وَلَد' yanında 'مال' varken %81 çoğul, yokken %25 çoğul
**Yöntem:** b'nin ortak ayetlerdeki vs diğer ayetlerdeki tekil/çoğul sayımı; iki yönlü Fisher, BH-FDR · **Ölçüt:** çoğul oranı farkı = 0.562 · **p:** 0.0002 · **q:** 0.0035 · **Etki:** 0.562

Ortak 16 ayet | 'وَلَد' ortak: 13 çoğul/3 tekil | diğer: 10 çoğul/30 tekil | 'مال' çoğul payı genel %71

<details><summary>Kanıt (12)</summary>

- 3:10
- 3:116
- 8:28
- 9:55
- 9:69
- 9:85
- 17:64
- 18:39
- 19:77
- 34:35
- 34:37
- 57:20

</details>

### ✅ 'سَماء' yanında 'شَىْء' varken %87 çoğul, yokken %58 çoğul
**Yöntem:** b'nin ortak ayetlerdeki vs diğer ayetlerdeki tekil/çoğul sayımı; iki yönlü Fisher, BH-FDR · **Ölçüt:** çoğul oranı farkı = 0.291 · **p:** 0.0003 · **q:** 0.0059 · **Etki:** 0.291

Ortak 36 ayet | 'سَماء' ortak: 33 çoğul/5 tekil | diğer: 157 çoğul/115 tekil | 'شَىْء' çoğul payı genel %1

<details><summary>Kanıt (12)</summary>

- 2:29
- 2:255
- 2:284
- 3:5
- 3:29
- 3:189
- 4:126
- 5:17
- 5:40
- 5:97
- 5:120
- 6:99

</details>

### 📋 262 eşdizim çiftinin 22 tanesinde ortak lemma tekil/çoğul seçimini anlamlı değiştiriyor (q<0.05)
**Yöntem:** Eşdizim-sayı etkisi taraması özeti · **Ölçüt:** anlamlı çift = 22

<details><summary>Kanıt (20)</summary>

- 'سَماء' yanında 'أَرْض' varken %79 çoğul, yokken %9 çoğul
- 'ابْن' yanında 'نِساء' varken %100 çoğul, yokken %17 çoğul
- 'ذُو' yanında 'أَلْباب' varken %100 çoğul, yokken %25 çoğul
- 'آيَة' yanında 'أَكْثَر' varken %8 çoğul, yokken %80 çoğul
- 'سَماء' yanında 'ماء' varken %18 çoğul, yokken %66 çoğul
- 'رَسُول' yanında 'بَيِّنَة' varken %76 çoğul, yokken %25 çoğul
- 'آيَة' yanında 'مُؤْمِن' varken %30 çoğul, yokken %81 çoğul
- 'أَخ' yanında 'آباء' varken %100 çoğul, yokken %20 çoğul
- 'سَماء' yanında 'مُلْك' varken %100 çoğul, yokken %58 çoğul
- 'بَيِّنَة' yanında 'رَسُول' varken %100 çoğul, yokken %48 çoğul
- 'بَيِّنَة' yanında 'رَبّ' varken %27 çoğul, yokken %85 çoğul
- 'نَفْس' yanında 'مال' varken %94 çoğul, yokken %50 çoğul
- 'وَلِيّ' yanında 'نَصِير' varken %6 çoğul, yokken %59 çoğul
- 'وَلَد' yanında 'مال' varken %81 çoğul, yokken %25 çoğul
- 'سَماء' yanında 'شَىْء' varken %87 çoğul, yokken %58 çoğul

</details>

### 📋 İkil envanteri: 83 farklı isim lemması ikil biçimde, toplam 229 kez
**Yöntem:** İsim segmentlerinde sayı etiketi D · **Ölçüt:** ikil lemma = 83

<details><summary>Kanıt (25)</summary>

- يَد ×33 (2:66, 2:97, 3:3)
- اثْنَيْن ×13 (5:12, 5:106, 6:143)
- والِد ×10 (2:83, 2:180, 2:215)
- والِدَي ×10 (14:41, 19:14, 27:19)
- جَنَّة ×8 (18:32, 18:33, 34:15)
- اثْنَتَيْن ×7 (2:60, 4:11, 4:176)
- أَبَوان ×7 (4:11, 4:11, 7:27)
- زَوْج ×7 (11:40, 13:3, 23:27)
- عَيْن ×7 (12:84, 15:88, 18:28)
- مَرَّة ×6 (2:229, 9:101, 9:126)
- أُنثَيَيْن ×6 (4:11, 4:176, 6:143)
- رَجُل ×5 (2:282, 5:23, 16:76)
- ذُو ×5 (5:95, 5:106, 34:16)
- بَحْر ×5 (18:60, 25:53, 27:61)
- طائِفَة ×4 (3:122, 6:156, 8:7)

</details>

### 📋 İkil yoğunluğu en yüksek sure Rahmân (353‰, genel 9.9‰); 2. şahıs ikil hitabın %49'i Rahmân suresinde
**Yöntem:** Tüm ikil segmentler (isim, fiil, zamir) / sure kelime sayısı · **Ölçüt:** ‰ kelime = 353.276

Rahmân suresinin ikil hitabı (insan ve cin: 'ikiniz') klasik tefsirde bilinir; burada tüm sureler arasında nicel sıralaması verilir.

<details><summary>Kanıt (10)</summary>

- Rahmân 353.3‰
- Tahrîm 68.3‰
- Tebbet (Mesed) 43.5‰
- Kehf 41.2‰
- Beled 36.6‰
- Tâhâ 30.7‰
- Kasas 20.3‰
- Mücâdele 19.1‰
- Ahkâf 18.7‰
- Hucurât 17.3‰

</details>

### ✅ Fiil babı I (fe'ale): Medenî/Mekkî oranı 0.88x
**Yöntem:** Sure bazında ‰ fiil yoğunluğu, Mann-Whitney U (Medenî > Mekkî pozitif) · **Ölçüt:** z = -3.897 · **p:** 9.7e-05 · **q:** 0.0004 · **Etki:** 0.878

Toplam 12323 | Mekkî 667.5‰ | Medenî 586.3‰

### ⚪ Fiil babı II (tef'îl): Medenî/Mekkî oranı 1.13x
**Yöntem:** Sure bazında ‰ fiil yoğunluğu, Mann-Whitney U (Medenî > Mekkî pozitif) · **Ölçüt:** z = 1.554 · **p:** 0.1203 · **q:** 0.2079 · **Etki:** 1.132

Toplam 1300 | Mekkî 64.0‰ | Medenî 72.4‰

### ✅ Fiil babı III (müfâale): Medenî/Mekkî oranı 2.56x
**Yöntem:** Sure bazında ‰ fiil yoğunluğu, Mann-Whitney U (Medenî > Mekkî pozitif) · **Ölçüt:** z = 4.592 · **p:** 4.0e-06 · **q:** 4.0e-05 · **Etki:** 2.559

Toplam 338 | Mekkî 11.0‰ | Medenî 28.1‰

### ✅ Fiil babı IV (if'âl): Medenî/Mekkî oranı 1.26x
**Yöntem:** Sure bazında ‰ fiil yoğunluğu, Mann-Whitney U (Medenî > Mekkî pozitif) · **Ölçüt:** z = 3.410 · **p:** 0.0006 · **q:** 0.0019 · **Etki:** 1.264

Toplam 3499 | Mekkî 164.4‰ | Medenî 207.7‰

### ⚪ Fiil babı V (tefa''ul): Medenî/Mekkî oranı 1.38x
**Yöntem:** Sure bazında ‰ fiil yoğunluğu, Mann-Whitney U (Medenî > Mekkî pozitif) · **Ölçüt:** z = 1.652 · **p:** 0.0985 · **q:** 0.2079 · **Etki:** 1.377

Toplam 414 | Mekkî 18.7‰ | Medenî 25.8‰

### ⚪ Fiil babı VI (tefâ'ul): Medenî/Mekkî oranı 0.98x
**Yöntem:** Sure bazında ‰ fiil yoğunluğu, Mann-Whitney U (Medenî > Mekkî pozitif) · **Ölçüt:** z = 0.517 · **p:** 0.6053 · **q:** 0.6053 · **Etki:** 0.978

Toplam 91 | Mekkî 4.7‰ | Medenî 4.6‰

### ⚪ Fiil babı VII (infi'âl): Medenî/Mekkî oranı 0.97x
**Yöntem:** Sure bazında ‰ fiil yoğunluğu, Mann-Whitney U (Medenî > Mekkî pozitif) · **Ölçüt:** z = 0.711 · **p:** 0.4771 · **q:** 0.6053 · **Etki:** 0.973

Toplam 51 | Mekkî 2.7‰ | Medenî 2.6‰

### ⚪ Fiil babı VIII (ifti'âl): Medenî/Mekkî oranı 1.17x
**Yöntem:** Sure bazında ‰ fiil yoğunluğu, Mann-Whitney U (Medenî > Mekkî pozitif) · **Ölçüt:** z = 1.481 · **p:** 0.1386 · **q:** 0.2079 · **Etki:** 1.170

Toplam 963 | Mekkî 46.8‰ | Medenî 54.7‰

### ⚪ Fiil babı X (istif'âl): Medenî/Mekkî oranı 0.85x
**Yöntem:** Sure bazında ‰ fiil yoğunluğu, Mann-Whitney U (Medenî > Mekkî pozitif) · **Ölçüt:** z = 0.592 · **p:** 0.5535 · **q:** 0.6053 · **Etki:** 0.850

Toplam 369 | Mekkî 20.2‰ | Medenî 17.2‰


## 14. Tekrar ve Formül Yapıları

_Çalışma süresi: 1.66 s_

### 📋 Rahmân suresinde nakarat: 'فباي ءالاء ربكما تكذبان' ×31
**Yöntem:** Aynı sure içinde harekesiz metni birebir tekrar eden ayetler (>= 3 kelime, >= 3 tekrar) · **Ölçüt:** tekrar = 31

Konumlar arası aralıklar: [3, 2, 3, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]

<details><summary>Kanıt (31)</summary>

- 55:13
- 55:16
- 55:18
- 55:21
- 55:23
- 55:25
- 55:28
- 55:30
- 55:32
- 55:34
- 55:36
- 55:38
- 55:40
- 55:42
- 55:45

</details>

### 📋 Mürselât suresinde nakarat: 'ويل يومئذ للمكذبين' ×10
**Yöntem:** Aynı sure içinde harekesiz metni birebir tekrar eden ayetler (>= 3 kelime, >= 3 tekrar) · **Ölçüt:** tekrar = 10

Konumlar arası aralıklar: [4, 5, 4, 6, 3, 3, 5, 2, 2]

<details><summary>Kanıt (10)</summary>

- 77:15
- 77:19
- 77:24
- 77:28
- 77:34
- 77:37
- 77:40
- 77:45
- 77:47
- 77:49

</details>

### 📋 Şuarâ suresinde nakarat: 'وان ربك لهو العزيز الرحيم' ×8
**Yöntem:** Aynı sure içinde harekesiz metni birebir tekrar eden ayetler (>= 3 kelime, >= 3 tekrar) · **Ölçüt:** tekrar = 8

Konumlar arası aralıklar: [59, 36, 18, 18, 19, 16, 16]

<details><summary>Kanıt (8)</summary>

- 26:9
- 26:68
- 26:104
- 26:122
- 26:140
- 26:159
- 26:175
- 26:191

</details>

### 📋 Şuarâ suresinde nakarat: 'فاتقوا الله واطيعون' ×8
**Yöntem:** Aynı sure içinde harekesiz metni birebir tekrar eden ayetler (>= 3 kelime, >= 3 tekrar) · **Ölçüt:** tekrar = 8

Konumlar arası aralıklar: [2, 16, 5, 13, 6, 13, 16]

<details><summary>Kanıt (8)</summary>

- 26:108
- 26:110
- 26:126
- 26:131
- 26:144
- 26:150
- 26:163
- 26:179

</details>

### 📋 Şuarâ suresinde nakarat: 'ان في ذلك لءايه وما كان اكثرهم مؤمنين' ×6
**Yöntem:** Aynı sure içinde harekesiz metni birebir tekrar eden ayetler (>= 3 kelime, >= 3 tekrar) · **Ölçüt:** tekrar = 6

Konumlar arası aralıklar: [59, 36, 18, 53, 16]

<details><summary>Kanıt (6)</summary>

- 26:8
- 26:67
- 26:103
- 26:121
- 26:174
- 26:190

</details>

### 📋 Şuarâ suresinde nakarat: 'اني لكم رسول امين' ×5
**Yöntem:** Aynı sure içinde harekesiz metni birebir tekrar eden ayetler (>= 3 kelime, >= 3 tekrar) · **Ölçüt:** tekrar = 5

Konumlar arası aralıklar: [18, 18, 19, 16]

<details><summary>Kanıt (5)</summary>

- 26:107
- 26:125
- 26:143
- 26:162
- 26:178

</details>

### 📋 Şuarâ suresinde nakarat: 'وما اسلكم عليه من اجر ان اجري الا علي رب العلمين' ×5
**Yöntem:** Aynı sure içinde harekesiz metni birebir tekrar eden ayetler (>= 3 kelime, >= 3 tekrar) · **Ölçüt:** tekrar = 5

Konumlar arası aralıklar: [18, 18, 19, 16]

<details><summary>Kanıt (5)</summary>

- 26:109
- 26:127
- 26:145
- 26:164
- 26:180

</details>

### 📋 Sâffât suresinde nakarat: 'الا عباد الله المخلصين' ×4
**Yöntem:** Aynı sure içinde harekesiz metni birebir tekrar eden ayetler (>= 3 kelime, >= 3 tekrar) · **Ölçüt:** tekrar = 4

Konumlar arası aralıklar: [34, 54, 32]

<details><summary>Kanıt (4)</summary>

- 37:40
- 37:74
- 37:128
- 37:160

</details>

### 📋 Kamer suresinde nakarat: 'ولقد يسرنا القرءان للذكر فهل من مدكر' ×4
**Yöntem:** Aynı sure içinde harekesiz metni birebir tekrar eden ayetler (>= 3 kelime, >= 3 tekrar) · **Ölçüt:** tekrar = 4

Konumlar arası aralıklar: [5, 10, 8]

<details><summary>Kanıt (4)</summary>

- 54:17
- 54:22
- 54:32
- 54:40

</details>

### 📋 Sâffât suresinde nakarat: 'وتركنا عليه في الءاخرين' ×3
**Yöntem:** Aynı sure içinde harekesiz metni birebir tekrar eden ayetler (>= 3 kelime, >= 3 tekrar) · **Ölçüt:** tekrar = 3

Konumlar arası aralıklar: [30, 21]

<details><summary>Kanıt (3)</summary>

- 37:78
- 37:108
- 37:129

</details>

### 📋 Sâffât suresinde nakarat: 'انا كذلك نجزي المحسنين' ×3
**Yöntem:** Aynı sure içinde harekesiz metni birebir tekrar eden ayetler (>= 3 kelime, >= 3 tekrar) · **Ölçüt:** tekrar = 3

Konumlar arası aralıklar: [41, 10]

<details><summary>Kanıt (3)</summary>

- 37:80
- 37:121
- 37:131

</details>

### 📋 Sâffât suresinde nakarat: 'انه من عبادنا المؤمنين' ×3
**Yöntem:** Aynı sure içinde harekesiz metni birebir tekrar eden ayetler (>= 3 kelime, >= 3 tekrar) · **Ölçüt:** tekrar = 3

Konumlar arası aralıklar: [30, 21]

<details><summary>Kanıt (3)</summary>

- 37:81
- 37:111
- 37:132

</details>

### 📋 13 nakarat örüntüsü 5 surede bulundu
**Yöntem:** Nakarat taraması özeti · **Ölçüt:** nakarat sayısı = 13

<details><summary>Kanıt (13)</summary>

- Rahmân ×31
- Mürselât ×10
- Şuarâ ×8
- Şuarâ ×8
- Şuarâ ×6
- Şuarâ ×5
- Şuarâ ×5
- Sâffât ×4
- Kamer ×4
- Sâffât ×3
- Sâffât ×3
- Sâffât ×3
- Kamer ×3

</details>

### ✅ 192 sureler arası benzer ayet çifti, nüzul sırasında birbirine yakın surelerde yoğunlaşıyor (ort. mesafe 21.0 vs rastgele 27.2)
**Yöntem:** Jaccard(içerik lemma) >= 0.7 çiftler; sure etiketleri ayetler arasında karıştırılır (1000 permütasyon) · **Ölçüt:** ort. nüzul sırası mesafesi = 21.036 · **p:** 0.0010 · **q:** 0.0025 · **Etki:** 0.773

Toplam benzer çift 777 (sure içi 585). En çok paylaşan sure çiftleri: Tûr-Mürselât (11), Mürselât-Mutaffifîn (10), A'râf-Şuarâ (7), Bakara-A'râf (6), Bakara-Âl-i İmrân (3), Âl-i İmrân-Enfâl (3), A'râf-Ankebût (3), Hicr-Sâd (3)

<details><summary>Kanıt (20)</summary>

- 1:2 ~ 37:182 (J=1.00)
- 2:5 ~ 31:5 (J=1.00)
- 2:95 ~ 62:7 (J=1.00)
- 2:136 ~ 3:84 (J=1.00)
- 2:147 ~ 3:60 (J=1.00)
- 2:162 ~ 3:88 (J=1.00)
- 3:51 ~ 19:36 (J=1.00)
- 3:51 ~ 43:64 (J=1.00)
- 3:89 ~ 24:5 (J=1.00)
- 3:126 ~ 8:10 (J=1.00)
- 3:182 ~ 8:51 (J=1.00)
- 3:182 ~ 22:10 (J=1.00)
- 6:4 ~ 36:46 (J=1.00)
- 6:10 ~ 21:41 (J=1.00)
- 6:15 ~ 39:13 (J=1.00)

</details>

### 📋 Formül: 'أَيّ الَّذِي آمَنَ' — 89 kez, 20 surede
**Yöntem:** Maksimal içerik-lemma n-gramı (3-6), >= 3 geçiş, >= 2 sure · **Ölçüt:** geçiş = 89

<details><summary>Kanıt (25)</summary>

- 2:104
- 2:153
- 2:172
- 2:178
- 2:183
- 2:208
- 2:254
- 2:264
- 2:267
- 2:278
- 2:282
- 3:100
- 3:102
- 3:118
- 3:130

</details>

### 📋 Formül: 'ما كانَ عَمِلَ' — 56 kez, 32 surede
**Yöntem:** Maksimal içerik-lemma n-gramı (3-6), >= 3 geçiş, >= 2 sure · **Ölçüt:** geçiş = 56

<details><summary>Kanıt (25)</summary>

- 2:134
- 2:141
- 5:62
- 5:105
- 6:43
- 6:60
- 6:88
- 6:108
- 6:122
- 6:127
- 7:43
- 7:118
- 7:139
- 7:147
- 7:180

</details>

### 📋 Formül: 'الَّذِي آمَنَ عَمِلَ صالِحَة' — 51 kez, 33 surede
**Yöntem:** Maksimal içerik-lemma n-gramı (3-6), >= 3 geçiş, >= 2 sure · **Ölçüt:** geçiş = 51

<details><summary>Kanıt (25)</summary>

- 2:25
- 2:82
- 2:277
- 3:57
- 4:57
- 4:122
- 4:173
- 5:9
- 5:93
- 7:42
- 10:4
- 10:9
- 11:23
- 13:29
- 14:23

</details>

### 📋 Formül: 'اللَّه غَفُور رَحِيم' — 47 kez, 19 surede
**Yöntem:** Maksimal içerik-lemma n-gramı (3-6), >= 3 geçiş, >= 2 sure · **Ölçüt:** geçiş = 47

<details><summary>Kanıt (25)</summary>

- 2:173
- 2:182
- 2:192
- 2:199
- 2:218
- 2:226
- 3:31
- 3:89
- 3:129
- 4:25
- 4:96
- 4:100
- 4:110
- 4:152
- 5:3

</details>

### 📋 Formül: 'اللَّه كُلّ شَىْء' — 46 kez, 22 surede
**Yöntem:** Maksimal içerik-lemma n-gramı (3-6), >= 3 geçiş, >= 2 sure · **Ölçüt:** geçiş = 46

<details><summary>Kanıt (25)</summary>

- 2:20
- 2:106
- 2:109
- 2:148
- 2:231
- 2:259
- 2:282
- 2:284
- 3:29
- 3:165
- 3:189
- 4:85
- 4:126
- 4:176
- 5:17

</details>

### 📋 Formül: 'جَرَيْ تَحْت نَهَر' — 38 kez, 26 surede
**Yöntem:** Maksimal içerik-lemma n-gramı (3-6), >= 3 geçiş, >= 2 sure · **Ölçüt:** geçiş = 38

<details><summary>Kanıt (25)</summary>

- 2:25
- 2:266
- 3:15
- 3:136
- 3:195
- 3:198
- 4:13
- 4:57
- 4:122
- 5:12
- 5:85
- 5:119
- 7:43
- 9:72
- 9:89

</details>

### 📋 Formül: 'كُلّ شَىْء قَدِير' — 35 kez, 24 surede
**Yöntem:** Maksimal içerik-lemma n-gramı (3-6), >= 3 geçiş, >= 2 sure · **Ölçüt:** geçiş = 35

<details><summary>Kanıt (25)</summary>

- 2:20
- 2:106
- 2:109
- 2:148
- 2:259
- 2:284
- 3:26
- 3:29
- 3:165
- 3:189
- 5:17
- 5:19
- 5:40
- 5:120
- 6:17

</details>

### 📋 Formül: 'أَيّ آلاء رَبّ' — 32 kez, 2 surede
**Yöntem:** Maksimal içerik-lemma n-gramı (3-6), >= 3 geçiş, >= 2 sure · **Ölçüt:** geçiş = 32

<details><summary>Kanıt (25)</summary>

- 53:55
- 55:13
- 55:16
- 55:18
- 55:21
- 55:23
- 55:25
- 55:28
- 55:30
- 55:32
- 55:34
- 55:36
- 55:38
- 55:40
- 55:42

</details>

### 📋 Formül: 'خَلَقَ سَماء أَرْض' — 29 kez, 25 surede
**Yöntem:** Maksimal içerik-lemma n-gramı (3-6), >= 3 geçiş, >= 2 sure · **Ölçüt:** geçiş = 29

<details><summary>Kanıt (25)</summary>

- 6:1
- 6:73
- 7:54
- 9:36
- 10:3
- 11:7
- 14:19
- 14:32
- 15:85
- 16:3
- 17:99
- 21:16
- 25:59
- 27:60
- 29:61

</details>

### 📋 Formül: 'جَنَّة جَرَيْ تَحْت نَهَر' — 28 kez, 17 surede
**Yöntem:** Maksimal içerik-lemma n-gramı (3-6), >= 3 geçiş, >= 2 sure · **Ölçüt:** geçiş = 28

<details><summary>Kanıt (25)</summary>

- 2:25
- 3:15
- 3:136
- 3:195
- 3:198
- 4:13
- 4:57
- 4:122
- 5:12
- 5:85
- 5:119
- 9:72
- 9:89
- 9:100
- 14:23

</details>

### ⚪ Uzunluk kontrolünde (yalnızca uzun ayetler) formül yoğunluğu–nüzul ilişkisi: rho=+0.13 — eğilim büyük ölçüde ayet uzunluğundan kaynaklanıyor
**Yöntem:** Yalnızca >= 8 içerik lemmalı ayetler, >= 30 token olan sureler; Spearman, 2000 permütasyon · **Ölçüt:** Spearman rho = 0.133 · **p:** 0.2624 · **q:** 0.2624 · **Etki:** 0.133

70 sure

### ✅ Sure formül yoğunluğu nüzul sırasıyla artıyor (rho=+0.52)
**Yöntem:** İçerik tokenlarının başka surelerle paylaşılan 4-gram içinde kalma oranı; Spearman, 2000 permütasyon · **Ölçüt:** Spearman rho = 0.523 · **p:** 0.0005 · **q:** 0.0025 · **Etki:** 0.523

Mekkî ort. %14.9 | Medenî ort. %28.0 | toplam maksimal formül: 1450

<details><summary>Kanıt (10)</summary>

- Beyyine %64
- Tegâbün %58
- Cuma %57
- Saf %55
- Lokmân %50
- Câsiye %46
- Rûm %44
- Ankebût %40
- Mücâdele %39
- Hadîd %38

</details>

### ✅ Ayet sonu ilahî isim çiftleri ayetin içeriğiyle uyumlu: karşılıklı bilgi rastlantının 1.28 katı
**Yöntem:** 9 sık sonlanma çifti (>= 8), 229 ayet; sonlar ayetler arasında karıştırılır (300 permütasyon) · **Ölçüt:** karşılıklı bilgi (bit) = 3.239 · **p:** 0.0033 · **q:** 0.0042 · **Etki:** 1.284

Gözlenen MI 3.2385 | null ort. 2.5218

<details><summary>Kanıt (12)</summary>

- غَفُور رَحِيم ×70
- عَزِيز حَكِيم ×47
- سَمِيع عَلِيم ×32
- عَلِيم حَكِيم ×28
- عَزِيز رَحِيم ×13
- سَمِيع بَصِير ×11
- غَنِيّ حَمِيد ×10
- تَوّاب رَحِيم ×9
- رَءُوف رَحِيم ×9
- حَكِيم عَلِيم ×7
- قَوِيّ عَزِيز ×7
- عَزِيز عَلِيم ×6

</details>

### ✅ Sure içi karıştırmada da fâsıla-içerik uyumu korunuyor (MI rastlantının 1.13 katı)
**Yöntem:** Aynı sonlanma-kök MI istatistiği; sonlar yalnızca aynı sure içinde karıştırılır (300 permütasyon) · **Ölçüt:** karşılıklı bilgi (bit) = 3.239 · **p:** 0.0033 · **q:** 0.0042 · **Etki:** 1.133

Sure içi null ort. 2.8594. Bu test, uyumun sure konusundan değil ayet düzeyinden geldiğini sınar.

### ✅ 'غَفُور رَحِيم' ile biten ayetlerde kök غفر 2.7 kat sık
**Yöntem:** Sonlanma çifti × gövde kökü, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 2.677 · **p:** 0.0000 · **q:** 3.5e-05 · **Etki:** 2.677

18/70 ayet

<details><summary>Kanıt (10)</summary>

- 2:199
- 3:31
- 3:129
- 4:96
- 4:106
- 4:110
- 5:74
- 8:70
- 12:98
- 24:22

</details>

### ✅ 'تَوّاب رَحِيم' ile biten ayetlerde kök توب 6.6 kat sık
**Yöntem:** Sonlanma çifti × gövde kökü, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 6.597 · **p:** 5.0e-06 · **q:** 0.0003 · **Etki:** 6.597

7/9 ayet

<details><summary>Kanıt (7)</summary>

- 2:37
- 2:54
- 2:128
- 2:160
- 4:16
- 9:104
- 9:118

</details>

### ✅ 'عَزِيز رَحِيم' ile biten ayetlerde kök ربب (Rab, efendi) 3.4 kat sık
**Yöntem:** Sonlanma çifti × gövde kökü, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 3.437 · **p:** 0.0004 · **q:** 0.0129 · **Etki:** 3.437

8/13 ayet

<details><summary>Kanıt (8)</summary>

- 26:9
- 26:68
- 26:104
- 26:122
- 26:140
- 26:159
- 26:175
- 26:191

</details>

### ✅ 'عَلِيم حَكِيم' ile biten ayetlerde kök قبل (önce) 4.1 kat sık
**Yöntem:** Sonlanma çifti × gövde kökü, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 4.089 · **p:** 0.0004 · **q:** 0.0129 · **Etki:** 4.089

7/28 ayet

<details><summary>Kanıt (7)</summary>

- 4:26
- 8:71
- 12:6
- 12:100
- 22:52
- 24:58
- 24:59

</details>

### ✅ 'عَلِيم حَكِيم' ile biten ayetlerde kök فرض 6.5 kat sık
**Yöntem:** Sonlanma çifti × gövde kökü, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 6.543 · **p:** 0.0008 · **q:** 0.0235 · **Etki:** 6.543

4/28 ayet

<details><summary>Kanıt (4)</summary>

- 4:11
- 4:24
- 9:60
- 66:2

</details>

### ✅ 'غَنِيّ حَمِيد' ile biten ayetlerde kök كفر (inkâr etmek, küfretmek) 7.0 kat sık
**Yöntem:** Sonlanma çifti × gövde kökü, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 7.046 · **p:** 0.0011 · **q:** 0.0258 · **Etki:** 7.046

4/10 ayet

<details><summary>Kanıt (4)</summary>

- 4:131
- 14:8
- 31:12
- 64:6

</details>

### ✅ 'غَنِيّ حَمِيد' ile biten ayetlerde kök ولي 9.8 kat sık
**Yöntem:** Sonlanma çifti × gövde kökü, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 9.814 · **p:** 0.0019 · **q:** 0.0387 · **Etki:** 9.814

3/10 ayet

<details><summary>Kanıt (3)</summary>

- 57:24
- 60:6
- 64:6

</details>

### ✅ 'عَلِيم حَكِيم' ile biten ayetlerde kök أيي (ayet, işaret) 2.6 kat sık
**Yöntem:** Sonlanma çifti × gövde kökü, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 2.629 · **p:** 0.0024 · **q:** 0.0421 · **Etki:** 2.629

9/28 ayet

<details><summary>Kanıt (9)</summary>

- 4:11
- 4:170
- 9:28
- 22:52
- 24:18
- 24:58
- 24:59
- 33:1
- 60:10

</details>

### ✅ 'غَنِيّ حَمِيد' ile biten ayetlerde kök أرض (yeryüzü, toprak) 4.1 kat sık
**Yöntem:** Sonlanma çifti × gövde kökü, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 4.089 · **p:** 0.0032 · **q:** 0.0440 · **Etki:** 4.089

5/10 ayet

<details><summary>Kanıt (5)</summary>

- 2:267
- 4:131
- 14:8
- 22:64
- 31:26

</details>

### ✅ 'غَفُور رَحِيم' ile biten ayetlerde kök سوأ 2.3 kat sık
**Yöntem:** Sonlanma çifti × gövde kökü, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 2.265 · **p:** 0.0036 · **q:** 0.0440 · **Etki:** 2.265

9/70 ayet

<details><summary>Kanıt (9)</summary>

- 4:110
- 6:54
- 7:153
- 7:167
- 9:102
- 12:53
- 16:119
- 25:70
- 27:11

</details>

### ✅ 'غَفُور رَحِيم' ile biten ayetlerde kök عمل (yapmak, işlemek) 2.5 kat sık
**Yöntem:** Sonlanma çifti × gövde kökü, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 2.544 · **p:** 0.0041 · **q:** 0.0440 · **Etki:** 2.544

7/70 ayet

<details><summary>Kanıt (7)</summary>

- 4:110
- 6:54
- 7:153
- 9:102
- 16:119
- 25:70
- 49:14

</details>

### ✅ 'غَفُور رَحِيم' ile biten ayetlerde kök حرم 2.5 kat sık
**Yöntem:** Sonlanma çifti × gövde kökü, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 2.544 · **p:** 0.0041 · **q:** 0.0440 · **Etki:** 2.544

7/70 ayet

<details><summary>Kanıt (7)</summary>

- 2:173
- 4:23
- 5:3
- 6:145
- 9:5
- 16:115
- 66:1

</details>

### ✅ 'غَفُور رَحِيم' ile biten ayetlerde kök وجد 2.5 kat sık
**Yöntem:** Sonlanma çifti × gövde kökü, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 2.544 · **p:** 0.0041 · **q:** 0.0440 · **Etki:** 2.544

7/70 ayet

<details><summary>Kanıt (7)</summary>

- 4:100
- 4:110
- 6:145
- 9:5
- 9:91
- 24:33
- 58:12

</details>

### 📋 140 sonlanma-kök eşleşmesinin 13 tanesi anlamlı (q<0.05)
**Yöntem:** Fâsıla-anlam taraması özeti · **Ölçüt:** anlamlı eşleşme = 13


## 15. Kavram Ağı ve Anlam Alanları

_Çalışma süresi: 1.86 s_

### 📋🤖 Kök eşbulunma ağı: 592 kök, 2069 PPMI bağı; etiket yayılımı 41 kavram kümesi (>= 5 kök) buldu
**Yöntem:** Ayet düzeyi eşbulunma (>= 3), PPMI ağırlıklı graf, deterministik etiket yayılımı · **Ölçüt:** küme sayısı = 41

Küme adı: kümedeki köklerin iki modelce uzlaşılmış anlam alanlarının çoğunluğu (LLM yalnızca etiket verir).

<details><summary>Kanıt (15)</summary>

- [?] جنن, نور, عظم, دخل, نهر … (26 kök)
- [Peygamberlik/Vahiy (%100)] كتب (kitap, yazı), نزل (indirmek), خرج, أمم, أكل … (25 kök)
- [Zaman (%100)] أخر (son, sonraki), خير, حيي, دنو, رود … (23 kök)
- [Peygamberlik/Vahiy (%50)] رسل (elçi, peygamber), حقق (hak, gerçek), جيأ (gelmek), غير, قتل … (22 kök)
- [Diğer/Dilbilgisel (%67)] أله (Allah, ilah), شيأ (şey), كلل (hepsi, tüm), عبد (kul, köle), قدر … (21 kök)
- [Doğa/Kozmos (%67)] أرض (yeryüzü, toprak), سمو (gök), خلق (yaratmak), ملك, بلغ … (18 kök)
- [Diğer/Dilbilgisel (%100)] كون (olmak, var olmak), نظر, شدد, كيف, عقب … (17 kök)
- [Bilgi/Akıl (%100)] جعل (yapmak, kılmak), رأي (görmek), ليل, سخر, شمس … (15 kök)
- [Konuşma/İletişim (%100)] قول (söylemek, demek), أبو, أخو, وفي, حفظ … (15 kök)
- [Hukuk/Toplum (%50)] قوم (kavim, topluluk), هدي (hidayet etmek, yol göstermek), ضلل, سبل, سوي … (13 kök)
- [Zaman (%100)] رحم (merhametli, esirgeyen), بعد (sonra), غفر, توب, ردد … (13 kök)
- [?] قلب, سلم, وجد, ليس, عدد … (13 kök)
- [İnanç/Tanrı (%33)] ربب (Rab, efendi), أيي (ayet, işaret), كذب (yalanlamak), تلو, فري … (12 kök)
- [?] عند, حسن, سأل, أجر, ضعف … (12 kök)
- [İnanç/Tanrı (%50)] كفر (inkâr etmek, küfretmek), عذب (azap, ceza), ألم, ذوق, هون … (12 kök)

</details>

### ⚪🤖 Metnin kendi eşbulunma yapısı anlam alanlarını geri üretiyor: NMI=0.758 (rastgele 0.737)
**Yöntem:** Deterministik kümeler vs uzlaşılmış LLM anlam alanları; NMI, alan etiketleri karıştırılır (1000 perm.) · **Ölçüt:** NMI = 0.758 · **p:** 0.1938 · **q:** 0.1938 · **Etki:** 1.029

29 kök. Uzlaşılmış alan etiketi oranı: 31/40.

### ✅🤖 Anlam alanı 'Ekonomi/Mal' nüzul sırasıyla artıyor (rho=+0.35)
**Yöntem:** Sure içi alan token payı ~ nüzul sırası; Spearman, 2000 permütasyon, BH-FDR · **Ölçüt:** Spearman rho = 0.351 · **p:** 0.0005 · **q:** 0.0032 · **Etki:** 0.351

Mekkî ort. %3.1 | Medenî ort. %3.4

### ✅🤖 Anlam alanı 'Peygamberlik/Vahiy' nüzul sırasıyla artıyor (rho=+0.41)
**Yöntem:** Sure içi alan token payı ~ nüzul sırası; Spearman, 2000 permütasyon, BH-FDR · **Ölçüt:** Spearman rho = 0.409 · **p:** 0.0005 · **q:** 0.0032 · **Etki:** 0.409

Mekkî ort. %6.0 | Medenî ort. %9.1

### ✅🤖 Anlam alanı 'Ahiret' nüzul sırasıyla artıyor (rho=+0.32)
**Yöntem:** Sure içi alan token payı ~ nüzul sırası; Spearman, 2000 permütasyon, BH-FDR · **Ölçüt:** Spearman rho = 0.315 · **p:** 0.0015 · **q:** 0.0065 · **Etki:** 0.315

Mekkî ort. %2.1 | Medenî ort. %1.6

### ✅🤖 Anlam alanı 'Hareket/Mekân' nüzul sırasıyla artıyor (rho=+0.27)
**Yöntem:** Sure içi alan token payı ~ nüzul sırası; Spearman, 2000 permütasyon, BH-FDR · **Ölçüt:** Spearman rho = 0.272 · **p:** 0.0040 · **q:** 0.0117 · **Etki:** 0.272

Mekkî ort. %1.2 | Medenî ort. %1.5

### ✅🤖 Anlam alanı 'Hukuk/Toplum' nüzul sırasıyla artıyor (rho=+0.27)
**Yöntem:** Sure içi alan token payı ~ nüzul sırası; Spearman, 2000 permütasyon, BH-FDR · **Ölçüt:** Spearman rho = 0.268 · **p:** 0.0045 · **q:** 0.0117 · **Etki:** 0.268

Mekkî ort. %4.1 | Medenî ort. %4.2

### ✅🤖 Anlam alanı 'Erdem/İyilik' nüzul sırasıyla artıyor (rho=+0.26)
**Yöntem:** Sure içi alan token payı ~ nüzul sırası; Spearman, 2000 permütasyon, BH-FDR · **Ölçüt:** Spearman rho = 0.259 · **p:** 0.0080 · **q:** 0.0173 · **Etki:** 0.259

Mekkî ort. %1.1 | Medenî ort. %1.6

### ⚪🤖 Anlam alanı 'Doğa/Kozmos' nüzul sırasıyla artıyor (rho=+0.20)
**Yöntem:** Sure içi alan token payı ~ nüzul sırası; Spearman, 2000 permütasyon, BH-FDR · **Ölçüt:** Spearman rho = 0.201 · **p:** 0.0310 · **q:** 0.0575 · **Etki:** 0.201

Mekkî ort. %5.4 | Medenî ort. %4.4

### ⚪🤖 Anlam alanı 'İnanç/Tanrı' nüzul sırasıyla artıyor (rho=+0.19)
**Yöntem:** Sure içi alan token payı ~ nüzul sırası; Spearman, 2000 permütasyon, BH-FDR · **Ölçüt:** Spearman rho = 0.188 · **p:** 0.0445 · **q:** 0.0723 · **Etki:** 0.188

Mekkî ort. %28.6 | Medenî ort. %39.5

### ⚪🤖 Anlam alanı 'Bilgi/Akıl' nüzul sırasıyla artıyor (rho=+0.18)
**Yöntem:** Sure içi alan token payı ~ nüzul sırası; Spearman, 2000 permütasyon, BH-FDR · **Ölçüt:** Spearman rho = 0.178 · **p:** 0.0620 · **q:** 0.0895 · **Etki:** 0.178

Mekkî ort. %8.1 | Medenî ort. %7.2

### ⚪🤖 Anlam alanı 'Diğer/Dilbilgisel' nüzul sırasıyla artıyor (rho=+0.15)
**Yöntem:** Sure içi alan token payı ~ nüzul sırası; Spearman, 2000 permütasyon, BH-FDR · **Ölçüt:** Spearman rho = 0.154 · **p:** 0.1049 · **q:** 0.1364 · **Etki:** 0.154

Mekkî ort. %13.6 | Medenî ort. %13.1

### ⚪🤖 Anlam alanı 'Konuşma/İletişim' nüzul sırasıyla azalıyor (rho=-0.10)
**Yöntem:** Sure içi alan token payı ~ nüzul sırası; Spearman, 2000 permütasyon, BH-FDR · **Ölçüt:** Spearman rho = -0.095 · **p:** 0.3353 · **q:** 0.3963 · **Etki:** -0.095

Mekkî ort. %11.6 | Medenî ort. %6.6

### ⚪🤖 Anlam alanı 'Zaman' nüzul sırasıyla azalıyor (rho=-0.05)
**Yöntem:** Sure içi alan token payı ~ nüzul sırası; Spearman, 2000 permütasyon, BH-FDR · **Ölçüt:** Spearman rho = -0.049 · **p:** 0.6007 · **q:** 0.6508 · **Etki:** -0.049

Mekkî ort. %9.2 | Medenî ort. %5.8

### ⚪🤖 Anlam alanı 'Yaratılış/Hayat-Ölüm' nüzul sırasıyla azalıyor (rho=-0.01)
**Yöntem:** Sure içi alan token payı ~ nüzul sırası; Spearman, 2000 permütasyon, BH-FDR · **Ölçüt:** Spearman rho = -0.011 · **p:** 0.8921 · **q:** 0.8921 · **Etki:** -0.011

Mekkî ort. %4.6 | Medenî ort. %2.0

### 📋 Kavram kümeleri arasında köprü kuran kökler: أله (Allah, ilah), كون (olmak, var olmak), قول (söylemek, demek), ربب (Rab, efendi), قوم (kavim, topluluk)
**Yöntem:** Bir kökün PPMI komşularının ait olduğu farklı küme sayısı · **Ölçüt:** küme sayısı = 21

<details><summary>Kanıt (15)</summary>

- أله (Allah, ilah): 21 küme
- كون (olmak, var olmak): 19 küme
- قول (söylemek, demek): 18 küme
- ربب (Rab, efendi): 17 küme
- قوم (kavim, topluluk): 16 küme
- جعل (yapmak, kılmak): 15 küme
- أمن (iman etmek, güvenmek): 13 küme
- كفر (inkâr etmek, küfretmek): 12 küme
- نفس (nefis, can, kendilik): 11 küme
- كلل (hepsi, tüm): 11 küme
- كتب (kitap, yazı): 10 küme
- رسل (elçi, peygamber): 10 küme
- أيي (ayet, işaret): 10 küme
- أرض (yeryüzü, toprak): 10 küme
- يدي: 9 küme

</details>


## 16. Zıt Anlam (Tıbâk) Sayımı

_Çalışma süresi: 0.19 s_

### 📋🤖 İki model 40 kökü etiketledi: zıt-kök varlığında Cohen κ=0.88, anlam alanında κ=0.75; 20 çiftte birebir uzlaşı
**Yöntem:** Modeller: deepseek-v4.1-flash, qwen3.7-plus; aynı istem, sıcaklık 0 · **Ölçüt:** kappa = 0.881

Model A çift: 24 | Model B çift: 25 | testlere giren (her iki kök frekansı >= 5): 19

<details><summary>Kanıt (20)</summary>

- أتي (vermek) ↔ منع
- أخر (son, sonraki) ↔ أول
- أرض (yeryüzü, toprak) ↔ سمو (gök)
- أمر (emir, buyruk) ↔ نهي
- أمن (iman etmek, güvenmek) ↔ كفر (inkâr etmek, küfretmek)
- بطل ↔ حقق (hak, gerçek)
- بعد (sonra) ↔ قبل (önce)
- بعض ↔ كلل (hepsi, tüm)
- جهل ↔ علم (bilmek)
- جيأ (gelmek) ↔ ذهب
- ذكر (anmak, hatırlamak) ↔ نسي
- رأي (görmek) ↔ عمي
- ربب (Rab, efendi) ↔ عبد (kul, köle)
- رحم (merhametli, esirgeyen) ↔ عذب (azap, ceza)
- سكت ↔ قول (söylemek, demek)

</details>

### ✅🤖 Zıt kavramlar aynı ayette rastlantıdan 2.8 kat (geometrik ort.) sık birlikte geçiyor (tıbâk)
**Yöntem:** 19 uzlaşılmış zıt çift; ort. log2(lift); null: partnerler yeniden eşlenir (10000 perm.) · **Ölçüt:** ort. log2 lift = 1.464 · **p:** 0.0001 · **q:** 0.0002 · **Etki:** 2.759

<details><summary>Kanıt (19)</summary>

- بطل ↔ حقق (hak, gerçek): 15 ayet (lift 10.8)
- أرض (yeryüzü, toprak) ↔ سمو (gök): 224 ayet (lift 9.0)
- ذكر (anmak, hatırlamak) ↔ نسي: 12 ayet (lift 8.0)
- ضلل ↔ هدي (hidayet etmek, yol göstermek): 52 ayet (lift 7.2)
- أمر (emir, buyruk) ↔ نهي: 12 ayet (lift 6.4)
- فجر ↔ وقي (sakınmak, takva): 3 ayet (lift 4.4)
- أخر (son, sonraki) ↔ أول: 16 ayet (lift 3.6)
- أتي (vermek) ↔ منع: 4 ayet (lift 3.4)
- جهل ↔ علم (bilmek): 7 ayet (lift 2.7)
- أمن (iman etmek, güvenmek) ↔ كفر (inkâr etmek, küfretmek): 126 ayet (lift 2.3)
- بعد (sonra) ↔ قبل (önce): 17 ayet (lift 1.7)
- بعض ↔ كلل (hepsi, tüm): 8 ayet (lift 1.7)
- صدق ↔ كذب (yalanlamak): 9 ayet (lift 1.6)
- رحم (merhametli, esirgeyen) ↔ عذب (azap, ceza): 25 ayet (lift 1.5)
- جيأ (gelmek) ↔ ذهب: 3 ayet (lift 1.5)

</details>

### ✅🤖 Tıbâk etkisi frekansı eşleştirilmiş rastgele kök çiftlerine karşı da korunuyor
**Yöntem:** Her kök aynı log-frekans kutusundan rastgele bir kökle değiştirilir (2000 tekrar) · **Ölçüt:** ort. log2 lift = 1.464 · **p:** 0.0005 · **q:** 0.0007 · **Etki:** 2.759

### ⚪🤖 Sistematik simetri testi: zıt çiftler frekans bakımından rastgele eşleşmelerden daha dengeli DEĞİL (ort. |log2 oran| 2.11 vs null)
**Yöntem:** Tüm uzlaşılmış çiftler (seçim yok); |log2(fa/fb)|; null: partnerler yeniden eşlenir (10000 perm.) · **Ölçüt:** ort. |log2 oran| = 2.109 · **p:** 0.9450 · **q:** 0.9450

Tam eşit frekanslı zıt çift: 0 (yeniden eşleme beklentisi 0.00, p=1.0000). Bu, projenin önceki tekil 'eşit sayı' iddialarının sistematik ve seçimsiz karşılığıdır.

<details><summary>Kanıt (19)</summary>

- رحم (merhametli, esirgeyen) 339 ↔ عذب (azap, ceza) 373
- أرض (yeryüzü, toprak) 461 ↔ سمو (gök) 381
- بعد (sonra) 235 ↔ قبل (önce) 294
- ضلل 191 ↔ هدي (hidayet etmek, yol göstermek) 316
- أمن (iman etmek, güvenmek) 879 ↔ كفر (inkâr etmek, küfretmek) 525
- صدق 155 ↔ كذب (yalanlamak) 282
- أخر (son, sonraki) 250 ↔ أول 125
- بعض 158 ↔ كلل (hepsi, tüm) 377
- ربب (Rab, efendi) 980 ↔ عبد (kul, köle) 275
- أمر (emir, buyruk) 248 ↔ نهي 56
- جيأ (gelmek) 278 ↔ ذهب 56
- ليل 92 ↔ يوم (gün) 475
- ذكر (anmak, hatırlamak) 292 ↔ نسي 45
- بطل 36 ↔ حقق (hak, gerçek) 287
- رأي (görmek) 328 ↔ عمي 33

</details>

### ✅🤖 Ayet başına tıbâk yoğunluğu: Mekkî 0.058, Medenî 0.149
**Yöntem:** Sure başına (zıt çift eşbulunması / ayet sayısı), Mann-Whitney U · **Ölçüt:** z (Medenî>Mekkî) = 4.048 · **p:** 5.2e-05 · **q:** 0.0002

<details><summary>Kanıt (10)</summary>

- Mümtehine 0.46
- Fetih 0.38
- Hadîd 0.38
- Tegâbün 0.28
- Kureyş 0.25
- Sebe' 0.24
- Câsiye 0.22
- Lokmân 0.21
- Zümer 0.20
- Mü'min (Gâfir) 0.20

</details>


## 17. Halka (Ayna) Kompozisyon Taraması

_Çalışma süresi: 1.37 s_

### ⚪ Ayet düzeyinde 90 surenin 1'inde p<0.05 (rastlantı beklentisi 4.5); FDR sonrası 0 sure anlamlı
**Yöntem:** Sure başına rotasyon p-değerleri; p<0.05 sayısı için binom z (H0: %5) · **Ölçüt:** binom z = -1.693 · **p:** 1.0000 · **q:** 1.0000

Negatif sonuç da raporlanır: rastlantı düzeyinde bir oran, sistematik bir halka yapısı iddiasını DESTEKLEMEZ.

<details><summary>Kanıt (10)</summary>

- Hûd (11): ayet düzeyi ayna skoru 0.095 (rotasyon ort. 0.069)
- Haşr (59): ayet düzeyi ayna skoru 0.210 (rotasyon ort. 0.136)
- Ahzâb (33): ayet düzeyi ayna skoru 0.152 (rotasyon ort. 0.135)
- Secde (32): ayet düzeyi ayna skoru 0.090 (rotasyon ort. 0.061)
- Fetih (48): ayet düzeyi ayna skoru 0.181 (rotasyon ort. 0.149)
- Sâffât (37): ayet düzeyi ayna skoru 0.029 (rotasyon ort. 0.020)
- Ahkâf (46): ayet düzeyi ayna skoru 0.131 (rotasyon ort. 0.112)
- Kalem (68): ayet düzeyi ayna skoru 0.035 (rotasyon ort. 0.021)
- Alak (96): ayet düzeyi ayna skoru 0.095 (rotasyon ort. 0.051)
- Tevbe (9): ayet düzeyi ayna skoru 0.148 (rotasyon ort. 0.137)

</details>

### ⚪ Blok düzeyinde 57 surenin 1'inde p<0.05 (rastlantı beklentisi 2.9); FDR sonrası 0 sure anlamlı
**Yöntem:** Sure başına rotasyon p-değerleri; p<0.05 sayısı için binom z (H0: %5) · **Ölçüt:** binom z = -1.124 · **p:** 1.0000 · **q:** 1.0000

Negatif sonuç da raporlanır: rastlantı düzeyinde bir oran, sistematik bir halka yapısı iddiasını DESTEKLEMEZ.

<details><summary>Kanıt (10)</summary>

- Fussilet (41): 8-blok ayna skoru 0.384 (rotasyon ort. 0.322)
- Zuhruf (43): 8-blok ayna skoru 0.331 (rotasyon ort. 0.293)
- Kamer (54): 8-blok ayna skoru 0.257 (rotasyon ort. 0.180)
- Necm (53): 8-blok ayna skoru 0.185 (rotasyon ort. 0.145)
- Tevbe (9): 8-blok ayna skoru 0.724 (rotasyon ort. 0.707)
- Kalem (68): 8-blok ayna skoru 0.136 (rotasyon ort. 0.108)
- Sâffât (37): 8-blok ayna skoru 0.336 (rotasyon ort. 0.301)
- Âl-i İmrân (3): 8-blok ayna skoru 0.745 (rotasyon ort. 0.738)
- Neml (27): 8-blok ayna skoru 0.409 (rotasyon ort. 0.388)
- Zâriyât (51): 8-blok ayna skoru 0.140 (rotasyon ort. 0.129)

</details>

### ⚪ Hûd (11): ayet düzeyi ayna skoru 0.095 (rotasyon ort. 0.069)
**Yöntem:** Ayna çiftleri (i, n+1-i) kosinüs ortalaması; döngüsel kaydırma null modeli (n rotasyon) · **Ölçüt:** ayna skoru = 0.095 · **p:** 0.0081 · **q:** 1.0000 · **Etki:** 1.383

123 ayet | rotasyonlar arası sıra: 1/123

### ⚪ Fussilet (41): 8-blok ayna skoru 0.384 (rotasyon ort. 0.322)
**Yöntem:** 8 eşit ayet bloğu, ayna blok çiftleri kosinüs; döngüsel kaydırma null modeli · **Ölçüt:** blok ayna skoru = 0.384 · **p:** 0.0185 · **q:** 1.0000 · **Etki:** 1.193

Ayna blok çifti benzerlikleri (dış→iç): 0.14, 0.45, 0.37, 0.58

### ⚪ Zuhruf (43): 8-blok ayna skoru 0.331 (rotasyon ort. 0.293)
**Yöntem:** 8 eşit ayet bloğu, ayna blok çiftleri kosinüs; döngüsel kaydırma null modeli · **Ölçüt:** blok ayna skoru = 0.331 · **p:** 0.0787 · **q:** 1.0000 · **Etki:** 1.130

Ayna blok çifti benzerlikleri (dış→iç): 0.38, 0.26, 0.38, 0.30

### ⚪ Haşr (59): ayet düzeyi ayna skoru 0.210 (rotasyon ort. 0.136)
**Yöntem:** Ayna çiftleri (i, n+1-i) kosinüs ortalaması; döngüsel kaydırma null modeli (n rotasyon) · **Ölçüt:** ayna skoru = 0.210 · **p:** 0.0833 · **q:** 1.0000 · **Etki:** 1.548

24 ayet | rotasyonlar arası sıra: 2/24

### ⚪ Kamer (54): 8-blok ayna skoru 0.257 (rotasyon ort. 0.180)
**Yöntem:** 8 eşit ayet bloğu, ayna blok çiftleri kosinüs; döngüsel kaydırma null modeli · **Ölçüt:** blok ayna skoru = 0.257 · **p:** 0.1091 · **q:** 1.0000 · **Etki:** 1.431

Ayna blok çifti benzerlikleri (dış→iç): 0.20, 0.16, 0.47, 0.19

### ⚪ Ahzâb (33): ayet düzeyi ayna skoru 0.152 (rotasyon ort. 0.135)
**Yöntem:** Ayna çiftleri (i, n+1-i) kosinüs ortalaması; döngüsel kaydırma null modeli (n rotasyon) · **Ölçüt:** ayna skoru = 0.152 · **p:** 0.1096 · **q:** 1.0000 · **Etki:** 1.121

73 ayet | rotasyonlar arası sıra: 8/73

### ⚪ Necm (53): 8-blok ayna skoru 0.185 (rotasyon ort. 0.145)
**Yöntem:** 8 eşit ayet bloğu, ayna blok çiftleri kosinüs; döngüsel kaydırma null modeli · **Ölçüt:** blok ayna skoru = 0.185 · **p:** 0.1290 · **q:** 1.0000 · **Etki:** 1.276

Ayna blok çifti benzerlikleri (dış→iç): 0.00, 0.16, 0.22, 0.35

### ⚪ Secde (32): ayet düzeyi ayna skoru 0.090 (rotasyon ort. 0.061)
**Yöntem:** Ayna çiftleri (i, n+1-i) kosinüs ortalaması; döngüsel kaydırma null modeli (n rotasyon) · **Ölçüt:** ayna skoru = 0.090 · **p:** 0.1333 · **q:** 1.0000 · **Etki:** 1.471

30 ayet | rotasyonlar arası sıra: 4/30

### ⚪ Fetih (48): ayet düzeyi ayna skoru 0.181 (rotasyon ort. 0.149)
**Yöntem:** Ayna çiftleri (i, n+1-i) kosinüs ortalaması; döngüsel kaydırma null modeli (n rotasyon) · **Ölçüt:** ayna skoru = 0.181 · **p:** 0.1379 · **q:** 1.0000 · **Etki:** 1.215

29 ayet | rotasyonlar arası sıra: 4/29

### ⚪ Sâffât (37): ayet düzeyi ayna skoru 0.029 (rotasyon ort. 0.020)
**Yöntem:** Ayna çiftleri (i, n+1-i) kosinüs ortalaması; döngüsel kaydırma null modeli (n rotasyon) · **Ölçüt:** ayna skoru = 0.029 · **p:** 0.1429 · **q:** 1.0000 · **Etki:** 1.444

182 ayet | rotasyonlar arası sıra: 26/182

### ⚪ Ahkâf (46): ayet düzeyi ayna skoru 0.131 (rotasyon ort. 0.112)
**Yöntem:** Ayna çiftleri (i, n+1-i) kosinüs ortalaması; döngüsel kaydırma null modeli (n rotasyon) · **Ölçüt:** ayna skoru = 0.131 · **p:** 0.1429 · **q:** 1.0000 · **Etki:** 1.170

35 ayet | rotasyonlar arası sıra: 5/35

### ⚪ Tevbe (9): 8-blok ayna skoru 0.724 (rotasyon ort. 0.707)
**Yöntem:** 8 eşit ayet bloğu, ayna blok çiftleri kosinüs; döngüsel kaydırma null modeli · **Ölçüt:** blok ayna skoru = 0.724 · **p:** 0.1473 · **q:** 1.0000 · **Etki:** 1.023

Ayna blok çifti benzerlikleri (dış→iç): 0.65, 0.78, 0.71, 0.76

### ⚪ Kalem (68): ayet düzeyi ayna skoru 0.035 (rotasyon ort. 0.021)
**Yöntem:** Ayna çiftleri (i, n+1-i) kosinüs ortalaması; döngüsel kaydırma null modeli (n rotasyon) · **Ölçüt:** ayna skoru = 0.035 · **p:** 0.1538 · **q:** 1.0000 · **Etki:** 1.636

52 ayet | rotasyonlar arası sıra: 8/52

### ⚪ Kalem (68): 8-blok ayna skoru 0.136 (rotasyon ort. 0.108)
**Yöntem:** 8 eşit ayet bloğu, ayna blok çiftleri kosinüs; döngüsel kaydırma null modeli · **Ölçüt:** blok ayna skoru = 0.136 · **p:** 0.1538 · **q:** 1.0000 · **Etki:** 1.264

Ayna blok çifti benzerlikleri (dış→iç): 0.19, 0.07, 0.09, 0.20

### ⚪ Alak (96): ayet düzeyi ayna skoru 0.095 (rotasyon ort. 0.051)
**Yöntem:** Ayna çiftleri (i, n+1-i) kosinüs ortalaması; döngüsel kaydırma null modeli (n rotasyon) · **Ölçüt:** ayna skoru = 0.095 · **p:** 0.1579 · **q:** 1.0000 · **Etki:** 1.862

19 ayet | rotasyonlar arası sıra: 3/19


## 18. Bilgi Kuramı ve Metin Dinamiği

_Çalışma süresi: 2.58 s_

### 📋 Zipf üssü: lemma 1.00, kök 1.28 | Heaps üssü: lemma 0.58, kök 0.41
**Yöntem:** İlk 1000 sıra log-log eğimi (Zipf); kümülatif kelime dağarcığı büyümesi (Heaps) · **Ölçüt:** Zipf üssü (lemma) = 1.000

58000 içerik lemma tokenı, 4728 farklı lemma; 1651 farklı kök. Doğal dillerde Zipf üssü tipik olarak ~1, Heaps üssü 0.4-0.7 aralığındadır.

### 📋 241 sık kökün 123'i rastlantıdan belirgin biçimde kümeleniyor (z>3); en patlamalı: أثم, قتل, حرم, مكر, ربب (Rab, efendi)
**Yöntem:** Geçişler arası mesafe B=(σ-μ)/(σ+μ); null: tüm kök dizisi 50 kez karıştırılır · **Ölçüt:** kümelenen kök oranı = 0.510

En düzenli (homojen dağılan) kökler: جري B=-0.00, سكن B=-0.01, عرض B=-0.01, حزن B=-0.02, روح B=-0.03, حشر B=-0.03, دبر B=-0.05, قدم B=-0.12

<details><summary>Kanıt (20)</summary>

- أثم B=0.41 (n=48)
- قتل B=0.37 (n=170)
- حرم B=0.36 (n=83)
- مكر B=0.35 (n=43)
- ربب (Rab, efendi) B=0.33 (n=980)
- نسو B=0.32 (n=59)
- نفق B=0.32 (n=111)
- كذب (yalanlamak) B=0.31 (n=282)
- أله (Allah, ilah) B=0.31 (n=2851)
- نجو B=0.30 (n=84)
- رضو B=0.29 (n=73)
- مول B=0.28 (n=86)
- كره B=0.26 (n=41)
- أبو B=0.26 (n=117)
- قوي B=0.25 (n=42)

</details>

### ✅ Ayet uzunluğu dizisinde DFA α=0.895 (tam karıştırma 0.534, sure içi karıştırma 0.885): uzun menzilli belleğin %3'i sure İÇİ sıralamadan, geri kalanı sureler arası farklardan geliyor
**Yöntem:** Detrended Fluctuation Analysis (mushaf sırası, 6236 ayet); null: sure içi karıştırma (40 kez) · **Ölçüt:** DFA α = 0.895 · **p:** 0.0244 · **q:** 0.0366 · **Etki:** 0.009

α=0.5 belleksiz, α>0.5 kalıcı korelasyon. Sure içi null sure düzeyi farkları korur; α'nın bu null'u aşması, sure İÇİNDE de ayet uzunluklarının düzenli (rastgele olmayan) ilerlediğini gösterir.

### ✅ Kafiye (fâsıla harfi) değiştiğinde ardışık ayetlerin sözcüksel benzerliği düşüyor: 0.050 vs 0.057 (etki küçük ama tutarlı: kafiye kısmen konu sınırı işaretidir)
**Yöntem:** Ardışık ayet çiftlerinin içerik-lemma Jaccard benzerliği, kafiye değişen vs değişmeyen; sure içi etiket permütasyonu (1000) · **Ölçüt:** benzerlik farkı = 0.007 · **p:** 0.0010 · **q:** 0.0030 · **Etki:** 1.129

6122 geçiş, 1613 kafiye değişimi

### ⚪ Sure kafiye entropisi nüzul sırasıyla artıyor (rho=+0.02)
**Yöntem:** Ayet sonu harfi dağılımının Shannon entropisi (>= 10 ayetli sureler); Spearman, 2000 permütasyon · **Ölçüt:** Spearman rho = 0.017 · **p:** 0.8656 · **q:** 0.8656 · **Etki:** 0.017

Genel kafiye sürekliliği (ardışık ayetlerde aynı harf): %73.7. Kanıt: en tek-kafiyeli sureler.

<details><summary>Kanıt (8)</summary>

- Fetih H=0.00
- Kamer H=0.00
- Münâfikûn H=0.00
- Cin H=0.00
- İnsân (Dehr) H=0.00
- Şems H=0.00
- Leyl H=0.00
- İsrâ H=0.07

</details>


## 19. Kıssa (Anlatı) Ağı

_Çalışma süresi: 0.24 s_

### 📋 Kıssa haritası: 33 figür, 469 anlatı epizodu; en çok epizot Mûsâ (62 epizot, 34 sure)
**Yöntem:** Özel isim (PN) anılışları; aynı surede <= 5 ayet arayla süren anılışlar tek epizot · **Ölçüt:** epizot sayısı = 469

<details><summary>Kanıt (20)</summary>

- Mûsâ: 62 epizot / 34 sure / 136 anılış
- İbrâhim: 42 epizot / 25 sure / 69 anılış
- Firavun: 40 epizot / 27 sure / 74 anılış
- Nûh: 36 epizot / 28 sure / 43 anılış
- İsrâil(oğulları): 34 epizot / 17 sure / 43 anılış
- Semûd: 23 epizot / 21 sure / 26 anılış
- Îsâ: 20 epizot / 11 sure / 25 anılış
- Meryem: 20 epizot / 12 sure / 34 anılış
- Âd: 20 epizot / 18 sure / 24 anılış
- Hârûn: 19 epizot / 13 sure / 20 anılış
- Lût: 16 epizot / 14 sure / 27 anılış
- Âdem: 14 epizot / 9 sure / 25 anılış
- Ya'kûb: 13 epizot / 10 sure / 16 anılış
- İshâk: 13 epizot / 12 sure / 17 anılış
- Süleymân: 10 epizot / 7 sure / 17 anılış

</details>

### 📋 En uzun kesintisiz kıssa: Mûsâ, A'râf 115-160
**Yöntem:** Epizot uzunluğu (ilk ve son anılış arası ayet sayısı) · **Ölçüt:** ayet = 46

<details><summary>Kanıt (10)</summary>

- Mûsâ: 7:115-160 (17 anılış)
- Yûsuf: 12:76-99 (10 anılış)
- Mûsâ: 28:29-48 (9 anılış)
- Mûsâ: 28:3-20 (7 anılış)
- İbrâhim: 2:124-140 (10 anılış)
- Firavun: 10:75-90 (5 anılış)
- Mûsâ: 10:75-88 (8 anılış)
- Mûsâ: 20:57-70 (5 anılış)
- Dâvûd: 38:17-30 (5 anılış)
- Yûsuf: 12:46-58 (4 anılış)

</details>

### ✅ Helak edilen kavimler 23 surede anlatılıyor; anlatım sırası kanonik Nûh→Âd→Semûd→Lût→Medyen→Firavun sırasına ort. Kendall τ=0.42 ile uyuyor, 9 surede birebir
**Yöntem:** Sure içi her halkanın ANA epizodunun (en çok anılan blok) başlangıç sırası; >= 3 halka içeren sureler; sure başına bağımsız rastgele sıralama, 10000 permütasyon · **Ölçüt:** ort. Kendall tau = 0.420 · **p:** 0.0001 · **q:** 0.0002 · **Etki:** 0.420

Birebir kanonik sırada anlatan sureler: A'râf, Hûd, İsrâ, Kamer, Tahrîm, Fecr, Hac, Fussilet, Tevbe. Sırayı bozan sureler: İbrâhîm, Şuarâ, Neml, Ankebût, Mü'min (Gâfir), Zâriyât, Hâkka, En'âm, Enbiyâ, Furkân, Sâffât, Necm

<details><summary>Kanıt (20)</summary>

- A'râf: Nûh → Âd → Semûd → Lût → Medyen → Firavun/Mûsâ (τ=1.00)
- Hûd: Nûh → Âd → Semûd → Lût → Medyen → Firavun/Mûsâ (τ=1.00)
- İsrâ: Nûh → Semûd → Firavun/Mûsâ (τ=1.00)
- Kamer: Nûh → Âd → Semûd → Lût → Firavun/Mûsâ (τ=1.00)
- Tahrîm: Nûh → Lût → Firavun/Mûsâ (τ=1.00)
- Fecr: Âd → Semûd → Firavun/Mûsâ (τ=1.00)
- Hac: Nûh → Âd → Semûd → Lût → Medyen → Firavun/Mûsâ (τ=1.00)
- Fussilet: Âd → Semûd → Firavun/Mûsâ (τ=1.00)
- Tevbe: Nûh → Âd → Semûd → Medyen (τ=1.00)
- Sâd: Nûh → Âd → Firavun/Mûsâ → Semûd → Lût (τ=0.60)
- Kâf: Nûh → Semûd → Âd → Firavun/Mûsâ → Lût (τ=0.60)
- Ankebût: Nûh → Lût → Medyen → Âd → Semûd → Firavun/Mûsâ (τ=0.47)
- Şuarâ: Firavun/Mûsâ → Nûh → Âd → Semûd → Lût → Medyen (τ=0.33)
- Mü'min (Gâfir): Nûh → Firavun/Mûsâ → Âd → Semûd (τ=0.33)
- Hâkka: Semûd → Âd → Firavun/Mûsâ (τ=0.33)

</details>

### 📋 Figür eşanılma ağı: 28 düğüm, 61 anlamlı bağ (q<0.05)
**Yöntem:** Ayet düzeyi eşanılma, Fisher + BH-FDR · **Ölçüt:** anlamlı bağ = 61

<details><summary>Kanıt (25)</summary>

- İshâk – Ya'kûb: 13 ayette birlikte (beklenenin 317 katı)
- Îsâ – Meryem: 16 ayette birlikte (beklenenin 129 katı)
- Mûsâ – Hârûn: 12 ayette birlikte (beklenenin 29 katı)
- Dâvûd – Süleymân: 7 ayette birlikte (beklenenin 171 katı)
- İbrâhim – Ya'kûb: 9 ayette birlikte (beklenenin 56 katı)
- Semûd – Âd: 8 ayette birlikte (beklenenin 87 katı)
- İshâk – İsmâil: 6 ayette birlikte (beklenenin 195 katı)
- İbrâhim – İshâk: 8 ayette birlikte (beklenenin 49 katı)
- Firavun – Hâmân: 6 ayette birlikte (beklenenin 93 katı)
- Firavun – Mûsâ: 15 ayette birlikte (beklenenin 11 katı)
- İbrâhim – İsmâil: 7 ayette birlikte (beklenenin 58 katı)
- İsmâil – Ya'kûb: 5 ayette birlikte (beklenenin 162 katı)
- Âdem – İblîs: 5 ayette birlikte (beklenenin 113 katı)
- İbrâhim – Nûh: 7 ayette birlikte (beklenenin 16 katı)
- Şuayb – Medyen: 3 ayette birlikte (beklenenin 187 katı)

</details>

### ✅ İshâk – Ya'kûb: 13 ayette birlikte (beklenenin 317 katı)
**Yöntem:** Aynı ayette eşanılma, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 316.672 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 316.672

<details><summary>Kanıt (10)</summary>

- 2:133
- 2:136
- 2:140
- 3:84
- 4:163
- 6:84
- 11:71
- 12:6
- 12:38
- 19:49

</details>

### ✅ Îsâ – Meryem: 16 ayette birlikte (beklenenin 129 katı)
**Yöntem:** Aynı ayette eşanılma, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 128.743 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 128.743

<details><summary>Kanıt (10)</summary>

- 2:87
- 2:253
- 3:45
- 4:157
- 4:171
- 5:46
- 5:78
- 5:110
- 5:112
- 5:114

</details>

### ✅ Mûsâ – Hârûn: 12 ayette birlikte (beklenenin 29 katı)
**Yöntem:** Aynı ayette eşanılma, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 28.562 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 28.562

<details><summary>Kanıt (10)</summary>

- 2:248
- 6:84
- 7:122
- 7:142
- 10:75
- 20:70
- 21:48
- 23:45
- 25:35
- 26:48

</details>

### ✅ Dâvûd – Süleymân: 7 ayette birlikte (beklenenin 171 katı)
**Yöntem:** Aynı ayette eşanılma, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 170.516 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 170.516

<details><summary>Kanıt (7)</summary>

- 4:163
- 6:84
- 21:78
- 21:79
- 27:15
- 27:16
- 38:30

</details>

### ✅ İbrâhim – Ya'kûb: 9 ayette birlikte (beklenenin 56 katı)
**Yöntem:** Aynı ayette eşanılma, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 55.679 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 55.679

<details><summary>Kanıt (9)</summary>

- 2:132
- 2:133
- 2:136
- 2:140
- 3:84
- 4:163
- 12:6
- 12:38
- 38:45

</details>

### ✅ Semûd – Âd: 8 ayette birlikte (beklenenin 87 katı)
**Yöntem:** Aynı ayette eşanılma, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 86.762 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 86.762

<details><summary>Kanıt (8)</summary>

- 9:70
- 14:9
- 22:42
- 25:38
- 29:38
- 40:31
- 41:13
- 69:4

</details>

### ✅ İshâk – İsmâil: 6 ayette birlikte (beklenenin 195 katı)
**Yöntem:** Aynı ayette eşanılma, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 194.875 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 194.875

<details><summary>Kanıt (6)</summary>

- 2:133
- 2:136
- 2:140
- 3:84
- 4:163
- 14:39

</details>

### ✅ İbrâhim – İshâk: 8 ayette birlikte (beklenenin 49 katı)
**Yöntem:** Aynı ayette eşanılma, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 49.492 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 49.492

<details><summary>Kanıt (8)</summary>

- 2:133
- 2:136
- 2:140
- 3:84
- 4:163
- 12:6
- 12:38
- 38:45

</details>

### ✅ Firavun – Hâmân: 6 ayette birlikte (beklenenin 93 katı)
**Yöntem:** Aynı ayette eşanılma, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 93.075 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 93.075

<details><summary>Kanıt (6)</summary>

- 28:6
- 28:8
- 28:38
- 29:39
- 40:24
- 40:36

</details>

### ✅ Firavun – Mûsâ: 15 ayette birlikte (beklenenin 11 katı)
**Yöntem:** Aynı ayette eşanılma, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 10.657 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 10.657

<details><summary>Kanıt (10)</summary>

- 7:103
- 7:104
- 7:127
- 10:75
- 10:83
- 10:88
- 14:6
- 17:101
- 28:3
- 28:38

</details>

### ✅ İbrâhim – İsmâil: 7 ayette birlikte (beklenenin 58 katı)
**Yöntem:** Aynı ayette eşanılma, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 57.741 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 57.741

<details><summary>Kanıt (7)</summary>

- 2:125
- 2:127
- 2:133
- 2:136
- 2:140
- 3:84
- 4:163

</details>

### ✅ İsmâil – Ya'kûb: 5 ayette birlikte (beklenenin 162 katı)
**Yöntem:** Aynı ayette eşanılma, tek yönlü Fisher, BH-FDR · **Ölçüt:** lift = 162.396 · **p:** 0.0000 · **q:** 0.0000 · **Etki:** 162.396

<details><summary>Kanıt (5)</summary>

- 2:133
- 2:136
- 2:140
- 3:84
- 4:163

</details>

### ✅ Anlatı (kıssa) yoğunluğu dönemlere göre farklı; zirve: Orta Mekkî (%14 ayet)
**Yöntem:** Sure başına kıssa epizodu içindeki ayet oranı; nüzul sırasına göre Mekkî üçte birlikler + Medenî; Kruskal-Wallis · **Ölçüt:** H = 14.007 · **p:** 0.0031 · **q:** 0.0031

Nüzul sırası geleneksel (Mısır/Ezher) listeye dayanır; dönem sınırları eşit sayılı üçte birliklerdir.

<details><summary>Kanıt (4)</summary>

- Erken Mekkî: %1.6
- Orta Mekkî: %14.1
- Geç Mekkî: %6.2
- Medenî: %5.0

</details>


---
**Simgeler:** ✅ FDR sonrası anlamlı · ⚪ anlamsız / negatif sonuç · 📋 betimsel envanter · 🤖 LLM etiketi kullanır
