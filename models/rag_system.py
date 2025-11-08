import chromadb
from chromadb.config import Settings as ChromaSettings
from typing import List, Dict, Any, Optional
import uuid
from utils.embeddings import EmbeddingGenerator
from utils.text_processor import TextProcessor
from models.cag_cache import CAGCache
from config.settings import settings

class RAGSystem:
    def __init__(self):
        self.embedding_generator = EmbeddingGenerator()
        self.text_processor = TextProcessor()
        self.cache = CAGCache()
        
        # ChromaDB istemcisini başlat
        self.chroma_client = chromadb.PersistentClient(
            path=settings.CHROMA_DB_PATH,
            settings=ChromaSettings(anonymized_telemetry=False)
        )
        
        # Koleksiyon oluştur veya al
        try:
            self.collection = self.chroma_client.get_collection("din_kulturu_curriculum")
        except:
            self.collection = self.chroma_client.create_collection(
                name="din_kulturu_curriculum",
                metadata={"description": "LGS Din Kültürü Müfredatı"}
            )
    
    def add_documents(self, documents: List[Dict[str, Any]]):
        """Dokümanları RAG sistemine ekle"""
        for doc in documents:
            # Cache'den embedding kontrolü
            cached_embedding = self.cache.get_cached_embeddings(doc['content'])
            
            if cached_embedding:
                embedding = cached_embedding['embeddings']
            else:
                # Yeni embedding oluştur
                embedding = self.embedding_generator.encode(doc['content']).tolist()
                self.cache.cache_embeddings(doc['content'], embedding)
            
            # ChromaDB'ye ekle
            self.collection.add(
                documents=[doc['content']],
                embeddings=[embedding],
                metadatas=[{
                    'topic': doc.get('topic', ''),
                    'subtopic': doc.get('subtopic', ''),
                    'difficulty': doc.get('difficulty', 'orta'),
                    'source': doc.get('source', ''),
                    'keywords': ','.join(doc.get('keywords', []))
                }],
                ids=[str(uuid.uuid4())]
            )
    
    def search_relevant_documents(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """İlgili dokümanları ara"""
        # Query embedding'i al
        cached_query_embedding = self.cache.get_cached_embeddings(query)
        
        if cached_query_embedding:
            query_embedding = cached_query_embedding['embeddings']
        else:
            query_embedding = self.embedding_generator.encode(query).tolist()
            self.cache.cache_embeddings(query, query_embedding)
        
        # Filtreleri hazırla
        where_clause = {}
        if filters:
            for key, value in filters.items():
                if value:
                    where_clause[key] = value
        
        # Arama yap
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=settings.TOP_K_DOCUMENTS,
            where=where_clause if where_clause else None
        )
        
        # Sonuçları düzenle
        documents = []
        for i in range(len(results['documents'][0])):
            documents.append({
                'content': results['documents'][0][i],
                'metadata': results['metadatas'][0][i],
                'distance': results['distances'][0][i] if 'distances' in results else 0,
                'id': results['ids'][0][i]
            })
        
        return documents
    
    def get_context_for_query(self, query: str, topic: str = None) -> str:
        """Query için bağlam oluştur"""
        filters = {'topic': topic} if topic else None
        relevant_docs = self.search_relevant_documents(query, filters)
        
        context = "İlgili Müfredat İçeriği:\n\n"
        for i, doc in enumerate(relevant_docs):
            context += f"{i+1}. {doc['content']}\n"
            if doc['metadata'].get('keywords'):
                context += f"   Anahtar Kelimeler: {doc['metadata']['keywords']}\n"
            context += "\n"
        
        return context