from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn
from datetime import datetime

from services.prediction_service import PredictionService
from models.rare_model import RAREModel
from data.curriculum_loader import CurriculumLoader
from config.settings import settings

# FastAPI uygulaması
app = FastAPI(
    title="LGS Din Kültürü Soru Tahmin Sistemi",
    description="RARE mimarisi kullanarak LGS Din Kültürü sorularını tahmin eden sistem",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global servis instance'ları
prediction_service = PredictionService()
rare_model = RAREModel()
curriculum_loader = CurriculumLoader()

# Pydantic modelleri
class PredictionRequest(BaseModel):
    exam_date: Optional[str] = None
    question_count: int = 20
    difficulty_filter: Optional[str] = None
    topic_filter: Optional[str] = None

class TopicAnalysisRequest(BaseModel):
    topic: str
    depth: int = 2

class QuestionGenerationRequest(BaseModel):
    topic: str
    count: int = 5
    difficulty: Optional[str] = None

# API Endpoints
@app.get("/")
async def root():
    """Ana endpoint - sistem bilgileri"""
    return {
        "message": "LGS Din Kültürü Soru Tahmin Sistemi",
        "version": "1.0.0",
        "architecture": "RARE (Retrieval-Augmented Reasoning Engine)",
        "features": ["RAG", "CAG Cache", "Gemini Reasoning"],
        "timestamp": datetime.now().isoformat()
    }

@app.post("/predict/exam-questions")
async def predict_exam_questions(request: PredictionRequest):
    """Sınav soruları tahmin et"""
    try:
        result = prediction_service.predict_next_exam_questions(
            exam_date=request.exam_date,
            question_count=request.question_count,
            difficulty_filter=request.difficulty_filter,
            topic_filter=request.topic_filter
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/topic")
async def analyze_topic(request: TopicAnalysisRequest):
    """Belirli bir konuyu detaylı analiz et"""
    try:
        result = prediction_service.get_topic_specific_prediction(
            topic=request.topic,
            depth=request.depth
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate/questions")
async def generate_questions(request: QuestionGenerationRequest):
    """Belirli bir konu için soru üret"""
    try:
        context = rare_model.rag_system.get_context_for_query(request.topic, request.topic)
        result = rare_model.gemini_service.generate_questions_with_reasoning(
            context=context,
            topic=request.topic,
            count=request.count
        )
        
        # Zorluk filtresi uygula
        if request.difficulty and 'questions' in result:
            filtered_questions = [
                q for q in result['questions'] 
                if q.get('difficulty') == request.difficulty
            ]
            result['questions'] = filtered_questions
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/curriculum/topics")
async def get_curriculum_topics():
    """Müfredat konularını listele"""
    try:
        curriculum_data = curriculum_loader.load_din_kulturu_curriculum()
        topics = {}
        
        for doc in curriculum_data:
            topic = doc['topic']
            if topic not in topics:
                topics[topic] = []
            topics[topic].append({
                'subtopic': doc['subtopic'],
                'difficulty': doc['difficulty'],
                'keywords': doc.get('keywords', [])
            })
        
        return {
            "topics": topics,
            "total_topics": len(topics),
            "total_subtopics": len(curriculum_data)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/curriculum/search")
async def search_curriculum(query: str, topic: Optional[str] = None):
    """Müfredat içinde arama yap"""
    try:
        relevant_docs = rare_model.rag_system.search_relevant_documents(
            query=query,
            filters={'topic': topic} if topic else None
        )
        
        return {
            "query": query,
            "topic_filter": topic,
            "results": relevant_docs,
            "result_count": len(relevant_docs)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analysis/curriculum-trends")
async def analyze_curriculum_trends():
    """Müfredat trendlerini analiz et"""
    try:
        analysis = rare_model.analyze_curriculum_trends()
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reasoning/deep-analysis")
async def deep_reasoning_analysis(topic: str, depth: int = 3):
    """Derin reasoning analizi yap"""
    try:
        result = rare_model.deep_reasoning(topic, depth)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/cache/clear")
async def clear_cache(pattern: str = "*"):
    """Cache'i temizle"""
    try:
        rare_model.cache.clear_cache(pattern)
        return {"message": f"Cache cleared with pattern: {pattern}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/system/health")
async def health_check():
    """Sistem sağlık kontrolü"""
    try:
        # Redis bağlantısı kontrol et
        redis_status = "healthy"
        try:
            rare_model.cache.redis_client.ping()
        except:
            redis_status = "error"
        
        # ChromaDB kontrol et
        chroma_status = "healthy"
        try:
            rare_model.rag_system.collection.count()
        except:
            chroma_status = "error"
        
        return {
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "components": {
                "redis_cache": redis_status,
                "chroma_db": chroma_status,
                "gemini_api": "healthy" if settings.GOOGLE_API_KEY else "not_configured"
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/system/stats")
async def system_stats():
    """Sistem istatistikleri"""
    try:
        # ChromaDB doküman sayısı
        doc_count = rare_model.rag_system.collection.count()
        
        # Müfredat konuları
        curriculum_data = curriculum_loader.load_din_kulturu_curriculum()
        topic_counts = {}
        for doc in curriculum_data:
            topic = doc['topic']
            topic_counts[topic] = topic_counts.get(topic, 0) + 1
        
        return {
            "database_stats": {
                "total_documents": doc_count,
                "curriculum_topics": len(topic_counts),
                "topic_distribution": topic_counts
            },
            "system_config": {
                "embedding_model": settings.EMBEDDING_MODEL,
                "gemini_model": settings.GEMINI_MODEL,
                "cache_ttl": settings.CACHE_TTL,
                "top_k_documents": settings.TOP_K_DOCUMENTS
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# CLI Fonksiyonları
class CLIInterface:
    def __init__(self):
        self.prediction_service = PredictionService()
        self.rare_model = RAREModel()
    
    def interactive_prediction(self):
        """Etkileşimli tahmin modu"""
        print("🎯 LGS Din Kültürü Soru Tahmin Sistemi")
        print("=" * 50)
        
        while True:
            print("\nSeçenekler:")
            print("1. Sınav soruları tahmin et")
            print("2. Konu analizi yap")
            print("3. Soru üret")
            print("4. Müfredat ara")
            print("5. Çıkış")
            
            choice = input("\nSeçiminizi yapın (1-5): ")
            
            if choice == "1":
                self._predict_questions_cli()
            elif choice == "2":
                self._analyze_topic_cli()
            elif choice == "3":
                self._generate_questions_cli()
            elif choice == "4":
                self._search_curriculum_cli()
            elif choice == "5":
                print("Hoşça kalın! 👋")
                break
            else:
                print("Geçersiz seçim. Lütfen 1-5 arasında bir sayı girin.")
    
    def _predict_questions_cli(self):
        """CLI üzerinden soru tahmini"""
        print("\n📝 Sınav Soruları Tahmini")
        print("-" * 30)
        
        count = int(input("Kaç soru tahmin edilsin? (varsayılan: 10): ") or 10)
        difficulty = input("Zorluk seviyesi (kolay/orta/zor, boş bırakılabilir): ") or None
        topic = input("Konu filtresi (boş bırakılabilir): ") or None
        
        print("\n⏳ Tahmin yapılıyor...")
        
        result = self.prediction_service.predict_next_exam_questions(
            question_count=count,
            difficulty_filter=difficulty,
            topic_filter=topic
        )
        
        print(f"\n✅ {len(result['predicted_questions'])} soru tahmin edildi:")
        print("-" * 50)
        
        for i, question in enumerate(result['predicted_questions'][:5], 1):
            print(f"\n{i}. {question['question']}")
            for option, text in question['options'].items():
                print(f"   {option}) {text}")
            print(f"   Doğru Cevap: {question['correct_answer']}")
            print(f"   Konu: {question.get('topic', 'Belirtilmemiş')}")
            print(f"   Zorluk: {question.get('difficulty', 'orta')}")
            print(f"   Güven Skoru: {question.get('prediction_confidence', 0):.2f}")
        
        if len(result['predicted_questions']) > 5:
            print(f"\n... ve {len(result['predicted_questions']) - 5} soru daha.")
    
    def _analyze_topic_cli(self):
        """CLI üzerinden konu analizi"""
        print("\n🔍 Konu Analizi")
        print("-" * 20)
        
        topic = input("Analiz edilecek konu: ")
        depth = int(input("Analiz derinliği (1-5, varsayılan: 2): ") or 2)
        
        print(f"\n⏳ {topic} konusu analiz ediliyor...")
        
        result = self.prediction_service.get_topic_specific_prediction(topic, depth)
        
        print(f"\n✅ {topic} Analiz Sonuçları:")
        print("-" * 40)
        
        if 'deep_analysis' in result:
            insights = result['deep_analysis'].get('final_insights', {})
            if isinstance(insights, dict) and 'insights' in insights:
                print(f"💡 Ana Bulgular: {insights['insights'][:200]}...")
        
        if 'generated_questions' in result and 'questions' in result['generated_questions']:
            questions = result['generated_questions']['questions']
            print(f"\n📝 Üretilen sorular ({len(questions)} adet):")
            for i, q in enumerate(questions[:3], 1):
                print(f"\n{i}. {q['question']}")
                print(f"   Doğru Cevap: {q['correct_answer']}")
    
    def _generate_questions_cli(self):
        """CLI üzerinden soru üretimi"""
        print("\n🎲 Soru Üretimi")
        print("-" * 18)
        
        topic = input("Konu: ")
        count = int(input("Kaç soru? (varsayılan: 5): ") or 5)
        
        print(f"\n⏳ {topic} konusunda {count} soru üretiliyor...")
        
        context = self.rare_model.rag_system.get_context_for_query(topic, topic)
        result = self.rare_model.gemini_service.generate_questions_with_reasoning(
            context, topic, count
        )
        
        if 'questions' in result:
            print(f"\n✅ Üretilen Sorular:")
            print("-" * 30)
            
            for i, question in enumerate(result['questions'], 1):
                print(f"\n{i}. {question['question']}")
                for option, text in question['options'].items():
                    print(f"   {option}) {text}")
                print(f"   Doğru Cevap: {question['correct_answer']}")
                if 'reasoning' in question:
                    print(f"   Açıklama: {question['reasoning'][:100]}...")
    
    def _search_curriculum_cli(self):
        """CLI üzerinden müfredat arama"""
        print("\n🔎 Müfredat Arama")
        print("-" * 20)
        
        query = input("Arama sorgusu: ")
        
        print(f"\n⏳ '{query}' aranıyor...")
        
        results = self.rare_model.rag_system.search_relevant_documents(query)
        
        print(f"\n✅ {len(results)} sonuç bulundu:")
        print("-" * 30)
        
        for i, doc in enumerate(results[:3], 1):
            print(f"\n{i}. Konu: {doc['metadata'].get('topic', 'Bilinmeyen')}")
            print(f"   Alt Konu: {doc['metadata'].get('subtopic', 'Bilinmeyen')}")
            print(f"   İçerik: {doc['content'][:150]}...")
            print(f"   Benzerlik: {1 - doc['distance']:.3f}")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "cli":
        # CLI modu
        cli = CLIInterface()
        cli.interactive_prediction()
    else:
        # Web server modu
        print("🚀 LGS Din Kültürü Soru Tahmin Sistemi başlatılıyor...")
        print(f"📡 API: http://localhost:8000")
        print(f"📖 Dokümantasyon: http://localhost:8000/docs")
        
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )