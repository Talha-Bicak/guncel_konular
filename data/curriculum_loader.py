from typing import Dict, List, Any
import json
from utils.text_processor import TextProcessor

class CurriculumLoader:
    def __init__(self):
        self.text_processor = TextProcessor()
        
    def load_din_kulturu_curriculum(self) -> List[Dict[str, Any]]:
        """Din Kültürü müfredatını yükle"""
        
        # LGS Din Kültürü Müfredatı - Ana Konular
        curriculum_data = [
            {
                "topic": "İslam'ın Temel İnançları",
                "subtopic": "Tevhid İnancı",
                "content": """
                Tevhid, İslam dininin temel inancıdır. Allah'ın birliğini, eşsizliğini ve her şeyden münezzeh oluşunu ifade eder. 
                Tevhid inancı şu unsurları içerir: Allah'ın varlığına iman, O'nun birliğine iman, sıfatlarına iman.
                Şirk, tevhidin karşıtıdır ve Allah'a ortak koşmak anlamına gelir.
                """,
                "difficulty": "orta",
                "keywords": ["tevhid", "allah", "birlik", "şirk", "iman"],
                "source": "MEB Müfredatı"
            },
            {
                "topic": "İslam'ın Temel İnançları", 
                "subtopic": "Ahiret İnancı",
                "content": """
                Ahiret inancı, ölümden sonraki hayata iman etmeyi içerir. Bu inanç şunları kapsar:
                Ölüm, kabir hayatı, kıyamet, hesap, mizan, cennet ve cehennem.
                Ahiret inancı insanın dünyevi yaşamında sorumluluk bilincini geliştirir.
                """,
                "difficulty": "orta",
                "keywords": ["ahiret", "kıyamet", "cennet", "cehennem", "kabir"],
                "source": "MEB Müfredatı"
            },
            {
                "topic": "İbadetler",
                "subtopic": "Namaz İbadeti", 
                "content": """
                Namaz, İslam'ın beş temel rüknünden biridir. Günde beş vakit kılınan namazlar:
                Sabah, öğle, ikindi, akşam ve yatsı namazları.
                Namazın farzları: 4 rükün, 12 farz, sünnet ve müstehap kısımları vardır.
                Namaz Allah'la kulun arasında manevi bir bağ kurar.
                """,
                "difficulty": "kolay",
                "keywords": ["namaz", "ibadet", "farz", "sünnet", "rükün"],
                "source": "MEB Müfredatı"
            },
            {
                "topic": "İbadetler",
                "subtopic": "Oruç İbadeti",
                "content": """
                Oruç, Ramazan ayında tutulan önemli bir ibadettir. 
                Oruç tutan kişi gün doğumundan gün batımına kadar yemez, içmez.
                Orucun faydaları: Nefsi terbiye, empati geliştirme, sağlık yararları.
                Orucu bozan durumlar ve mazeret halleri bulunmaktadır.
                """,
                "difficulty": "kolay",
                "keywords": ["oruç", "ramazan", "nefis", "terbiye", "empati"],
                "source": "MEB Müfredatı"
            },
            {
                "topic": "İbadetler",
                "subtopic": "Zekât İbadeti",
                "content": """
                Zekât, belirli miktarda mala sahip olan müslümanların vermesi gereken zorunlu bağıştır.
                Zekât, toplumsal dayanışmayı sağlar ve gelir adaletsizliğini azaltır.
                Zekât verilecek mallar: altın, gümüş, para, ticaret malları, hayvanlar, tarım ürünleri.
                Zekât alan kişiler Kur'an'da belirtilmiştir.
                """,
                "difficulty": "orta",
                "keywords": ["zekât", "dayanışma", "adalet", "mal", "fıtır"],
                "source": "MEB Müfredatı"
            },
            {
                "topic": "Hz. Muhammed'in Hayatı",
                "subtopic": "Doğumu ve Çocukluk Dönemi",
                "content": """
                Hz. Muhammed 570 yılında Mekke'de doğdu. Babası Abdullah, annesi Amine'dir.
                Küçük yaşta yetim kaldı. Önce dedesi Abdülmuttalib, sonra amcası Ebu Talib tarafından büyütüldü.
                Çocukluktan itibaren dürüstlüğü ve güvenilirliğiyle tanındı. 'Emin' lakabını aldı.
                """,
                "difficulty": "kolay", 
                "keywords": ["hz muhammed", "mekke", "abdullah", "amine", "emin"],
                "source": "MEB Müfredatı"
            },
            {
                "topic": "Hz. Muhammed'in Hayatı",
                "subtopic": "Peygamber Oluşu",
                "content": """
                Hz. Muhammed 40 yaşında Hira Mağarası'nda ilk vahyi aldı.
                İlk inen ayet 'İkra' (Oku) ayetidir. İlk müslüman olan Hz. Hatice'dir.
                Peygamberlik görevini önce gizli, sonra açık olarak yürüttü.
                Mekke'de karşılaştığı zorluklar nedeniyle Medine'ye hicret etti.
                """,
                "difficulty": "orta",
                "keywords": ["hira", "vahiy", "ikra", "hatice", "hicret"],
                "source": "MEB Müfredatı"
            },
            {
                "topic": "Ahlaki Değerler",
                "subtopic": "Dürüstlük",
                "content": """
                Dürüstlük, İslam ahlakının temel değerlerinden biridir.
                Söz, davranış ve ticarette doğru olmayı gerektirir.
                Hz. Peygamber'in 'Emin' lakabı dürüstlüğünün kanıtıdır.
                Yalan söylemek, aldatmak dürüstlüğün karşıtıdır.
                """,
                "difficulty": "kolay",
                "keywords": ["dürüstlük", "doğruluk", "emanet", "yalan", "ahlak"],
                "source": "MEB Müfredatı"
            },
            {
                "topic": "Ahlaki Değerler", 
                "subtopic": "Adalet",
                "content": """
                Adalet, hakkı hak sahibine vermek, kimseye haksızlık yapmamaktır.
                İslam'da adalet evrensel bir değerdir. Allah'ın da adalet sıfatı vardır.
                Adalet sadece hukuki değil, sosyal ve ekonomik alanlarda da gereklidir.
                Adaletsizlik toplumsal bozulmanın en önemli nedenlerindendir.
                """,
                "difficulty": "orta", 
                "keywords": ["adalet", "hak", "hakkaniyet", "eşitlik", "zulüm"],
                "source": "MEB Müfredatı"
            },
            {
                "topic": "Din ve Bilim",
                "subtopic": "İslam'da Bilimin Yeri",
                "content": """
                İslam dini bilim öğrenmeyi teşvik eder. Kur'an'ın ilk emri 'oku'dur.
                İslam medeniyeti bilim ve teknolojide önemli katkılar yapmıştır.
                İslam alimleri matematik, tıp, astronomi, kimya gibi alanlarda çalışmışlardır.
                Din ve bilim arasında çelişki değil, uyum vardır.
                """,
                "difficulty": "orta",
                "keywords": ["bilim", "okumak", "araştırma", "medeniyet", "uyum"],
                "source": "MEB Müfredatı"
            },
            {
                "topic": "Kur'an-ı Kerim",
                "subtopic": "Kur'an'ın Özellikleri", 
                "content": """
                Kur'an-ı Kerim, İslam'ın kutsal kitabıdır. Hz. Muhammed'e vahyedilmiştir.
                114 sure ve yaklaşık 6236 ayetten oluşur. Arapça indirilmiştir.
                Kur'an'ın dili edebî açıdan mükemmeldir. Hiç değiştirilmemiştir.
                İnsanlığa rehberlik eden evrensel mesajlar içerir.
                """,
                "difficulty": "orta",
                "keywords": ["kuran", "vahiy", "sure", "ayet", "rehberlik"],
                "source": "MEB Müfredatı"
            },
            {
                "topic": "Hadis-i Şerifler",
                "subtopic": "Hadislerin Önemi",
                "content": """
                Hadis, Hz. Peygamber'in söz, fiil ve tasviplerini içerir.
                Hadisler Kur'an'ı açıklayıcı niteliktedir. İslam hukukunun kaynağıdır.
                Sahih, hasen ve zayıf hadis türleri vardır.
                Hadislerin toplanması ve yazılması İslam tarihinde önemli çalışmalardır.
                """,
                "difficulty": "zor",
                "keywords": ["hadis", "sünnet", "sahih", "rivayet", "açıklama"],
                "source": "MEB Müfredatı"
            }
        ]
        
        # Her dokümana anahtar kelimeler ve işlenmiş metin ekle
        processed_documents = []
        for doc in curriculum_data:
            processed_doc = doc.copy()
            
            # Metni temizle
            cleaned_text = self.text_processor.clean_text(doc['content'])
            processed_doc['content'] = cleaned_text
            
            # Otomatik anahtar kelime çıkarma
            auto_keywords = self.text_processor.extract_keywords(cleaned_text)
            processed_doc['auto_keywords'] = auto_keywords
            
            # Mevcut anahtar kelimelerle birleştir
            all_keywords = list(set(doc.get('keywords', []) + auto_keywords))
            processed_doc['all_keywords'] = all_keywords
            
            processed_documents.append(processed_doc)
        
        return processed_documents
    
    def load_sample_questions(self) -> List[Dict[str, Any]]:
        """Örnek LGS soruları yükle"""
        sample_questions = [
            {
                "question": "İslam dininin temel inancı olan Tevhid'in anlamı nedir?",
                "options": {
                    "A": "Allah'ın birliğine inanmak",
                    "B": "Peygamberlere inanmak", 
                    "C": "Ahirete inanmak",
                    "D": "Meleklere inanmak"
                },
                "correct_answer": "A",
                "difficulty": "kolay",
                "topic": "İslam'ın Temel İnançları",
                "subtopic": "Tevhid İnancı",
                "explanation": "Tevhid, Allah'ın birliğine ve eşsizliğine iman etmek anlamına gelir."
            },
            {
                "question": "Aşağıdakilerden hangisi günlük namazlardan biri değildir?",
                "options": {
                    "A": "Sabah namazı",
                    "B": "Cuma namazı",
                    "C": "İkindi namazı", 
                    "D": "Yatsı namazı"
                },
                "correct_answer": "B",
                "difficulty": "kolay",
                "topic": "İbadetler",
                "subtopic": "Namaz İbadeti",
                "explanation": "Cuma namazı haftalık kılınan bir namazdır, günlük beş vakit namaza dahil değildir."
            },
            {
                "question": "Hz. Peygamber'e verilen 'Emin' lakabının nedeni nedir?", 
                "options": {
                    "A": "Cesur olması",
                    "B": "Güçlü olması",
                    "C": "Güvenilir ve dürüst olması",
                    "D": "Zengin olması"
                },
                "correct_answer": "C", 
                "difficulty": "kolay",
                "topic": "Hz. Muhammed'in Hayatı",
                "subtopic": "Doğumu ve Çocukluk Dönemi",
                "explanation": "Hz. Peygamber dürüstlüğü ve güvenilirliği nedeniyle 'Emin' lakabını almıştır."
            }
        ]
        
        return sample_questions