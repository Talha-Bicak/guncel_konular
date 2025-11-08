import redis
import json
import hashlib
from typing import Any, Optional, Dict, List
from config.settings import settings
from datetime import datetime, timedelta

class CAGCache:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.ttl = settings.CACHE_TTL
    
    def _generate_key(self, prefix: str, data: Any) -> str:
        """Cache anahtarı oluştur"""
        data_str = json.dumps(data, sort_keys=True, ensure_ascii=False)
        hash_value = hashlib.md5(data_str.encode('utf-8')).hexdigest()
        return f"{prefix}:{hash_value}"
    
    def get_cached_response(self, prefix: str, query_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Cache'den yanıt al"""
        key = self._generate_key(prefix, query_data)
        try:
            cached_data = self.redis_client.get(key)
            if cached_data:
                return json.loads(cached_data.decode('utf-8'))
        except Exception as e:
            print(f"Cache okuma hatası: {e}")
        return None
    
    def cache_response(self, prefix: str, query_data: Dict[str, Any], response: Dict[str, Any]):
        """Yanıtı cache'le"""
        key = self._generate_key(prefix, query_data)
        try:
            cached_item = {
                "response": response,
                "timestamp": datetime.now().isoformat(),
                "query_data": query_data
            }
            self.redis_client.setex(
                key, 
                self.ttl, 
                json.dumps(cached_item, ensure_ascii=False)
            )
        except Exception as e:
            print(f"Cache yazma hatası: {e}")
    
    def get_cached_embeddings(self, text: str) -> Optional[List[float]]:
        """Cache'den embedding al"""
        return self.get_cached_response("embedding", {"text": text})
    
    def cache_embeddings(self, text: str, embeddings: List[float]):
        """Embedding'i cache'le"""
        self.cache_response("embedding", {"text": text}, {"embeddings": embeddings})
    
    def get_cached_questions(self, topic: str, difficulty: str) -> Optional[List[Dict[str, Any]]]:
        """Cache'den soruları al"""
        return self.get_cached_response("questions", {"topic": topic, "difficulty": difficulty})
    
    def cache_questions(self, topic: str, difficulty: str, questions: List[Dict[str, Any]]):
        """Soruları cache'le"""
        self.cache_response("questions", {"topic": topic, "difficulty": difficulty}, {"questions": questions})
    
    def clear_cache(self, pattern: str = "*"):
        """Cache'i temizle"""
        try:
            keys = self.redis_client.keys(pattern)
            if keys:
                self.redis_client.delete(*keys)
        except Exception as e:
            print(f"Cache temizleme hatası: {e}")