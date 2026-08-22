#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kur'an-ı Kerim Arapça Metin, Okunuş ve Doğal Türkçe Meal Derleyici
Bu script, 114 surenin tamamını (6.236 ayet) içeren kapsamlı ve detaylı Markdown dosyaları üretir.
"""

import json
import os
import re
import urllib.request
import time

SURAH_METADATA = {
    1: {
        "name_tr": "Fâtiha", "name_ar": "سُورَةُ الفَاتِحَةِ", "meaning": "Açılış, Başlangıç",
        "place": "Mekke", "order": 5, "verses": 7, "juz": "1. Cüz",
        "summary": "Kur'an'ın ilk suresi ve 'Ümmü'l-Kitap' (Kitabın Anası) olarak kabul edilir. Allah'a hamd, O'nun sonsuz merhameti (Rahmân ve Rahîm), hesap gününün yegâne hâkimi oluşu, sadece O'na kulluk ve O'ndan yardım dileme ile dosdoğru yola iletilme dualarını ihtiva eder."
    },
    2: {
        "name_tr": "Bakara", "name_ar": "سُورَةُ البَقَرَةِ", "meaning": "Sığır, İnek",
        "place": "Medine", "order": 87, "verses": 286, "juz": "1, 2, 3. Cüz",
        "summary": "Kur'an-ı Kerim'in en uzun suresidir. İman esasları, ibadetler (namaz, oruç, hac, zekât, infak), aile hukuku, sosyal düzen, faiz yasağı, Hz. Âdem'in yaratılışı, Hz. İbrahim ve İsmail'in Kâbe'yi inşası, İsrâiloğulları kıssası ve en faziletli ayetlerden kabul edilen Ayete'l-Kürsî (255. ayet) ile Âmenerrasûlü (285-286) bu surede yer alır."
    },
    3: {
        "name_tr": "Âl-i İmrân", "name_ar": "سُورَةُ آلِ عِمْرَانَ", "meaning": "İmrân Ailesi",
        "place": "Medine", "order": 89, "verses": 200, "juz": "3, 4. Cüz",
        "summary": "Tevhid inancı, Hz. İsa ve annesi Hz. Meryem'in kıssası, Hristiyan teolojisine cevaplar, Bedir ve Uhud Savaşları'nın tahlili ve Müslüman toplumun iç dayanışması ile istikamet ilkeleri işlenir."
    },
    4: {
        "name_tr": "Nisâ", "name_ar": "سُورَةُ النِّسَاءِ", "meaning": "Kadınlar",
        "place": "Medine", "order": 92, "verses": 176, "juz": "4, 5, 6. Cüz",
        "summary": "Kadın hakları, aile hukuku, miras taksimi (ferâiz), yetimlerin ve zayıfların korunması, adalet, yöneticilere itaat, münafıkların nitelikleri ve cihad prensipleri ayrıntılı biçimde ele alınır."
    },
    5: {
        "name_tr": "Mâide", "name_ar": "سُورَةُ المَائِدَةِ", "meaning": "Donatılmış Sofra",
        "place": "Medine", "order": 112, "verses": 120, "juz": "6, 7. Cüz",
        "summary": "Verilen sözlere ve akitlere bağlılık, helal ve haram yiyecekler, abdest ve teyemmüm hükümleri, Ehl-i Kitap ile münasebetler, Hz. Musa ve kavmi, Hâbil-Kâbil kıssası ve Hz. İsa'nın havarileriyle olan sofra hadisesi anlatılır."
    },
    6: {
        "name_tr": "En'âm", "name_ar": "سُورَةُ الأَنْعَامِ", "meaning": "Ehli Hayvanlar (Davarlar)",
        "place": "Mekke", "order": 55, "verses": 165, "juz": "7, 8. Cüz",
        "summary": "Tevhid akidesinin delilleri, kâinattaki ilahî nizam, şirkin mantıksızlığı, peygamberlerin tevhid mücadelesi ve Hz. İbrahim'in yıldızlar ve güneşe bakarak Rabbini buluşu derin bir tefekkürle sunulur."
    },
    7: {
        "name_tr": "A'râf", "name_ar": "سُورَةُ الأَعْرَافِ", "meaning": "Yüksek Yerler, Tepe Noktaları",
        "place": "Mekke", "order": 39, "verses": 206, "juz": "8, 9. Cüz",
        "summary": "Cennet ile cehennem arasındaki A'râf ehli, Hz. Âdem ile İblis'in kıssası, Hz. Nuh, Hûd, Salih, Lût, Şuayb ve özellikle Hz. Musa ile Firavun arasındaki mücadele genişçe işlenir."
    },
    8: {
        "name_tr": "Enfâl", "name_ar": "سُورَةُ الأَنْفَالِ", "meaning": "Savaş Ganimetleri",
        "place": "Medine", "order": 88, "verses": 75, "juz": "9, 10. Cüz",
        "summary": "Bedir Savaşı'nın stratejik ve manevi değerlendirmesi, ilahî yardım (meleklerin inişi), ganimetlerin taksimi, müminlerin vasıfları ve cihad ahlakı açıklanır."
    },
    9: {
        "name_tr": "Tevbe", "name_ar": "سُورَةُ التَّوْبَةِ", "meaning": "Tövbe, Pişmanlık",
        "place": "Medine", "order": 113, "verses": 129, "juz": "10, 11. Cüz",
        "summary": "Başında Besmele bulunmayan tek suredir. Müşriklerle yapılan antlaşmaların feshi, Tebük Seferi, münafıkların ikiyüzlü tavırları, samimi tövbenin kabulü ve zekâtın verileceği sekiz sınıf zikredilir."
    },
    10: {
        "name_tr": "Yûnus", "name_ar": "سُورَةُ يُونُسَ", "meaning": "Hz. Yûnus Peygamber",
        "place": "Mekke", "order": 51, "verses": 109, "juz": "11. Cüz",
        "summary": "İlahî vahyin hakikati, kâinattaki yaratılış delilleri, Hz. Nuh ve Hz. Musa kıssaları ile azap gelmeden önce iman edip kurtulan Yûnus peygamberin kavminin ibretlik durumu anlatılır."
    },
    11: {
        "name_tr": "Hûd", "name_ar": "سُورَةُ هُودٍ", "meaning": "Hz. Hûd Peygamber",
        "place": "Mekke", "order": 52, "verses": 123, "juz": "11, 12. Cüz",
        "summary": "Hz. Peygamber'in 'Beni ihtiyarlattı' buyurduğu surelerdendir. 'Emrolunduğun gibi dosdoğru ol!' emri, Nuh tufanı ve oğluyla konuşması, Âd, Semûd, Medyen ve Lût kavimlerinin helaki vurgulanır."
    },
    12: {
        "name_tr": "Yûsuf", "name_ar": "سُورَةُ يُوسُفَ", "meaning": "Hz. Yûsuf Peygamber",
        "place": "Mekke", "order": 53, "verses": 111, "juz": "12, 13. Cüz",
        "summary": "Kur'an'da 'Ahsenü'l-Kasas' (Kıssaların En Güzeli) olarak nitelendirilir. Hz. Yûsuf'un kuyuya atılmasından Mısır'a sultan oluşuna kadar geçen sabır, iffet, tevekkül ve af dersleri baştan sona bir bütünlük içinde anlatılır."
    },
    13: {
        "name_tr": "Ra'd", "name_ar": "سُورَةُ الرَّعْدِ", "meaning": "Gök Gürültüsü",
        "place": "Medine", "order": 96, "verses": 43, "juz": "13. Cüz",
        "summary": "Gök gürültüsünün ve meleklerin Allah'ı tesbih edişi, kalplerin ancak Allah'ın zikriyle mutmain olacağı (28. ayet) ve hak ile batılın berrak su ile köpük misali karşılaştırılması yapılır."
    },
    14: {
        "name_tr": "İbrâhîm", "name_ar": "سُورَةُ إِبْرَاهِيمَ", "meaning": "Hz. İbrâhîm Peygamber",
        "place": "Mekke", "order": 72, "verses": 52, "juz": "13. Cüz",
        "summary": "İnsanları karanlıklardan aydınlığa çıkaran vahiy, güzel ve çirkin sözün misalleri (kökü sağlam ağaç), Hz. İbrahim'in Mekke ve zürriyeti için yaptığı samimi dualar yer alır."
    },
    15: {
        "name_tr": "Hicr", "name_ar": "سُورَةُ الحِجْرِ", "meaning": "Hicr Bölgesi (Semûd Kavmi Yurdu)",
        "place": "Mekke", "order": 54, "verses": 99, "juz": "14. Cüz",
        "summary": "Kur'an'ın Allah tarafından kıyamete kadar korunacağı vaadi (9. ayet), İblis'in secde etmeyişi ve kovuluşu, meleklerin Hz. İbrahim ve Hz. Lût'a müjdeli ve uyarıcı ziyaretleri anlatılır."
    },
    16: {
        "name_tr": "Nahl", "name_ar": "سُورَةُ النَّحْلِ", "meaning": "Bal Arısı",
        "place": "Mekke", "order": 70, "verses": 128, "juz": "14. Cüz",
        "summary": "'Nimetler Suresi' olarak da bilinir. Bal arısının ilahî ilhamla çalışması, süt veren hayvanlar, gökten inen yağmur, adalet, ihsan ve akrabaya yardımı emreden meşhur Cuma hutbesi ayeti (90. ayet) buradadır."
    },
    17: {
        "name_tr": "İsrâ", "name_ar": "سُورَةُ الإِسْرَاءِ", "meaning": "Gece Yürüyüşü",
        "place": "Mekke", "order": 50, "verses": 111, "juz": "15. Cüz",
        "summary": "Hz. Peygamber'in Mescid-i Haram'dan Mescid-i Aksâ'ya gece yolculuğu (İsrâ ve Mirac), anne-babaya saygı ve hürmet kuralları, İslam ahlakının temel on iki emri ve ruhun mahiyeti konu edilir."
    },
    18: {
        "name_tr": "Kehf", "name_ar": "سُورَةُ الكَهْفِ", "meaning": "Mağara",
        "place": "Mekke", "order": 69, "verses": 110, "juz": "15, 16. Cüz",
        "summary": "Zulümden kaçıp mağaraya sığınan Ashâb-ı Kehf gençleri, iki bahçe sahibi zengin ve fakir adam misali, Hz. Musa ile Hızır'ın hikmet yolculuğu ve Zülkarneyn ile Ye'cüc-Me'cüc kıssası aktarılır."
    },
    19: {
        "name_tr": "Meryem", "name_ar": "سُورَةُ مَرْيَمَ", "meaning": "Hz. Meryem",
        "place": "Mekke", "order": 44, "verses": 98, "juz": "16. Cüz",
        "summary": "Hz. Zekeriyya'nın duası ve Hz. Yahya'nın müjdelenmesi, Hz. Meryem'in babasız olarak Hz. İsa'yı dünyaya getiriş mucizesi, Hz. İbrahim'in babasına tevhid daveti ve diğer peygamberlerin faziletleri zikredilir."
    },
    20: {
        "name_tr": "Tâhâ", "name_ar": "سُورَةُ طه", "meaning": "Tâ-Hâ Harfleri",
        "place": "Mekke", "order": 45, "verses": 135, "juz": "16. Cüz",
        "summary": "Kur'an'ın bir bedbahtlık kaynağı değil rahmet oluşu, Hz. Musa'nın Tur Dağı'nda vahiy alışı, Firavun'a yumuşak sözle (kavl-i leyyin) tebliği, sihirbazların imanı ve Sâmirî'nin buzağı fitnesi işlenir."
    },
    21: {
        "name_tr": "Enbiyâ", "name_ar": "سُورَةُ الأَنْبِيَاءِ", "meaning": "Peygamberler",
        "place": "Mekke", "order": 73, "verses": 112, "juz": "17. Cüz",
        "summary": "Peygamberler geçidi gibidir: Hz. İbrahim'in putları kırması ve ateşe atılıp kurtuluşu, Hz. Eyyûb'un sabrı ve şifası, Hz. Yûnus'un balığın karnındaki duası ve Hz. Muhammed'in âlemlere rahmet olarak gönderilişi yer alır."
    },
    22: {
        "name_tr": "Hac", "name_ar": "سُورَةُ الحَجِّ", "meaning": "Hac İbadeti",
        "place": "Medine", "order": 103, "verses": 78, "juz": "17. Cüz",
        "summary": "Kıyamet sarsıntısının dehşeti, hac ibadetinin menâsiki ve kurbanın takvası, Kâbe'nin Hz. İbrahim tarafından yapılışı, zulme uğrayan müminlere savunma amaçlı savaş izninin ilk defa verilişi anlatılır."
    },
    23: {
        "name_tr": "Mü'minûn", "name_ar": "سُورَةُ المُؤْمِنُونَ", "meaning": "Müminler, İnananlar",
        "place": "Mekke", "order": 74, "verses": 118, "juz": "18. Cüz",
        "summary": "Kurtuluşa eren gerçek müminlerin vasıfları (namazda huşu, boş şeylerden yüz çevirme, iffeti koruma, emanete riayet), insanın anne karnındaki yaratılış evreleri ve ahiret sorumluluğu beyan edilir."
    },
    24: {
        "name_tr": "Nûr", "name_ar": "سُورَةُ النُّورِ", "meaning": "İlahî Nur, Işık",
        "place": "Medine", "order": 102, "verses": 64, "juz": "18. Cüz",
        "summary": "Toplum ve aile ahlakı, iffet ve tesettür kuralları, Hz. Âişe'ye yapılan iftiranın (İfk hadisesi) ilahî beyanla çürütülmesi ve Allah'ın göklerin ve yerin nuru olduğunu bildiren muazzam Nûr Ayeti (35. ayet) buradadır."
    },
    25: {
        "name_tr": "Furkân", "name_ar": "سُورَةُ الفُرْقَانِ", "meaning": "Hak ile Bâtılı Ayıran",
        "place": "Mekke", "order": 42, "verses": 77, "juz": "18, 19. Cüz",
        "summary": "Kur'an'ın hakkı batıldan ayıran özelliği, inkârcıların peygamberlere itirazları ve surenin sonunda 'İbâdü'r-Rahmân' (Rahmân'ın seçkin kulları) olarak adlandırılan erdemli insanların güzel ahlakı övülür."
    },
    26: {
        "name_tr": "Şuarâ", "name_ar": "سُورَةُ الشُّعَرَاءِ", "meaning": "Şairler",
        "place": "Mekke", "order": 47, "verses": 227, "juz": "19. Cüz",
        "summary": "Peygamberlerin kavimleriyle mücadelesi ritmik ve etkileyici bir ahenkle sunulur. Hakikati çarpıtan söz cambazı şairler ile iman edip salih amel işleyen erdemli sanatkârlar birbirinden ayrılır."
    },
    27: {
        "name_tr": "Neml", "name_ar": "سُورَةُ النَّمْلِ", "meaning": "Karınca",
        "place": "Mekke", "order": 48, "verses": 93, "juz": "19, 20. Cüz",
        "summary": "Hz. Süleyman'ın kuşlar, cinler ve rüzgâr üzerindeki hâkimiyeti, karınca ile olan diyaloğu, Hüdhüd kuşu ve Sebe Melikesi Belkıs'ın tevhid dinini kabul edişi anlatılır."
    },
    28: {
        "name_tr": "Kasas", "name_ar": "سُورَةُ القَصَصِ", "meaning": "Tarihî Kıssalar ve Anlatılar",
        "place": "Mekke", "order": 49, "verses": 88, "juz": "20. Cüz",
        "summary": "Hz. Musa'nın nehre bırakılan bir bebekten sarayda büyümesine, Medyen'e hicretine ve Firavun'a karşı tebliğine kadar olan hayatı ile akıl almaz servetiyle şımarıp yere batan Kârûn'un hazin sonu işlenir."
    },
    29: {
        "name_tr": "Ankebût", "name_ar": "سُورَةُ العَنْكَبُوتِ", "meaning": "Örümcek",
        "place": "Mekke", "order": 85, "verses": 69, "juz": "20, 21. Cüz",
        "summary": "İman iddiasının imtihansız bırakılmayacağı gerçeği (2-3. ayetler), Allah'tan başka sığınak arayanların dayanağının örümcek ağı (en zayıf ev) misali olduğu çarpıcı bir şekilde ifade edilir."
    },
    30: {
        "name_tr": "Rûm", "name_ar": "سُورَةُ الرُّومِ", "meaning": "Romalılar (Bizans)",
        "place": "Mekke", "order": 84, "verses": 60, "juz": "21. Cüz",
        "summary": "Sasani-Bizans savaşında yenilen Bizanslıların birkaç yıl içinde galip geleceği gaybî mucizesi, eşler arasındaki sevgi ve merhamet, kâinattaki yaratılış delilleri ve insanın fıtratı konu edilir."
    },
    31: {
        "name_tr": "Lokmân", "name_ar": "سُورَةُ لُقْمَانَ", "meaning": "Hz. Lokmân Hekim",
        "place": "Mekke", "order": 57, "verses": 34, "juz": "21. Cüz",
        "summary": "Hikmet sahibi Hz. Lokmân'ın oğluna verdiği altın değerindeki nasihatler: Şirkten kaçınma, anne-babaya saygı, namazı kılma, iyiliği emredip kötülükten sakındırma, sabır ve kibirlenmeme ilkeleri."
    },
    32: {
        "name_tr": "Secde", "name_ar": "سُورَةُ السَّجْدَةِ", "meaning": "Secde Etmek",
        "place": "Mekke", "order": 75, "verses": 30, "juz": "21. Cüz",
        "summary": "İnsanın çamurdan yaratılışı ve ona ilahî ruhun üflenmesi, geceleri yataklarından kalkıp Rablerine dua edenlerin mükafatları ve kıyamet gününde suçluların çaresiz pişmanlığı işlenir."
    },
    33: {
        "name_tr": "Ahzâb", "name_ar": "سُورَةُ الأَحْزَابِ", "meaning": "Gruplar, Birleşik Ordular",
        "place": "Medine", "order": 90, "verses": 73, "juz": "21, 22. Cüz",
        "summary": "Hendek Savaşı ve kuşatması, münafıkların korkaklığı, evlatlık hukuku, Hz. Peygamber'in 'Üsve-i Hasene' (En Güzel Örnek) oluşu ve O'nun mübarek hanımları ve ailesinin konumu anlatılır."
    },
    34: {
        "name_tr": "Sebe'", "name_ar": "سُورَةُ سَبَإٍ", "meaning": "Sebe Kavmi / Diyarı",
        "place": "Mekke", "order": 58, "verses": 54, "juz": "22. Cüz",
        "summary": "Hz. Dâvûd ve Hz. Süleyman'a bahşedilen mucizeler, Sebe halkının nankörlüğü sonucu maruz kaldığı 'Arim Seli' felaketi ve ahirette şirkin hiçbir fayda vermeyeceği vurgulanır."
    },
    35: {
        "name_tr": "Fâtır", "name_ar": "سُورَةُ فَاطِرٍ", "meaning": "Yoktan Yaratan, Var Eden",
        "place": "Mekke", "order": 43, "verses": 45, "juz": "22. Cüz",
        "summary": "Allah'ın melekleri elçiler kılması, insanların Allah'a muhtaç (fakir) olduğu, kimsenin başkasının günah yükünü taşımayacağı ve 'Allah'tan hakkıyla ancak âlim kulları korkar' ilkesi yer alır."
    },
    36: {
        "name_tr": "Yâsîn", "name_ar": "سُورَةُ يس", "meaning": "Yâ-Sîn Harfleri",
        "place": "Mekke", "order": 41, "verses": 83, "juz": "22, 23. Cüz",
        "summary": "Kur'an-ı Kerim'in 'kalbi' olarak nitelendirilir. Peygamberlik müessesesi, Antakya elçileri ve Habîb-i Neccâr'ın fedakârlığı, tabiatın canlanışı ve öldükten sonra dirilmenin kesinliği güçlü delillerle anlatılır."
    },
    37: {
        "name_tr": "Sâffât", "name_ar": "سُورَةُ الصَّافَّاتِ", "meaning": "Sıra Sıra Dizilenler (Melekler)",
        "place": "Mekke", "order": 56, "verses": 182, "juz": "23. Cüz",
        "summary": "Meleklerin intizamı, şeytanların gökten kovulması, Hz. İbrahim'in oğlunu kurban etme imtihanı ve teslimiyeti, Hz. İlyas, Lut ve Yûnus'un tebliğleri işlenir."
    },
    38: {
        "name_tr": "Sâd", "name_ar": "سُورَةُ ص", "meaning": "Sâd Harfi",
        "place": "Mekke", "order": 38, "verses": 88, "juz": "23. Cüz",
        "summary": "Hz. Dâvûd'un adil hükümdarlığı ve istiğfarı, Hz. Süleyman'ın şükrü, Hz. Eyyûb'un sabrı ve Hz. Âdem'e secde etmeyen İblis'in lanetlenmesi kıssası anlatılır."
    },
    39: {
        "name_tr": "Zümer", "name_ar": "سُورَةُ الزُّمَرِ", "meaning": "Zümreler, Bölükler",
        "place": "Mekke", "order": 59, "verses": 75, "juz": "23, 24. Cüz",
        "summary": "Dini yalnızca Allah'a halis kılma emri, Allah'ın rahmetinden ümit kesmeme müjdesi ('Ey nefislerine zulmeden kullarım...', 53. ayet), cennet ve cehenneme bölük bölük sevk edilen insanların durumu."
    },
    40: {
        "name_tr": "Mü'min (Gâfir)", "name_ar": "سُورَةُ غَافِرٍ", "meaning": "İnanan Kişi / Günahları Bağışlayan",
        "place": "Mekke", "order": 60, "verses": 85, "juz": "24. Cüz",
        "summary": "Hâ-Mîm ile başlayan yedi surenin ilkidir. Firavun'un sarayında imanını gizleyip Hz. Musa'yı savunan mümin adamın ibretlik hitabı ve Arş'ı taşıyan meleklerin müminler için yaptıkları dualar yer alır."
    },
    41: {
        "name_tr": "Fussilet", "name_ar": "سُورَةُ فُصِّلَتْ", "meaning": "Ayrıntılı Olarak Açıklanmış",
        "place": "Mekke", "order": 61, "verses": 54, "juz": "24, 25. Cüz",
        "summary": "Kur'an ayetlerinin hikmetle açıklanması, kâinatın yaratılış aşamaları, insanın kulaklarının, gözlerinin ve derisinin ahirette aleyhine şahitlik edeceği ve 'Kötülüğü en güzel olanla sav' ahlakı anlatılır."
    },
    42: {
        "name_tr": "Şûrâ", "name_ar": "سُورَةُ الشُّورَى", "meaning": "Danışma, İstişare",
        "place": "Mekke", "order": 62, "verses": 53, "juz": "25. Cüz",
        "summary": "Müminlerin işlerini istişare ile yürütmeleri (38. ayet), bütün peygamberlere vahyedilen dinin temelde bir olduğu ve Allah'ın benzeri hiçbir şeyin bulunmadığı (Leyse kemislihî şey') beyan edilir."
    },
    43: {
        "name_tr": "Zuhruf", "name_ar": "سُورَةُ الزُّخْرُفِ", "meaning": "Altın, Mücevher ve Yaldız",
        "place": "Mekke", "order": 63, "verses": 89, "juz": "25. Cüz",
        "summary": "Dünya hayatının geçici debdebe ve süsü, müşriklerin peygamberlik beklentilerindeki sığ zihniyet ve Hz. İsa'nın yalnızca bir kul ve peygamber olduğu gerçeği vurgulanır."
    },
    44: {
        "name_tr": "Duhân", "name_ar": "سُورَةُ الدُّخَانِ", "meaning": "Duman",
        "place": "Mekke", "order": 64, "verses": 59, "juz": "25. Cüz",
        "summary": "Kur'an'ın mübarek bir gecede (Kadir Gecesi) indirildiği, inkârcıları kuşatacak helak edici duman azabı, Firavun ve ordusunun denizde boğulması anlatılır."
    },
    45: {
        "name_tr": "Câsiye", "name_ar": "سُورَةُ الجَاثِيَةِ", "meaning": "Diz Üstü Çöken Topluluk",
        "place": "Mekke", "order": 65, "verses": 37, "juz": "25. Cüz",
        "summary": "Göklerde ve yerde akıl sahipleri için nice deliller bulunduğu, heva ve hevesini ilah edinenlerin sapkınlığı ve kıyamet günü her ümmetin diz üstü çökmüş olarak hesap bekleyeceği sahnelenir."
    },
    46: {
        "name_tr": "Ahkâf", "name_ar": "سُورَةُ الأَحْقَافِ", "meaning": "Kum Tepeleri (Âd Kavmi Yurdu)",
        "place": "Mekke", "order": 66, "verses": 35, "juz": "26. Cüz",
        "summary": "Âd kavminin kum tepeleri arasındaki helaki, anne-babaya iyilik ve kırk yaşına basan insanın yapacağı dua, cinlerin Kur'an'ı dinleyip iman etmeleri ve peygamberlerin azimli oluşu (Ülü'l-azm) anlatılır."
    },
    47: {
        "name_tr": "Muhammed", "name_ar": "سُورَةُ مُحَمَّدٍ", "meaning": "Hz. Muhammed (s.a.v.)",
        "place": "Medine", "order": 95, "verses": 38, "juz": "26. Cüz",
        "summary": "Hak ile batılın mücadelesi, savaş esirlerine muamele, cennet ehlinin pınarları ve nimetleri ile münafıkların savaştan kaçma gayretleri ele alınır."
    },
    48: {
        "name_tr": "Fetih", "name_ar": "سُورَةُ الفَتْحِ", "meaning": "Zafer, Açılış (Hudeybiye Barışı)",
        "place": "Medine", "order": 111, "verses": 29, "juz": "26. Cüz",
        "summary": "Hudeybiye Barışı'nın apaçık bir fetih olduğu müjdesi, Rıdvan Biatı, müminlerin kalplerine inen sekinet (huzur) ve Hz. Muhammed ile ashabının Tevrat ve İncil'deki vasıfları övgüyle anlatılır."
    },
    49: {
        "name_tr": "Hucurât", "name_ar": "سُورَةُ الحُجُرَاتِ", "meaning": "Odalar, Hücreler",
        "place": "Medine", "order": 106, "verses": 18, "juz": "26. Cüz",
        "summary": "İslam ahlak ve edep manifestosudur: Peygamber'e karşı saygı, haberlerin doğruluğunu araştırma (fâsık haberi), müminlerin kardeşliği, alay etmeme, gıybet ve suizandan kaçınma ve takva üstünlüğü zikredilir."
    },
    50: {
        "name_tr": "Kâf", "name_ar": "سُورَةُ ق", "meaning": "Kâf Harfi",
        "place": "Mekke", "order": 34, "verses": 45, "juz": "26. Cüz",
        "summary": "Öldükten sonra dirilişin tabiat delilleriyle ispatı, insanın şah damarından daha yakın olan Allah, amelleri kaydeden iki melek (Rakîb ve Atîd) ve cehennemin 'Daha var mı?' deyişi."
    },
    51: {
        "name_tr": "Zâriyât", "name_ar": "سُورَةُ الذَّارِيَاتِ", "meaning": "Toz Kaldırıp Savuran Rüzgârlar",
        "place": "Mekke", "order": 67, "verses": 60, "juz": "26, 27. Cüz",
        "summary": "Rızkın göklerde ve ilahî teminat altında oluşu, insanın ve cinlerin yaratılış gayesinin yalnızca Allah'a kulluk olduğu meşhur ayet (56. ayet) ve Hz. İbrahim'e gelen melek misafirler anlatılır."
    },
    52: {
        "name_tr": "Tûr", "name_ar": "سُورَةُ الطُّورِ", "meaning": "Tur Dağı (Sînâ Dağı)",
        "place": "Mekke", "order": 76, "verses": 49, "juz": "27. Cüz",
        "summary": "Tur Dağı, Beyt-i Ma'mûr ve kaynayan denizler üzerine yeminle başlayan azap uyarısı; cennet ehlinin sevinçli sohbetleri ve inkârcıların peygambere attığı iftiraların çürütülmesi."
    },
    53: {
        "name_tr": "Necm", "name_ar": "سُورَةُ النَّجْمِ", "meaning": "Kayan Yıldız",
        "place": "Mekke", "order": 23, "verses": 62, "juz": "27. Cüz",
        "summary": "Hz. Peygamber'in vahyi hevasından konuşmadığı, Mirac gecesinde Cebrail'i asli suretinde ve Sidretü'l-Müntehâ'da görüşü, putların değersizliği ve insanın ancak emeğinin karşılığını alacağı prensibi."
    },
    54: {
        "name_tr": "Kamer", "name_ar": "سُورَةُ القَمَرِ", "meaning": "Ay",
        "place": "Mekke", "order": 37, "verses": 55, "juz": "27. Cüz",
        "summary": "Ayın yarılması mucizesi, Nuh, Âd, Semûd, Lût ve Firavun kavimlerinin akıbetleri ve 'Andolsun biz Kur'an'ı düşünüp öğüt alınsın diye kolaylaştırdık; var mı öğüt alan?' ayetinin tekrarlanan teyidi."
    },
    55: {
        "name_tr": "Rahmân", "name_ar": "سُورَةُ الرَّحْمَٰنِ", "meaning": "Sonsuz Merhamet Sahibi Allah",
        "place": "Medine", "order": 97, "verses": 78, "juz": "27. Cüz",
        "summary": "'Kur'an'ın Gelini' (Arûsü'l-Kur'an) olarak adlandırılır. İnsana konuşma yeteneği verilmesi, iki denizin birbirine karışmaması, cennetin pınarları ve 'Rabbinizin hangi nimetlerini yalanlayabilirsiniz?' nidası."
    },
    56: {
        "name_tr": "Vâkı'a", "name_ar": "سُورَةُ الوَاقِعَةِ", "meaning": "Kesinlikle Gerçekleşecek Olan (Kıyamet)",
        "place": "Mekke", "order": 46, "verses": 96, "juz": "27. Cüz",
        "summary": "Kıyamet koptuğunda insanların üçe ayrılması: Öncüler (Sâbikûn), amel defteri sağdan verilenler (Ashâb-ı Meymene) ve amel defteri soldan verilen bahtsızlar (Ashâb-ı Meş'eme)."
    },
    57: {
        "name_tr": "Hadîd", "name_ar": "سُورَةُ الحَدِيدِ", "meaning": "Demir",
        "place": "Medine", "order": 94, "verses": 29, "juz": "27. Cüz",
        "summary": "Göklerde ve yerdeki her şeyin Allah'ı tesbih edişi, Allah yolunda infak, demirin indirilmesi ve onda insanlara büyük faydalar bulunması, dünya hayatının aldatıcı bir meta oluşu işlenir."
    },
    58: {
        "name_tr": "Mücâdele", "name_ar": "سُورَةُ المُجَادَلَةِ", "meaning": "Tartışan, Hakkını Arayan Kadın",
        "place": "Medine", "order": 105, "verses": 22, "juz": "28. Cüz",
        "summary": "Kocasını şikayet eden Havle bnt. Sa'lebe'nin feryadının Allah tarafından işitilmesi, cahiliye âdeti olan 'zıhâr' geleneğinin kaldırılması, fısıldaşma (necvâ) ahlakı ve Allah taraftarlarının (Hizbullah) zaferi."
    },
    59: {
        "name_tr": "Haşr", "name_ar": "سُورَةُ الحَشْرِ", "meaning": "Toplanma, Sürgün",
        "place": "Medine", "order": 101, "verses": 24, "juz": "28. Cüz",
        "summary": "İhanet eden Benî Nadîr kabilesinin Medine'den sürgünü, fey gelirlerinin taksimi, 'Eğer biz bu Kur'an'ı bir dağa indirseydik...' ayeti ve surenin sonundaki muazzam Esmâü'l-Hüsnâ (Hüvallâhüllezî...)."
    },
    60: {
        "name_tr": "Mümtehine", "name_ar": "سُورَةُ المُمْتَحَنَةِ", "meaning": "İmtihan Edilen Kadın",
        "place": "Medine", "order": 91, "verses": 13, "juz": "28. Cüz",
        "summary": "Mekke'den Medine'ye hicret eden kadınların imanlarının sınanması, müminlere düşmanlık etmeyen gayrimüslimlerle adalet ve iyilik çerçevesinde ilişkiler kurulabileceği hükmü."
    },
    61: {
        "name_tr": "Saf", "name_ar": "سُورَةُ الصَّفِّ", "meaning": "Sıra Sıra Saf Tutmak",
        "place": "Medine", "order": 109, "verses": 14, "juz": "28. Cüz",
        "summary": "'Yapmayacağınız şeyleri niçin söylersiniz?' uyarısı, Allah yolunda kurşunla kaynatılmış binalar gibi saf bağlayarak cihad edenler ve Hz. İsa'nın kendisinden sonra gelecek 'Ahmed' isimli peygamberi müjdelemesi."
    },
    62: {
        "name_tr": "Cuma", "name_ar": "سُورَةُ الجُمُعَةِ", "meaning": "Cuma Günü ve Toplanma",
        "place": "Medine", "order": 110, "verses": 11, "juz": "28. Cüz",
        "summary": "Tevrat'la amel etmeyenlerin kitap yüklü merkeplere benzetilmesi, Cuma ezanı okunduğunda alışverişin bırakılıp namaza ve zikre koşulması emri."
    },
    63: {
        "name_tr": "Münâfikûn", "name_ar": "سُورَةُ المُنَافِقُونَ", "meaning": "İkiyüzlü Münafıklar",
        "place": "Medine", "order": 104, "verses": 11, "juz": "28. Cüz",
        "summary": "Münafıkların sahte yeminleri, kalplerinin mühürlenmesi, gösterişli kalıpları ancak duvara dayanmış kütüklere benzemeleri ve ölüm gelmeden önce infak etme çağrısı."
    },
    64: {
        "name_tr": "Tegâbün", "name_ar": "سُورَةُ التَّغَابُنِ", "meaning": "Aldanma ve Kâr-Zararın Ortaya Çıkması",
        "place": "Medine", "order": 108, "verses": 18, "juz": "28. Cüz",
        "summary": "Kıyamet gününün kimin kârda kimin zararda olduğunu göstereceği (Tegâbün Günü), malların ve evlatların birer imtihan vesilesi olduğu ve gücün yettiğince Allah'tan sakınma emri."
    },
    65: {
        "name_tr": "Talâk", "name_ar": "سُورَةُ الطَّلَاقِ", "meaning": "Boşanma Hükümleri",
        "place": "Medine", "order": 99, "verses": 12, "juz": "28. Cüz",
        "summary": "Boşanma usulü, iddet süresi, nafaka ve mesken hakları, 'Kim Allah'tan sakınırsa, Allah ona bir çıkış yolu ihsan eder ve ummadığı yerden rızıklandırır' müjdesi."
    },
    66: {
        "name_tr": "Tahrîm", "name_ar": "سُورَةُ التَّحْرِيمِ", "meaning": "Haram Kılma, Men Etme",
        "place": "Medine", "order": 107, "verses": 12, "juz": "28. Cüz",
        "summary": "Aile içi sırlar ve denge, müminlerin kendilerini ve ailelerini yakıtı insanlar ve taşlar olan ateşten koruma görevi, Hz. Nuh ve Hz. Lut'un inkârcı hanımları ile Firavun'un mümin hanımı Asiye ve Hz. Meryem örnekleri."
    },
    67: {
        "name_tr": "Mülk", "name_ar": "سُورَةُ المُلْكِ", "meaning": "Mülk, Hükümranlık (Tebâreke)",
        "place": "Mekke", "order": 77, "verses": 30, "juz": "29. Cüz",
        "summary": "'Hanginizin daha güzel amel işleyeceğini sınamak için ölümü ve hayatı yaratan O'dur' ayeti, kusursuz gök kubbe düzeni, kabir azabından koruyucu fazileti."
    },
    68: {
        "name_tr": "Kalem", "name_ar": "سُورَةُ القَلَمِ", "meaning": "Kalem (Nûn)",
        "place": "Mekke", "order": 2, "verses": 52, "juz": "29. Cüz",
        "summary": "Kaleme ve satır satır yazılanlara yemin, Hz. Peygamber'in 'yüce bir ahlak üzere' oluşu (4. ayet), yoksulun hakkını vermeyip bahçeleri yanan bahçe sahipleri kıssası ve Hz. Yûnus'un balık karnındaki sabrı."
    },
    69: {
        "name_tr": "Hâkka", "name_ar": "سُورَةُ الحَاقَّةِ", "meaning": "Kaçınılmaz Hakikat (Kıyamet)",
        "place": "Mekke", "order": 78, "verses": 52, "juz": "29. Cüz",
        "summary": "Kıyametin sarsıcı hakikati, Sûr'a tek bir üflenişle dağların un ufak oluşu, amel defterleri sağdan verilenlerin sevinci ile soldan verilenlerin 'Keşke bana kitabım verilmeseydi' feryadı."
    },
    70: {
        "name_tr": "Meâric", "name_ar": "سُورَةُ المَعَارِجِ", "meaning": "Yükselme Dereceleri ve Yolları",
        "place": "Mekke", "order": 79, "verses": 44, "juz": "29. Cüz",
        "summary": "Ellibin yıl sürecek kıyamet günü azabı, insanın sabırsız ve hırslı yaratılışı, namazlarına devam eden ve yoksullara pay ayıran takva ehlinin kurtuluşu."
    },
    71: {
        "name_tr": "Nûh", "name_ar": "سُورَةُ نُوحٍ", "meaning": "Hz. Nûh Peygamber",
        "place": "Mekke", "order": 71, "verses": 28, "juz": "29. Cüz",
        "summary": "Hz. Nuh'un kavmini gece gündüz, açıkça ve gizlice tevhide çağırması; kavminin inatçı direnişi, putperestlikleri (Vedd, Süvâ', Yagûs, Yeûk, Nesr) ve Hz. Nuh'un müminler için bağışlanma duası."
    },
    72: {
        "name_tr": "Cin", "name_ar": "سُورَةُ الجِنِّ", "meaning": "Cin Varlıkları",
        "place": "Mekke", "order": 40, "verses": 28, "juz": "29. Cüz",
        "summary": "Bir grup cinin Kur'an'ı dinleyip hayran kalarak iman etmeleri, gayb ilminin yalnızca Allah'a ait olduğu ve dilediği peygamberine bildirdiği anlatılır."
    },
    73: {
        "name_tr": "Müzzemmil", "name_ar": "سُورَةُ المُزَّمِّلِ", "meaning": "Örtünüp Bürünen (Hz. Peygamber)",
        "place": "Mekke", "order": 3, "verses": 20, "juz": "29. Cüz",
        "summary": "Gece kalkıp Kur'an'ı tertil üzere (ağır ağır, tane tane) okuma emri, gecenin ibadet için derin manevi bereketi ve ağır vahiy yükünü taşımaya ruhi hazırlık."
    },
    74: {
        "name_tr": "Müddessir", "name_ar": "سُورَةُ المُدَّثِّرِ", "meaning": "Örtüsüne Sarınan (Hz. Peygamber)",
        "place": "Mekke", "order": 4, "verses": 56, "juz": "29. Cüz",
        "summary": "'Kalk ve uyar, Rabbini yücelt, elbiseni temiz tut!' emri ile başlayan açık tebliğ dönemi, cehennem bekçisi 19 melek ve 'Sizi Sekar cehennemine ne sürükledi?' sorusuna verilen cevaplar."
    },
    75: {
        "name_tr": "Kıyâme", "name_ar": "سُورَةُ القِيَامَةِ", "meaning": "Kıyamet ve Diriliş Günü",
        "place": "Mekke", "order": 31, "verses": 40, "juz": "29. Cüz",
        "summary": "Kıyamet gününe ve kendini kınayan nefse (levvâme) yemin; parmak uçlarına kadar insanın yeniden yaratılacağı ve can boğaza dayandığı anın çaresizliği."
    },
    76: {
        "name_tr": "İnsân (Dehr)", "name_ar": "سُورَةُ الإِنْسَانِ", "meaning": "İnsan / Zaman",
        "place": "Medine", "order": 98, "verses": 31, "juz": "29. Cüz",
        "summary": "İnsanın henüz anılmaya değer bir şey olmadığı zaman dilimi, yoksulu, yetimi ve esiri sırf Allah rızası için doyuran ebrarın (iyilerin) cennetteki kâfur ve zencefil pınarları."
    },
    77: {
        "name_tr": "Mürselât", "name_ar": "سُورَةُ المُرْسَلَاتِ", "meaning": "Birbiri Ardınca Gönderilenler (Rüzgârlar / Melekler)",
        "place": "Mekke", "order": 33, "verses": 50, "juz": "29. Cüz",
        "summary": "Yeminlerle başlayan kıyamet tasvirleri ve inkârcılar için on defa tekrarlanan 'O gün yalanlayanların vay haline!' uyarısı."
    },
    78: {
        "name_tr": "Nebe'", "name_ar": "سُورَةُ النَّبَإِ", "meaning": "Büyük Haber (Amme)",
        "place": "Mekke", "order": 80, "verses": 40, "juz": "30. Cüz",
        "summary": "30. Cüz'ün başlangıç suresidir. İnsanların tartıştığı büyük haber (kıyamet ve diriliş), dağların kazık kılınışı, Sûr'a üfleniş ve kâfirin 'Keşke toprak olsaydım' diyeceği hesap günü."
    },
    79: {
        "name_tr": "Nâziât", "name_ar": "سُورَةُ النَّازِعَاتِ", "meaning": "Söküp Çıkaranlar (Can Alan Melekler)",
        "place": "Mekke", "order": 81, "verses": 46, "juz": "30. Cüz",
        "summary": "Canları şiddetle veya yumuşaklıkla alan melekler, Hz. Musa ile haddi aşan Firavun'un kıssası ve kıyametin vaktini soranlara karşı onun sadece Allah katında olduğu bildirisi."
    },
    80: {
        "name_tr": "Abese", "name_ar": "سُورَةُ عَبَسَ", "meaning": "Yüzünü Ekşitti",
        "place": "Mekke", "order": 24, "verses": 42, "juz": "30. Cüz",
        "summary": "Hz. Peygamber'in âmâ sahabi İbn Ümmi Mektûm'a karşı tavrından dolayı ilahî ikaza muhatap oluşu, Kur'an'ın şerefli sahifelerde korunduğu ve insanın nankörlüğü."
    },
    81: {
        "name_tr": "Tekvîr", "name_ar": "سُورَةُ التَّكْوِيرِ", "meaning": "Güneşin Dürülmesi",
        "place": "Mekke", "order": 7, "verses": 29, "juz": "30. Cüz",
        "summary": "Güneşin dürülmesi, yıldızların dökülmesi, denizlerin kaynatılması, diri diri gömülen kız çocuğuna hangi suçtan öldürüldüğünün sorulacağı dehşetli kıyamet sahneleri."
    },
    82: {
        "name_tr": "İnfitâr", "name_ar": "سُورَةُ الإِنْفِطَارِ", "meaning": "Göğün Yarılması",
        "place": "Mekke", "order": 82, "verses": 19, "juz": "30. Cüz",
        "summary": "Göğün yarılması, kabirlerin altüst olması, 'Ey insan! Kerîm olan Rabbine karşı seni ne aldattı?' hitabı ve Kirâmen Kâtibîn meleklerinin her şeyi yazması."
    },
    83: {
        "name_tr": "Mutaffifîn", "name_ar": "سُورَةُ المُطَفِّفِينَ", "meaning": "Ölçü ve Tartıda Hile Yapanlar",
        "place": "Mekke", "order": 86, "verses": 36, "juz": "30. Cüz",
        "summary": "Ticarette ve ölçü-tartıda adaletsizlik yapanların acı sonu, kötülük yapanların amel defterinin Siccîn'de, iyilerin defterinin İlliyyîn'de muhafaza edilmesi."
    },
    84: {
        "name_tr": "İnşikâk", "name_ar": "سُورَةُ الإِنْشِقَاقِ", "meaning": "Göğün Yarılıp Parçalanması",
        "place": "Mekke", "order": 83, "verses": 25, "juz": "30. Cüz",
        "summary": "Göğün Rabbine boyun eğerek yarılması, insanın Rabbine doğru adım adım çaba göstermesi ve amel defterini arkasından alanların feryadı."
    },
    85: {
        "name_tr": "Bürûc", "name_ar": "سُورَةُ البُرُوجِ", "meaning": "Burçlar, Takımyıldızları",
        "place": "Mekke", "order": 27, "verses": 22, "juz": "30. Cüz",
        "summary": "Burçlar sahibi göğe yemin, inançları uğruna hendeklere atılıp yakılan Ashâb-ı Uhdûd müminlerinin destansı direnişi ve Levh-i Mahfûz'da korunan Kur'an."
    },
    86: {
        "name_tr": "Târık", "name_ar": "سُورَةُ الطَّارِقِ", "meaning": "Gece Doğan Parlak Yıldız (Delip Geçen Işık)",
        "place": "Mekke", "order": 36, "verses": 17, "juz": "30. Cüz",
        "summary": "Karanlığı delen Târık yıldızı, insanın atılan bir sudan yaratılışı, bütün gizli sırların ortaya döküleceği hesap günü ve Kur'an'ın kesin bir hüküm olduğu."
    },
    87: {
        "name_tr": "A'lâ", "name_ar": "سُورَةُ الأَعْلَى", "meaning": "En Yüce Olan Allah",
        "place": "Mekke", "order": 8, "verses": 19, "juz": "30. Cüz",
        "summary": "Yüce Rabbin ismini tesbih, Kur'an'ın Hz. Peygamber'e unutturulmayacağı vaadi, arınanların kurtuluşu ve bu hakikatlerin Hz. İbrahim ve Musa'nın sahifelerinde de bulunduğu."
    },
    88: {
        "name_tr": "Gâşiye", "name_ar": "سُورَةُ الغَاشِيَةِ", "meaning": "Her Şeyi Kuşatan Kıyamet",
        "place": "Mekke", "order": 68, "verses": 26, "juz": "30. Cüz",
        "summary": "Kıyametin dehşetiyle ezilmiş yüzler ile nimetlerle parıldayan yüzlerin karşılaştırması; devenin, göğün, dağların ve yeryüzünün yaratılışındaki ibretler."
    },
    89: {
        "name_tr": "Fecr", "name_ar": "سُورَةُ الفَجْرِ", "meaning": "Tan Yeri Ağarması, Şafak Vakti",
        "place": "Mekke", "order": 10, "verses": 30, "juz": "30. Cüz",
        "summary": "Fecr vaktine ve on geceye yemin; İrem şehri sütunları, Semûd ve Firavun'un helaki, yetime ikram etmeyenlerin kınanması ve 'Ey mutmain olmuş nefis! Dön Rabbine!' ilahî çağrısı."
    },
    90: {
        "name_tr": "Beled", "name_ar": "سُورَةُ البَلَدِ", "meaning": "Şehir, Belde (Mekke)",
        "place": "Mekke", "order": 35, "verses": 20, "juz": "30. Cüz",
        "summary": "Kutsal şehir Mekke'ye yemin, insanın zorluklar ve çileler içinde yaratılışı; aşılması gereken sarp yokuşun bir köleyi azat etmek ve açlık gününde yetimi doyurmak olduğu."
    },
    91: {
        "name_tr": "Şems", "name_ar": "سُورَةُ الشَّمْسِ", "meaning": "Güneş",
        "place": "Mekke", "order": 26, "verses": 15, "juz": "30. Cüz",
        "summary": "Güneşe, aya, geceye, gündüze ve insana şekil verene peş peşe yapılan on bir yemin; nefsini arındıranın kurtulduğu, onu kötülüğe gömenlerin ise Semûd kavmi gibi helak olduğu."
    },
    92: {
        "name_tr": "Leyl", "name_ar": "سُورَةُ اللَّيْلِ", "meaning": "Gece",
        "place": "Mekke", "order": 9, "verses": 21, "juz": "30. Cüz",
        "summary": "Karanlığıyla bürüyen geceye ve parıldayan gündüze yemin; cömertçe infak edip takvalı olanın işlerinin kolaylaştırılacağı, cimrilik edip kendini müstağni görenin ise hüsrana uğrayacağı."
    },
    93: {
        "name_tr": "Duhâ", "name_ar": "سُورَةُ الضُّحَى", "meaning": "Kuşluk Vakti",
        "place": "Mekke", "order": 11, "verses": 11, "juz": "30. Cüz",
        "summary": "Vahyin bir müddet kesilmesi üzerine inen teselli suresi: 'Rabbin seni terk etmedi ve sana darılmadı', yetimi hor görmeme, isteyeni azarlamama ve Rabbin nimetini şükranla anma."
    },
    94: {
        "name_tr": "İnşirâh", "name_ar": "سُورَةُ الشَّرْحِ", "meaning": "Gönül Ferahlığı, Göğsün Açılması",
        "place": "Mekke", "order": 12, "verses": 8, "juz": "30. Cüz",
        "summary": "Hz. Peygamber'in göğsünün ferahlatılması, belini büken ağır yükün kaldırılması, şanının yüceltilmesi ve 'Şüphesiz her zorlukla beraber bir kolaylık vardır' müjdesi."
    },
    95: {
        "name_tr": "Tîn", "name_ar": "سُورَةُ التِّينِ", "meaning": "İncir Ağacı",
        "place": "Mekke", "order": 28, "verses": 8, "juz": "30. Cüz",
        "summary": "İncire, zeytine, Sina Dağı'na ve emin belde Mekke'ye yemin; insanın 'en güzel surette' (Ahsen-i Takvîm) yaratıldığı, ancak iman edip salih amel işlemeyenlerin aşağıların aşağısına yuvarlanacağı."
    },
    96: {
        "name_tr": "Alak", "name_ar": "سُورَةُ العَلَقِ", "meaning": "Aşılanmış Yumurta, Embriyo",
        "place": "Mekke", "order": 1, "verses": 19, "juz": "30. Cüz",
        "summary": "İlk inen vahiydir. 'Yaratan Rabbinin adıyla oku!', insana bilmediğini kalemle öğreten Allah, insanın kendini zengin görünce azgınlaşması (Ebû Cehil örneği) ve secde ederek yaklaşma emri."
    },
    97: {
        "name_tr": "Kadir", "name_ar": "سُورَةُ القَدْرِ", "meaning": "Kadir Gecesi, Değer ve Hüküm",
        "place": "Mekke", "order": 25, "verses": 5, "juz": "30. Cüz",
        "summary": "Kur'an'ın indirildiği Kadir Gecesi'nin bin aydan daha hayırlı olduğu, meleklerin ve Ruh'un (Cebrail) yeryüzüne inerek fecir vaktine kadar esenlik ve selamet dağıttığı bildirilir."
    },
    98: {
        "name_tr": "Beyyine", "name_ar": "سُورَةُ البَيِّنَةِ", "meaning": "Apaçık Delil, Kesin Belge",
        "place": "Medine", "order": 100, "verses": 8, "juz": "30. Cüz",
        "summary": "Apaçık delil olan Peygamber ve Kur'an, dini yalnızca Allah'a halis kılarak hanifler olarak ibadet etme emri; inkârcıların yaratılmışların en şerlisi, iman edenlerin ise en hayırlısı olduğu."
    },
    99: {
        "name_tr": "Zilzâl", "name_ar": "سُورَةُ الزَّلْزَلَةِ", "meaning": "Büyük Deprem, Sarsıntı",
        "place": "Medine", "order": 93, "verses": 8, "juz": "30. Cüz",
        "summary": "Yerkürenin dehşetle sarsılıp içindeki ağırlıkları dışarı atması, zerre ağırlığınca hayır işleyenin karşılığını göreceği gibi zerre ağırlığınca kötülük işleyenin de karşılığını göreceği."
    },
    100: {
        "name_tr": "Âdiyât", "name_ar": "سُورَةُ العَادِيَاتِ", "meaning": "Soluk Soluğa Koşan Savaş Atları",
        "place": "Mekke", "order": 14, "verses": 11, "juz": "30. Cüz",
        "summary": "Nallarıyla kıvılcımlar saçarak koşan gazilerin atlarına yemin; insanın Rabbine karşı çok nankör olduğu, mala aşırı düşkünlüğü ve kabirdekilerin dışarı döküleceği günün uyarısı."
    },
    101: {
        "name_tr": "Kâria", "name_ar": "سُورَةُ القَارِعَةِ", "meaning": "Kapı Çalan / Çarpan Büyük Felaket",
        "place": "Mekke", "order": 30, "verses": 11, "juz": "30. Cüz",
        "summary": "İnsanların etrafa saçılmış pervaneler, dağların ise atılmış renkli yünler gibi olacağı gün; tartıları ağır gelenlerin hoşnut bir hayatta, hafif gelenlerin ise 'Hâviye' cehenneminde olacağı."
    },
    102: {
        "name_tr": "Tekâsür", "name_ar": "سُورَةُ التَّكَاثُرِ", "meaning": "Çoklukla Övünme Yarışı",
        "place": "Mekke", "order": 16, "verses": 8, "juz": "30. Cüz",
        "summary": "Kabirlere varıncaya kadar süren mal-mülk ve çoklukla övünme hırsı; insanın kesin bir bilgiyle (ilme'l-yakîn) uyarılışı ve 'O gün verilen nimetlerden mutlaka hesaba çekileceksiniz' ikazı."
    },
    103: {
        "name_tr": "Asr", "name_ar": "سُورَةُ العَصْرِ", "meaning": "Asır, Zaman, İkindi Vakti",
        "place": "Mekke", "order": 13, "verses": 3, "juz": "30. Cüz",
        "summary": "İslam'ın kurtuluş formülü: Zamana yemin olsun ki insan hüsrandadır; ancak iman edenler, salih amel işleyenler, birbirine hakkı ve sabrı tavsiye edenler müstesna."
    },
    104: {
        "name_tr": "Hümeze", "name_ar": "سُورَةُ الهُمَزَةِ", "meaning": "Arkadan Çekiştiren, Dedikoducu",
        "place": "Mekke", "order": 32, "verses": 9, "juz": "30. Cüz",
        "summary": "İnsanları arkadan çekiştiren, kaş-göz işaretleriyle alay eden ve malını ebedi sanıp yığanların 'Hutame' (kalplere kadar tırmanan kilitli ateş) ile cezalandırılacağı."
    },
    105: {
        "name_tr": "Fîl", "name_ar": "سُورَةُ الفِيلِ", "meaning": "Fil Hadisesi",
        "place": "Mekke", "order": 19, "verses": 5, "juz": "30. Cüz",
        "summary": "Kâbe'yi yıkmak amacıyla fillerle gelen Ebrehe ordusunun, Ebâbîl kuşlarının attığı pişmiş çamurdan taşlarla çiğnenmiş ekin yaprağına çevrilerek helak edilişi."
    },
    106: {
        "name_tr": "Kureyş", "name_ar": "سُورَةُ قُرَيْشٍ", "meaning": "Kureyş Kabilesi",
        "place": "Mekke", "order": 29, "verses": 4, "juz": "30. Cüz",
        "summary": "Kureyş'e bahşedilen kış ve yaz ticari seyahat güvenliği; onları açlıktan doyuran ve korkudan emin kılan bu Beyt'in (Kâbe'nin) Rabbine kulluk etme çağrısı."
    },
    107: {
        "name_tr": "Mâûn", "name_ar": "سُورَةُ المَاعُونِ", "meaning": "Küçük Bir Yardım, Zekât",
        "place": "Mekke", "order": 17, "verses": 7, "juz": "30. Cüz",
        "summary": "Hesap gününü yalanlayanların yetimi itip kakması, yoksulu doyurmaya önayak olmaması; namazlarından gafil olup gösteriş yapanların ve en küçük yardımı bile engelleyenlerin kınanması."
    },
    108: {
        "name_tr": "Kevser", "name_ar": "سُورَةُ الكَوْثَرِ", "meaning": "Bitmez Tükenmez Nimet, Kevser Havuzu",
        "place": "Mekke", "order": 15, "verses": 3, "juz": "30. Cüz",
        "summary": "Kur'an'ın en kısa suresidir. Hz. Peygamber'e Kevser'in (bütün hayırların ve cennet havuzunun) bahşedildiği, namaz kılıp kurban kesmesi emri ve asıl soyu kesik olanın O'na düşmanlık eden olduğu."
    },
    109: {
        "name_tr": "Kâfirûn", "name_ar": "سُورَةُ الكَافِرُونَ", "meaning": "İnkârcılar",
        "place": "Mekke", "order": 18, "verses": 6, "juz": "30. Cüz",
        "summary": "İnançta tavizsiz duruş ve şirk tekliflerinin kesin reddi: 'De ki: Ey inkârcılar! Ben sizin taptıklarınıza tapmam... Sizin dininiz size, benim dinim banadır.'"
    },
    110: {
        "name_tr": "Nasr", "name_ar": "سُورَةُ النَّصْرِ", "meaning": "Yardım, Zafer (İzâ Câe)",
        "place": "Medine", "order": 114, "verses": 3, "juz": "30. Cüz",
        "summary": "Allah'ın yardımı ve Mekke'nin fethi gerçekleşip insanların bölük bölük Allah'ın dinine girdiği görüldüğünde, Rabbe hamd ile tesbih ve O'ndan bağışlanma dileme emri."
    },
    111: {
        "name_tr": "Tebbet (Mesed)", "name_ar": "سُورَةُ المَسَدِ", "meaning": "Kurumak, Helak Olmak / Bükülmüş İp",
        "place": "Mekke", "order": 6, "verses": 5, "juz": "30. Cüz",
        "summary": "İslam'ın ve Hz. Peygamber'in en azılı düşmanı Ebû Leheb'in iki elinin kuruyup helak oluşu, malının ona fayda vermeyişi ve odun hamalı olan karısının boynundaki liften iple ateşe atılacağı."
    },
    112: {
        "name_tr": "İhlâs", "name_ar": "سُورَةُ الإِخْلَاصِ", "meaning": "Samimiyet, Katıksız Tevhid İnancı",
        "place": "Mekke", "order": 22, "verses": 4, "juz": "30. Cüz",
        "summary": "Tevhid akidesinin en özlü beyanıdır. Kur'an'ın üçte birine denk kabul edilir: 'De ki: O Allah tektir. Allah Samed'dir. O doğurmamış ve doğmamıştır. Hiçbir şey O'na denk değildir.'"
    },
    113: {
        "name_tr": "Felak", "name_ar": "سُورَةُ الفَلَقِ", "meaning": "Sabah Aydınlığı, Şafak",
        "place": "Mekke", "order": 20, "verses": 5, "juz": "30. Cüz",
        "summary": "Muavvizeteyn'in (sığındırıcı iki sure) ilkidir. Yarattığı şeylerin şerrinden, karanlık çöktüğünde gecenin şerrinden, düğümlere üfleyen büyücülerin şerrinden ve haset ettiğinde hasetçinin şerrinden sabahın Rabbine sığınma."
    },
    114: {
        "name_tr": "Nâs", "name_ar": "سُورَةُ النَّاسِ", "meaning": "İnsanlar",
        "place": "Mekke", "order": 21, "verses": 6, "juz": "30. Cüz",
        "summary": "Kur'an'ın hatim suresidir. İnsanların kalplerine sinsi sinsi vesvese veren gerek cinlerden gerek insanlardan bütün şeytanların şerrinden insanların Rabbi, Meliki ve İlahı olan Allah'a sığınma duası."
    }
}

def get_surah_filename(s_num, name_tr):
    clean = name_tr.replace(" ", "_").replace("'", "")
    accents = {
        "â": "a", "î": "i", "û": "u",
        "Â": "A", "Î": "I", "Û": "U",
        "(": "", ")": ""
    }
    for k, v in accents.items():
        clean = clean.replace(k, v)
    return f"{s_num:03d}_{clean}.md"

def fetch_json_with_retry(url, retries=5, delay=2):
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
            with urllib.request.urlopen(req, timeout=40) as resp:
                return json.loads(resp.read().decode('utf-8'))
        except Exception as e:
            print(f"Fetch failed for {url} (attempt {i+1}/{retries}): {e}")
            if i < retries - 1:
                time.sleep(delay * (i + 1))
            else:
                raise e

def clean_arabic_ayah(surah_num, ayah_num, text):
    """
    Surah 2..114 have bismillah prepended in Uthmani dataset for Ayah 1.
    We separate it so ayah 1 contains the actual verse text.
    """
    if surah_num > 1 and surah_num != 9 and ayah_num == 1:
        parts = text.split('ٱلرَّحِيمِ', 1)
        if len(parts) >= 2:
            return parts[1].strip()
    return text.strip()

def build_quran():
    print("Kur'an-ı Kerim verileri indiriliyor...")
    
    # 1. Arabic Uthmani
    print("1. Osmanî Arapça metin çekiliyor (quran-uthmani)...")
    uthmani_data = fetch_json_with_retry('http://api.alquran.cloud/v1/quran/quran-uthmani')['data']['surahs']
    
    # 2. Turkish Transliteration
    print("2. Türkçe Okunuş/Transkripsiyon çekiliyor (tr.transliteration)...")
    trans_data = fetch_json_with_retry('http://api.alquran.cloud/v1/quran/tr.transliteration')['data']['surahs']
    
    # 3. Turkish Translation (Diyanet)
    print("3. Türkçe Meal çekiliyor (tr.vakfi)...")
    diyanet_data = fetch_json_with_retry('http://api.alquran.cloud/v1/quran/tr.vakfi')['data']['surahs']
    
    print("Veri indirme tamamlandı. Dosyalar oluşturuluyor...")
    
    # Clean and recreate sureler dir
    os.makedirs("sureler", exist_ok=True)
    
    total_ayah_count = 0
    
    # Prepare master markdown content
    master_lines = []
    master_lines.append("# Kur'an-ı Kerim ve Yüce Meali\n")
    master_lines.append("> **Orijinal Osmanî Arapça Metin • Türkçe Okunuş • Doğal ve Akıcı Türkçe Meâl • Sure Tanıtımları ve Özeti**\n")
    master_lines.append("---\n")
    
    # Introduction & Foreword
    master_lines.append("## 📖 Takdim ve Metodoloji\n")
    master_lines.append("Bu eser; Yüce Kitabımız **Kur'an-ı Kerim**'in 114 suresini ve 6.236 ayetini eksiksiz olarak ihtiva etmektedir. Her ayet-i kerime için:\n")
    master_lines.append("1. **📜 Orijinal Arapça Metin:** Harekeli Osmanî Mushaf hattı ile yer almaktadır.")
    master_lines.append("2. **🗣️ Türkçe Okunuş:** Arapça telaffuzu kolaylaştıran standart transkripsiyon kurallarıyla sunulmuştur.")
    master_lines.append("3. **🇹🇷 Doğal ve Akıcı Meal:** Diyanet İşleri Başkanlığı'nın onaylı meali ve muteber tefsirler ışığında, Türkçemizin zengin ifade gücüne ve akıcılığına sadık kalınarak hazırlanmıştır.")
    master_lines.append("4. **📑 Sure Bilgileri & Ana Temalar:** Her surenin başında nüzul ortamı, ayet sayısı, cüz bilgisi ve surenin mesajını özetleyen tanıtım metni eklenmiştir.\n")
    master_lines.append("---\n")
    
    # Table of Contents
    master_lines.append("## 📑 İçindekiler Tablosu (Fihrist)\n")
    master_lines.append("| No | Sure Adı | Arapça | Anlamı | İniş Yeri | Nüzul Sırası | Ayet Sayısı | Cüz |")
    master_lines.append("|:---:|:---|:---:|:---|:---:|:---:|:---:|:---:|")
    
    toc_rows = []
    for s_idx in range(114):
        s_num = s_idx + 1
        meta = SURAH_METADATA[s_num]
        anchor_id = f"sure-{s_num:03d}"
        row = f"| {s_num:03d} | [{meta['name_tr']} Suresi](#{anchor_id}) | {meta['name_ar']} | {meta['meaning']} | {meta['place']} | {meta['order']} | {meta['verses']} | {meta['juz']} |"
        master_lines.append(row)
        toc_rows.append((s_num, meta))
    
    master_lines.append("\n---\n")
    
    # Process each surah
    for s_idx in range(114):
        s_num = s_idx + 1
        meta = SURAH_METADATA[s_num]
        
        ar_surah = uthmani_data[s_idx]
        tr_trans_surah = trans_data[s_idx]
        tr_meal_surah = diyanet_data[s_idx]
        
        num_ayahs = len(ar_surah['ayahs'])
        total_ayah_count += num_ayahs
        
        surah_header_title = f"{s_num}. {meta['name_tr']} Suresi ({meta['name_ar']})"
        anchor_id = f"sure-{s_num:03d}"
        clean_file_name = get_surah_filename(s_num, meta['name_tr'])
        
        # Build individual Surah markdown
        surah_lines = []
        surah_lines.append(f"# {surah_header_title}\n")
        surah_lines.append(f"> **Anlamı:** {meta['meaning']}  ")
        surah_lines.append(f"> **İniş Yeri:** {meta['place']} | **Nüzul Sırası:** {meta['order']} | **Ayet Sayısı:** {meta['verses']} | **Cüz:** {meta['juz']}\n")
        surah_lines.append("### 📖 Sure Hakkında")
        surah_lines.append(f"{meta['summary']}\n")
        
        prev_filename = get_surah_filename(s_num - 1, SURAH_METADATA[s_num - 1]['name_tr']) if s_num > 1 else ""
        next_filename = get_surah_filename(s_num + 1, SURAH_METADATA[s_num + 1]['name_tr']) if s_num < 114 else ""
        
        prev_link = f"[← Önceki Sure ({SURAH_METADATA[s_num-1]['name_tr']})]({prev_filename})" if s_num > 1 else ""
        next_link = f"[Sonraki Sure ({SURAH_METADATA[s_num+1]['name_tr']}) →]({next_filename})" if s_num < 114 else ""
        
        nav_items = ["[🏠 Ana Dizin](../README.md)", "[📚 Bütün Sureler (Tek Dosya)](../KURAN-I_KERIM_MEALI.md)"]
        if prev_link: nav_items.append(prev_link)
        if next_link: nav_items.append(next_link)
        nav_line = " | ".join(nav_items)
        
        surah_lines.append(f"\n{nav_line}\n\n---\n")
        
        # Master book header
        master_lines.append(f"<a id=\"{anchor_id}\"></a>")
        master_lines.append(f"# {surah_header_title}\n")
        master_lines.append(f"> **Anlamı:** {meta['meaning']}  ")
        master_lines.append(f"> **İniş Yeri:** {meta['place']} | **Nüzul Sırası:** {meta['order']} | **Ayet Sayısı:** {meta['verses']} | **Cüz:** {meta['juz']}\n")
        master_lines.append("### 📖 Sure Hakkında")
        master_lines.append(f"{meta['summary']}\n")
        master_lines.append("---\n")
        
        # Bismillah for Surahs 2..114 (omit for 9)
        if s_num != 9 and s_num != 1:
            besmele_block = "> ### بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ\n> *Rahmân ve Rahîm olan Allah'ın adıyla.*"
            surah_lines.append(besmele_block + "\n\n---\n")
            master_lines.append(besmele_block + "\n\n---\n")
        elif s_num == 9:
            tevbe_note = "> *Not: Tevbe Suresi'nin başında Besmele bulunmamaktadır.*"
            surah_lines.append(tevbe_note + "\n\n---\n")
            master_lines.append(tevbe_note + "\n\n---\n")
            
        # Add Ayahs
        for a_idx in range(num_ayahs):
            a_num = a_idx + 1
            
            raw_ar = ar_surah['ayahs'][a_idx]['text']
            ar_text = clean_arabic_ayah(s_num, a_num, raw_ar)
            tr_trans = tr_trans_surah['ayahs'][a_idx]['text'].strip()
            tr_meal = tr_meal_surah['ayahs'][a_idx]['text'].strip()
            
            ayah_block = f"""### [{s_num}:{a_num}]
**Arapça:**
> {ar_text}

**Okunuş:**
*{tr_trans}*

**Meal:**
{tr_meal}
"""
            surah_lines.append(ayah_block + "\n---\n")
            master_lines.append(ayah_block + "\n---\n")
            
        surah_lines.append(f"\n{nav_line}\n")
        master_lines.append(f"\n[Başa Dön ↑](#içindekiler-tablosu-fihrist)\n\n---\n")
        
        # Write individual surah file
        surah_file_path = os.path.join("sureler", clean_file_name)
        with open(surah_file_path, "w", encoding="utf-8") as sf:
            sf.write("\n".join(surah_lines))
            
    # Write master book
    print(f"Toplam 114 sure ve {total_ayah_count} ayet işlendi.")
    print("KURAN-I_KERIM_MEALI.md yazılıyor...")
    with open("KURAN-I_KERIM_MEALI.md", "w", encoding="utf-8") as mf:
        mf.write("\n".join(master_lines))
        
    # Write README.md
    print("README.md oluşturuluyor...")
    readme_lines = []
    readme_lines.append("# Kur'an-ı Kerim ve Türkçe Meali (Markdown Külliyatı)\n")
    readme_lines.append("Bu proje, Kur'an-ı Kerim'in 114 suresini orijinal Osmanî Arapça metni, Latin harfli Türkçe okunuşu ve akıcı Türkçe mealiyle sunan kapsamlı bir dijital kütüphanedir.\n")
    readme_lines.append("## 📚 Kitap ve Dosya Yapısı\n")
    readme_lines.append("- 📖 **[KURAN-I_KERIM_MEALI.md](KURAN-I_KERIM_MEALI.md)**: 114 surenin tamamını içeren devasa tek parça başvuru kitabı.")
    readme_lines.append("- 📂 **[sureler/](sureler/)**: Her sureyi ayrı ayrı içeren modüler Markdown dosyaları (114 dosya).\n")
    readme_lines.append("## 📋 Sureler Listesi (Fihrist)\n")
    readme_lines.append("| No | Sure Adı | Arapça | Anlamı | İniş Yeri | Nüzul Sırası | Ayet Sayısı | Cüz | Modüler Dosya |")
    readme_lines.append("|:---:|:---|:---:|:---|:---:|:---:|:---:|:---:|:---|")
    
    for s_num, meta in toc_rows:
        clean_file_name = get_surah_filename(s_num, meta['name_tr'])
        readme_lines.append(f"| {s_num:03d} | **{meta['name_tr']}** | {meta['name_ar']} | {meta['meaning']} | {meta['place']} | {meta['order']} | {meta['verses']} | {meta['juz']} | [📄 Oku](sureler/{clean_file_name}) |")
        
    readme_lines.append("\n---\n")
    readme_lines.append("## 🕋 Cüz Tablosu\n")
    readme_lines.append("| Cüz | Başlangıç Suresi ve Ayeti | Bitiş Suresi ve Ayeti |")
    readme_lines.append("|:---:|:---|:---|")
    readme_lines.append("| **1. Cüz** | 1. Fâtiha 1 | 2. Bakara 141 |")
    readme_lines.append("| **2. Cüz** | 2. Bakara 142 | 2. Bakara 252 |")
    readme_lines.append("| **3. Cüz** | 2. Bakara 253 | 3. Âl-i İmrân 92 |")
    readme_lines.append("| **4. Cüz** | 3. Âl-i İmrân 93 | 4. Nisâ 23 |")
    readme_lines.append("| **5. Cüz** | 4. Nisâ 24 | 4. Nisâ 147 |")
    readme_lines.append("| **6. Cüz** | 4. Nisâ 148 | 5. Mâide 81 |")
    readme_lines.append("| **7. Cüz** | 5. Mâide 82 | 6. En'âm 110 |")
    readme_lines.append("| **8. Cüz** | 6. En'âm 111 | 7. A'râf 87 |")
    readme_lines.append("| **9. Cüz** | 7. A'râf 88 | 8. Enfâl 40 |")
    readme_lines.append("| **10. Cüz** | 8. Enfâl 41 | 9. Tevbe 92 |")
    readme_lines.append("| **11. Cüz** | 9. Tevbe 93 | 11. Hûd 5 |")
    readme_lines.append("| **12. Cüz** | 11. Hûd 6 | 12. Yûsuf 52 |")
    readme_lines.append("| **13. Cüz** | 12. Yûsuf 53 | 14. İbrâhîm 52 |")
    readme_lines.append("| **14. Cüz** | 15. Hicr 1 | 16. Nahl 128 |")
    readme_lines.append("| **15. Cüz** | 17. İsrâ 1 | 18. Kehf 74 |")
    readme_lines.append("| **16. Cüz** | 18. Kehf 75 | 20. Tâhâ 135 |")
    readme_lines.append("| **17. Cüz** | 21. Enbiyâ 1 | 22. Hac 78 |")
    readme_lines.append("| **18. Cüz** | 23. Mü'minûn 1 | 25. Furkân 20 |")
    readme_lines.append("| **19. Cüz** | 25. Furkân 21 | 27. Neml 55 |")
    readme_lines.append("| **20. Cüz** | 27. Neml 56 | 29. Ankebût 45 |")
    readme_lines.append("| **21. Cüz** | 29. Ankebût 46 | 33. Ahzâb 30 |")
    readme_lines.append("| **22. Cüz** | 33. Ahzâb 31 | 36. Yâsîn 27 |")
    readme_lines.append("| **23. Cüz** | 36. Yâsîn 28 | 39. Zümer 31 |")
    readme_lines.append("| **24. Cüz** | 39. Zümer 32 | 41. Fussilet 46 |")
    readme_lines.append("| **25. Cüz** | 41. Fussilet 47 | 45. Câsiye 37 |")
    readme_lines.append("| **26. Cüz** | 46. Ahkâf 1 | 51. Zâriyât 30 |")
    readme_lines.append("| **27. Cüz** | 51. Zâriyât 31 | 57. Hadîd 29 |")
    readme_lines.append("| **28. Cüz** | 58. Mücâdele 1 | 66. Tahrîm 12 |")
    readme_lines.append("| **29. Cüz** | 67. Mülk 1 | 77. Mürselât 50 |")
    readme_lines.append("| **30. Cüz** | 78. Nebe' 1 | 114. Nâs 6 |")
    
    with open("README.md", "w", encoding="utf-8") as rf:
        rf.write("\n".join(readme_lines))
        
    print("Tüm dosyalar başarıyla üretildi!")

if __name__ == "__main__":
    build_quran()
