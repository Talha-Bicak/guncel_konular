from typing import Dict, Any, List, Optional
from models.rag_system import RAGSystem
from services.gemini_service import GeminiService
from models.cag_cache import CAGCache
from utils.text_processor import TextProcessor
from config.settings import settings
import json
from datetime import datetime

class RAREModel:
    def __init__(self):
        self.rag_system = RAGSystem()
        self.gemini_service = GeminiService()
        self.cache = CAGCache()
        self.text_processor = TextProcessor()
    
    def retrieve_and_reason(self, query: str, topic: str = None) -> Dict[str, Any]:
        """Retrieve ve Reasoning aşamalarını birleştir"""
        # 1. Retrieval: İlgili dokümanları al
        context = self.rag_system.get_context_for_query(query, topic)
        
        # 2. Reasoning: Gemini ile analiz yap
        reasoning_prompt = f"""
        Aşağıdaki sorguyu ve müfredat bağlamını analiz et:
        
        Sorgu: {query}
        
        {context}
        
        Bu sorgu ve bağlam için:
        1. Ana konuları belirle
        2. Soru çıkma olasılığını değerlendir (1-10 arası)
        3. Muhtemel soru türlerini listele
        4. Önemli anahtar kelimeleri çıkar
        5. Zorluk seviyesi tahmin et
        
        JSON formatında yanıt ver.
        """
        
        reasoning_result = self.gemini_service.generate_response(reasoning_prompt)
        
        try:
            analysis = json.loads(reasoning_result)
        except:
            analysis = {"error": "Reasoning analizi parse edilemedi"}
        
        return {
            "query": query,
            "retrieved_context": context,
            "reasoning_analysis": analysis,
            "timestamp": datetime.now().isoformat()
        }
    
    def predict_exam_questions(self, exam_type: str = "LGS", subject: str = "Din Kültürü", count: int = 10) -> Dict[str, Any]:
        """Sınav soruları tahmin et"""
        cache_key = {
            "exam_type": exam_type,
            "subject": subject,
            "count": count,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Cache kontrolü
        cached_prediction = self.cache.get_cached_response("rare_prediction", cache_key)
        if cached_prediction:
            return cached_prediction['response']
        
        # Müfredat analizi
        curriculum_analysis = self.analyze_curriculum_trends()
        
        # Yüksek olasılıklı konular
        high_prob_topics = curriculum_analysis.get('high_probability_topics', [])
        
        predicted_questions = []
        
        for topic in high_prob_topics[:count//len(high_prob_topics) if high_prob_topics else 1]:
            # Her konu için RARE pipeline çalıştır
            rare_result = self.retrieve_and_reason(
                f"{topic} konusunda {exam_type} sınavında çıkabilecek sorular",
                topic
            )
            
            # Soru üret
            questions_data = self.gemini_service.generate_questions_with_reasoning(
                rare_result['retrieved_context'],
                topic,
                count // len(high_prob_topics) if high_prob_topics else count
            )
            
            if 'questions' in questions_data:
                for question in questions_data['questions']:
                    question['prediction_confidence'] = rare_result['reasoning_analysis'].get('probability', 0.5)
                    question['rare_analysis'] = rare_result
                
                predicted_questions.extend(questions_data['questions'])
        
        # Sonuçları güven skoruna göre sırala
        predicted_questions.sort(key=lambda x: x.get('prediction_confidence', 0), reverse=True)
        
        result = {
            "exam_type": exam_type,
            "subject": subject,
            "prediction_date": datetime.now().isoformat(),
            "total_predicted_questions": len(predicted_questions),
            "questions": predicted_questions[:count],
            "curriculum_analysis": curriculum_analysis,
            "confidence_threshold": settings.PREDICTION_CONFIDENCE_THRESHOLD
        }
        
        # Cache'le
        self.cache.cache_response("rare_prediction", cache_key, result)
        
        return result
    
    def analyze_curriculum_trends(self) -> Dict[str, Any]:
        """Müfredat trendlerini analiz et"""
        # Tüm dokümanlardan trend analizi
        trends_prompt = """
        LGS Din Kültürü dersi için son yıllarda sıkça çıkan konuları ve gelecek sınavlarda 
        çıkma olasılığı yüksek konuları analiz et. Şu faktörleri göz önünde bulundur:
        
        1. Müfredat değişiklikleri
        2. Toplumsal gündem
        3. Din eğitimindeki güncel yaklaşımlar
        4. Öğrenci zorlanma alanları
        
        Yüksek olasılıklı konuları listele ve her biri için çıkma olasılığı ver (0-1 arası).
        """
        
        analysis_result = self.gemini_service.generate_response(trends_prompt)
        
        try:
            return json.loads(analysis_result)
        except:
            return {
                "high_probability_topics": [
                    "İslam'ın Temel İnançları", "Namaz İbadeti", "Oruç İbadeti",
                    "Hz. Muhammed'in Hayatı", "Ahlaki Değerler", "Din ve Bilim"
                ],
                "confidence_scores": {
                    "İslam'ın Temel İnançları": 0.9,
                    "Namaz İbadeti": 0.8,
                    "Oruç İbadeti": 0.7
                }
            }
    
    def deep_reasoning(self, topic: str, depth: int = None) -> Dict[str, Any]:
        """Derin reasoning analizi"""
        if depth is None:
            depth = settings.REASONING_DEPTH
        
        reasoning_chain = []
        current_query = f"{topic} konusunda detaylı analiz"
        
        for level in range(depth):
            rare_result = self.retrieve_and_reason(current_query, topic)
            reasoning_chain.append({
                "level": level + 1,
                "query": current_query,
                "analysis": rare_result
            })
            
            # Bir sonraki seviye için query oluştur
            if level < depth - 1:
                current_query = f"{topic} konusunun daha derin analizi - seviye {level + 2}"
        
        return {
            "topic": topic,
            "reasoning_depth": depth,
            "reasoning_chain": reasoning_chain,
            "final_insights": self._extract_final_insights(reasoning_chain)
        }
    
    def _extract_final_insights(self, reasoning_chain: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Reasoning zincirinden nihai içgörüleri çıkar"""
        all_analysis = []
        for chain_item in reasoning_chain:
            if 'reasoning_analysis' in chain_item['analysis']:
                all_analysis.append(chain_item['analysis']['reasoning_analysis'])
        
        # Tüm analiz sonuçlarını birleştir
        insight_prompt = f"""
        Aşağıdaki çoklu seviye analiz sonuçlarını birleştir ve nihai içgörüleri çıkar:
        
        {json.dumps(all_analysis, ensure_ascii=False, indent=2)}
        
        En önemli bulgular, tahminler ve öneriler neler?
        """
        
        final_insights = self.gemini_service.generate_response(insight_prompt)
        
        try:
            return json.loads(final_insights)
        except:
            return {"insights": final_insights}