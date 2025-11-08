from typing import Dict, Any, List, Optional
from models.rare_model import RAREModel
from data.curriculum_loader import CurriculumLoader
from models.cag_cache import CAGCache
import json
from datetime import datetime

class PredictionService:
    def __init__(self):
        self.rare_model = RAREModel()
        self.curriculum_loader = CurriculumLoader()
        self.cache = CAGCache()
        
        # Müfredatı yükle
        self._load_curriculum()
    
    def _load_curriculum(self):
        """Müfredatı RAG sistemine yükle"""
        curriculum_data = self.curriculum_loader.load_din_kulturu_curriculum()
        self.rare_model.rag_system.add_documents(curriculum_data)
    
    def predict_next_exam_questions(self, 
                                  exam_date: str = None, 
                                  question_count: int = 20,
                                  difficulty_filter: str = None,
                                  topic_filter: str = None) -> Dict[str, Any]:
        """Bir sonraki sınav için soru tahmini yap"""
        
        cache_key = {
            "exam_date": exam_date,
            "question_count": question_count, 
            "difficulty_filter": difficulty_filter,
            "topic_filter": topic_filter,
            "prediction_date": datetime.now().strftime("%Y-%m-%d")
        }
        
        # Cache kontrolü
        cached_result = self.cache.get_cached_response("prediction_service", cache_key)
        if cached_result:
            return cached_result['response']
        
        # RARE modeli ile tahmin
        prediction_result = self.rare_model.predict_exam_questions(
            exam_type="LGS",
            subject="Din Kültürü", 
            count=question_count
        )
        
        # Filtreleme uygula
        filtered_questions = self._apply_filters(
            prediction_result['questions'],
            difficulty_filter,
            topic_filter
        )
        
        # Sonuçları düzenle
        final_result = {
            "prediction_metadata": {
                "exam_type": "LGS",
                "subject": "Din Kültürü",
                "prediction_date": datetime.now().isoformat(),
                "target_exam_date": exam_date,
                "total_questions_predicted": len(filtered_questions),
                "filters_applied": {
                    "difficulty": difficulty_filter,
                    "topic": topic_filter
                }
            },
            "predicted_questions": filtered_questions[:question_count],
            "topic_distribution": self._calculate_topic_distribution(filtered_questions),
            "difficulty_distribution": self._calculate_difficulty_distribution(filtered_questions),
            "confidence_analysis": self._analyze_confidence_scores(filtered_questions),
            "curriculum_coverage": self._analyze_curriculum_coverage(filtered_questions)
        }
        
        # Cache'le
        self.cache.cache_response("prediction_service", cache_key, final_result)
        
        return final_result
    
    def _apply_filters(self, questions: List[Dict[str, Any]], 
                      difficulty_filter: str = None,
                      topic_filter: str = None) -> List[Dict[str, Any]]:
        """Sorulara filtre uygula"""
        filtered = questions.copy()
        
        if difficulty_filter:
            filtered = [q for q in filtered if q.get('difficulty') == difficulty_filter]
        
        if topic_filter:
            filtered = [q for q in filtered if topic_filter.lower() in q.get('topic', '').lower()]
        
        return filtered
    
    def _calculate_topic_distribution(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Konu dağılımını hesapla"""
        topic_counts = {}
        for question in questions:
            topic = question.get('topic', 'Bilinmeyen')
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        total = len(questions)
        topic_percentages = {topic: (count/total)*100 for topic, count in topic_counts.items()}
        
        return {
            "counts": topic_counts,
            "percentages": topic_percentages,
            "most_frequent_topic": max(topic_counts.items(), key=lambda x: x[1])[0] if topic_counts else None
        }
    
    def _calculate_difficulty_distribution(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Zorluk dağılımını hesapla"""
        difficulty_counts = {"kolay": 0, "orta": 0, "zor": 0}
        
        for question in questions:
            difficulty = question.get('difficulty', 'orta')
            if difficulty in difficulty_counts:
                difficulty_counts[difficulty] += 1
        
        total = len(questions)
        difficulty_percentages = {diff: (count/total)*100 for diff, count in difficulty_counts.items()}
        
        return {
            "counts": difficulty_counts,
            "percentages": difficulty_percentages
        }
    
    def _analyze_confidence_scores(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Güven skorlarını analiz et"""
        confidence_scores = [q.get('prediction_confidence', 0.5) for q in questions]
        
        if not confidence_scores:
            return {"error": "Güven skorları bulunamadı"}
        
        return {
            "average_confidence": sum(confidence_scores) / len(confidence_scores),
            "min_confidence": min(confidence_scores),
            "max_confidence": max(confidence_scores),
            "high_confidence_count": len([s for s in confidence_scores if s >= 0.8]),
            "medium_confidence_count": len([s for s in confidence_scores if 0.5 <= s < 0.8]),
            "low_confidence_count": len([s for s in confidence_scores if s < 0.5])
        }
    
    def _analyze_curriculum_coverage(self, questions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Müfredat kapsamını analiz et"""
        curriculum_topics = [
            "İslam'ın Temel İnançları", "İbadetler", "Hz. Muhammed'in Hayatı",
            "Ahlaki Değerler", "Din ve Bilim", "Kur'an-ı Kerim", "Hadis-i Şerifler"
        ]
        
        covered_topics = set()
        for question in questions:
            topic = question.get('topic')
            if topic:
                covered_topics.add(topic)
        
        coverage_percentage = (len(covered_topics) / len(curriculum_topics)) * 100
        
        return {
            "total_curriculum_topics": len(curriculum_topics),
            "covered_topics": list(covered_topics),
            "uncovered_topics": [t for t in curriculum_topics if t not in covered_topics],
            "coverage_percentage": coverage_percentage
        }
    
    def get_topic_specific_prediction(self, topic: str, depth: int = 2) -> Dict[str, Any]:
        """Belirli bir konu için detaylı tahmin"""
        deep_analysis = self.rare_model.deep_reasoning(topic, depth)
        
        # Konuya özel sorular üret
        context = self.rare_model.rag_system.get_context_for_query(f"{topic} soruları", topic)
        topic_questions = self.rare_model.gemini_service.generate_questions_with_reasoning(
            context, topic, 10
        )
        
        return {
            "topic": topic,
            "deep_analysis": deep_analysis,
            "generated_questions": topic_questions,
            "prediction_timestamp": datetime.now().isoformat()
        }