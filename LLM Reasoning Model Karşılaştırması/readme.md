# 🧠 LGS Soru Tahmin Platformu - AI Model Araştırması

![Project Status](https://img.shields.io/badge/Status-Research_Complete-success)
![AI Model](https://img.shields.io/badge/Selected_Model-Gemini_2.5_Pro-blue)
![Focus](https://img.shields.io/badge/Focus-Reasoning_%26_Analysis-orange)
![Subject](https://img.shields.io/badge/Subject-Din_Kültürü-green)

> **Ders:** Yazılım Mühendisliğinde Güncel Konular  
> **Araştırmacı:** İsmail Mete Karasubaşı  
> **Proje Rolü:** AI Model Research & Theoretical Architecture (Yapay Zeka Model Araştırması)

## 📖 Proje Hakkında

Bu dokümantasyon, LGS (Liselere Geçiş Sistemi) kapsamında öğrencilere sınav sorularını tahmin eden ve analiz sunan bir yapay zeka platformunun **teknik altyapı araştırma süreçlerini** içerir.

Bu araştırma, özellikle **Din Kültürü ve Ahlak Bilgisi** dersinin gerektirdiği semantik derinlik, senaryo yorumlama ve tarihsel trend takibi yeteneklerini karşılayacak en uygun LLM'in (Büyük Dil Modeli) seçilmesi üzerine odaklanmıştır.

## 🎯 Problem Tanımı

LGS soruları, son yıllarda yapılan müfredat değişiklikleriyle birlikte "bilgi/ezber" odaklı yapıdan uzaklaşarak **"muhakeme ve akıl yürütme"** odaklı bir yapıya evrilmiştir. Standart LLM'ler (GPT-3.5 vb.) genellikle metin tamamlama üzerine kurulu oldukları için şu sorunları yaşamaktadır:

1.  **Bağlam Kopukluğu:** 10 yıllık sınav arşivini ve tüm müfredatı aynı anda hafızada tutamama.
2.  **Yüzeysel Çıkarım:** "Kader" kavramını sözlük anlamıyla bilip, bir senaryo içindeki ince nüansını (örn: Tevekkül ile ayrımı) yapamama.
3.  **Halüsinasyon:** Var olmayan dini metin veya kural uydurma riski.

## 🏆 Seçilen Model: Gemini 2.5 Pro

Yapılan teknik kıyaslamalar ve benchmark analizleri sonucunda, projenin "Akıl Yürütme Motoru" (RARE Katmanı) için **Google Gemini 2.5 Pro** modeli seçilmiştir.

### Neden Gemini 2.5 Pro?

| Özellik | Açıklama ve Projeye Katkısı |
| :--- | :--- |
| **🧠 Thinking Process** | Model, yanıt üretmeden önce dahili bir "düşünme süreci" çalıştırır. LGS sorularındaki karmaşık neden-sonuç ilişkilerini (Chain of Thought) kurmak için kritiktir. |
| **📚 1M+ Token Bağlam** | **Oyun Değiştirici Özellik.** Tüm MEB kitaplarını, son 10 yılın LGS sorularını ve örnek soruları *tek seferde* modele yüklememizi sağlar. Veri bölünmediği için "büyük resmi" ve trendleri görür. |
| **👁️ Native Multimodal** | Sorulardaki harita, grafik ve infografikleri OCR kullanmadan, doğrudan görsel olarak işleyip metinle ilişkilendirebilir. |
| **📈 SOTA Performans** | *Humanity's Last Exam (HLE)* ve *GPQA* testlerinde uzman seviyesinde akıl yürütme başarısı kanıtlanmıştır. |

---

## ⚔️ Model Karşılaştırması ve Rakipler

Araştırma sürecinde Gemini 2.5 Pro, endüstri standardı diğer modellerle kıyaslanmış ve aşağıdaki nedenlerle tercih edilmiştir:

### ❌ GPT-4o (OpenAI) Neden Seçilmedi?
* **Bağlam Kısıtı:** ~128k token sınırı, tüm sınav arşivini ve kitapları aynı anda yüklemeye yetmemektedir. Veriyi parçalamak (chunking) ise yıllar arası trend analizini imkansız kılar.
* **Yüzeysel Akıl Yürütme:** Hızlı yanıt verme eğilimi, Din Kültürü sorularındaki derin felsefi ayrımları bazen kaçırmasına neden olmaktadır.

### ❌ Claude 3.5 Sonnet (Anthropic) Neden Seçilmedi?
* **Aşırı Güvenlik (Over-Refusal):** Dini metinler (Ayet/Hadis) içeren analizlerde, modelin "hassas içerik" uyarısı vererek yanıtı reddetme riski yüksektir. Otomasyon için risklidir.
* **Görsel İşleme:** Multimodal yetenekleri Gemini 2.5 Pro kadar entegre ve hızlı değildir.

