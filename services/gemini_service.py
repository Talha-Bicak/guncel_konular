import google.generativeai as genai
from typing import Dict, Any, List, Optional
from config.settings import settings
from models.cag_cache import CAGCache
import json

class GeminiService:
    def __init__(self):
        if not settings.GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY environment variable is required")
        
        genai.configure(api_key=settings.GOOGLE_API_KEY)
        self.model = genai.GenerativeModel(settings.GEMINI_MODEL)
        self.cache = CAGCache()
    
    def generate_response(self, prompt: str, use_cache: bool = True) -> str:
        """Gemini'den yanıt al"""
        cache_key = {"prompt": prompt, "model": settings.GEMINI_MODEL}
        
        # Cache kontrolü
        if use_cache:
            cached_response = self.cache.get_cached_response("gemini", cache_key)
            if cached_response:
                return cached_response['response']['text']
        
        try:
            response = self.model.generate_content(prompt)
            response_text = response.text
            
            # Cache'le
            if use_cache:
                self.cache.cache_response("gemini", cache_key, {"text": response_text})
            
            return response_text
        
        except Exception as e:
            print(f"Gemini API hatası: {e}")
            return "Üzgünüm, şu anda yanıt üretemiyorum."
    
    def analyze_curriculum_pattern(self, curriculum_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Müfredat desenlerini analiz et"""
        prompt = f"""
        Aşağıdaki LGS Din Kültürü müfredat verilerini analiz et ve soru çıkma olasılığı yüksek konuları belirle:
        
        Müfredat Verileri:
        {json.dumps(curriculum_data, ensure_ascii=False, indent=2)}
        
        Lütfen şunları analiz et:
        1. En sık tekrar eden konular
        2. Önceki sınavlarda sıkça çıkan konu türleri
        3. Öğrencilerin zorlandığı konular
        4. Güncel müfredattaki değişiklikler
        
        JSON formatında yanıt ver:
        {{
            "high_probability_topics": [...],
            "difficulty_levels": {{...}},
            "question_types": [...],
            "reasoning": "..."
        }}
        """
        
        response = self.generate_response(prompt)
        try:
            return json.loads(response)
        except:
            return {"error": "Analiz yanıtı parse edilemedi", "raw_response": response}
    
    def generate_questions_with_reasoning(self, context: str, topic: str, count: int = 5) -> List[Dict[str, Any]]:
        """Reasoning ile soru üret"""
        prompt = f"""
        Sen LGS Din Kültürü uzmanısın. Aşağıdaki bağlamı kullanarak {topic} konusunda {count} adet soru üret.
        
        Bağlam:
        {context}
        
        Her soru için:
        1. LGS formatına uygun 4 şıklı soru oluştur
        2. Doğru cevabı belirle
        3. Sorunun zorluk seviyesini değerlendir
        4. Neden bu sorunun çıkabileceğini açıkla (reasoning)
        
        JSON formatında yanıt ver:
        {{
            "questions": [
                {{
                    "question": "Soru metni",
                    "options": {{
                        "A": "Şık A",
                        "B": "Şık B", 
                        "C": "Şık C",
                        "D": "Şık D"
                    }},
                    "correct_answer": "A",
                    "difficulty": "kolay|orta|zor",
                    "reasoning": "Bu sorunun çıkma nedeni...",
                    "topic": "{topic}",
                    "subtopic": "alt konu",
                    "keywords": ["anahtar", "kelimeler"]
                }}
            ]
        }}
        """
        
        response = self.generate_response(prompt)
        try:
            return json.loads(response)
        except:
            return {"error": "Soru üretimi başarısız", "raw_response": response}