from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Union
from config.settings import settings

class EmbeddingGenerator:
    def __init__(self):
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)
    
    def encode(self, texts: Union[str, List[str]]) -> np.ndarray:
        """Metinleri embedding'lere dönüştür"""
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(texts)
    
    def compute_similarity(self, text1: str, text2: str) -> float:
        """İki metin arasındaki benzerliği hesapla"""
        embeddings = self.encode([text1, text2])
        similarity = np.dot(embeddings[0], embeddings[1]) / (
            np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
        )
        return float(similarity)
    
    def find_most_similar(self, query: str, candidates: List[str], top_k: int = 5) -> List[tuple]:
        """En benzer metinleri bul"""
        query_embedding = self.encode(query)
        candidate_embeddings = self.encode(candidates)
        
        similarities = []
        for i, candidate_embedding in enumerate(candidate_embeddings):
            similarity = np.dot(query_embedding, candidate_embedding) / (
                np.linalg.norm(query_embedding) * np.linalg.norm(candidate_embedding)
            )
            similarities.append((i, candidates[i], float(similarity)))
        
        similarities.sort(key=lambda x: x[2], reverse=True)
        return similarities[:top_k]
