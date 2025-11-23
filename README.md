#  LGS Soru Tahmin Sistemi Projesi README

##  Proje Amacı
Bu projenin temel amacı, **LGS (Liselere Geçiş Sistemi) tarzı sınav sorularını tahmin edebilen ve üretebilen** bir yapay zeka sistemi geliştirmektir. Sistem, öğrencilerin başarılarını artırmalarına ve öğretmenlerin materyal hazırlamalarına destek olmayı hedeflemektedir.

##  Sistem Mimarisi: RAG-CAG-RARE

Projemiz, güncel Doğal Dil İşleme (NLP) teknolojilerinin en güçlü bileşenlerini bir araya getiren hibrit bir mimari kullanmaktadır.

| Mimarinin Adı | Açıklama |
| :--- | :--- |
| **RAG (Retrieval-Augmented Generation)** | Geleneksel olarak, sistemin genel müfredat ve ders notları gibi **statik verilerden** bilgi çekmesini ve buna dayalı cevap/tahmin üretmesini sağlar. |
| **CAG (Context-Augmented Generation)** | Projenin özgün yanlarından biri olan CAG, sistemin **geçmiş LGS veya benzeri sınav sorularının semantik formatını** ve bağlamını analiz ederek, tahmini daha güncel ve bağlamsal hale getirmesini sağlar. |
| **RARE (Reasoning & Analysis for Response Extraction)** | Nihai aşamada, Gemini 2.5 Pro gibi güçlü bir **LLM'nin (Büyük Dil Modeli)** devreye girdiği kısımdır. Bu aşamada, RAG ve CAG'den gelen çıktılar **Analiz** edilir ve **Reasoning (Muhakeme)** ile işlenerek, en doğru ve mantıklı soru tahmini (`ÇIKTI`) oluşturulur. |

![LGS Soru Tahmin Sisteminin RAG, CAG ve RARE Bileşenlerini Gösteren Akış Şeması](Ekran%20görüntüsü%202025-11-21%20124704.png)

---

##  Proje Ekibi (16 Kişi)

Projemiz, toplam **16 kişilik** büyük ve dinamik bir ekip tarafından yürütülmektedir. Ekip üyeleri, scrum benzeri çalışma prensipleriyle belirlenen uzmanlık gruplarına ayrılmıştır.

| Araştırma Konusu | Ekip Üyeleri |
| :--- | :--- |
| **SWOT Analizi** | Zeliha Orhan, Ayten Ülkünur Karaoğlan |
| **SMART Kazanımlar** | Berkan Bağıt, Yaşar Görmez |
| **Ders Tercihi** | Ahmet Mert Şengöl, Enes Kaan Dede |
| **Müşteri Analizi** | Mustafa Oğuzhan Örs, Barış Yavuzarslan |
| **Altyapı Araştırması (RAG, CAG, RARE, Fine-Tuning)** | Muhammet Talha Bıçak, Muhammed Yusuf Karaman |
| **Veri Toplama ve Veri İşleme** | Elif Esra Tanış, Emine Göçer |
| **LGS Sorularının Semantik Format Analizi** | Mustafa Utku Akbay, Ethem Merç |
| **LLM Performans Karşılaştırması** | İsmail Mete Karasubaşı |
| **Caching Yöntemlerinin Araştırılması** | Muhammed Güneş |

---

## 📅 Proje İlerleme Durumu

Proje, belirlenen kilometre taşlarına uygun ve planlandığı gibi ilerlemektedir. **Tahmin edilen yolda ilerlemekte olup, çözülmesi gereken problemler planlandığı gibi çözülmüştür.**

### 📌 Toplantılar ve Ana Gelişmeler

* **25 Ekim: 1. Toplantı**
    * Projenin başlangıcı yapıldı, araştırma konuları tanımlandı ve **scrum benzeri grupların** oluşturulması tamamlandı.
* **1 Kasım: 2. Toplantı**
    * İlk araştırmalar ışığında, projenin **ana mimarisi belirlendi**.
    * Araştırmalar sonrası **somut yapılar** ortaya çıktı.
* **9 Kasım: 3. Toplantı**
    * İlerlemeler tartışıldı, **genel bir sıkıntı olmadığı** teyit edildi.
* **29 Kasım: Planlanan 4. Toplantı (İleriye Dönük Adım) 🛠️**
    * Tüm grupların geliştirdiği yapılar **birleştirilerek testler yapılacak**.
    * Sistemin performansındaki **eksikler ve gereksinimler tespit edilmeye çalışılacaktır**.

***

## 🚀 Sonraki Adımlar
Araştırma sonuçlarının uygulamaya geçirilmesi ve RAG-CAG bileşenlerinin ilk prototiplerinin oluşturulması planlanmaktadır.





Data source = https://drive.google.com/file/d/1Bbt8iFQPTATmCq5pcUaNT21SMD1jyJKx/view?usp=sharing
