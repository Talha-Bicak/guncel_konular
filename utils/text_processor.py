import re
import nltk
from typing import List, Dict, Any
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

class TextProcessor:
    def __init__(self):
        self._download_nltk_data()
        self.stop_words = set(stopwords.words('turkish'))
    
    def _download_nltk_data(self):
        """NLTK verilerini indir"""
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('punkt')
            nltk.download('stopwords')
    
    def clean_text(self, text: str) -> str:
        """Metni temizle"""
        # HTML taglarını kaldır
        text = re.sub(r'<[^>]+>', '', text)
        # Özel karakterleri kaldır
        text = re.sub(r'[^\w\s]', ' ', text)
        # Çoklu boşlukları tek boşluk yap
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def tokenize(self, text: str) -> List[str]:
        """Metni tokenize et"""
        tokens = word_tokenize(text.lower(), language='turkish')
        return [token for token in tokens if token not in self.stop_words and len(token) > 2]
    
    def split_into_sentences(self, text: str) -> List[str]:
        """Metni cümlelere ayır"""
        return sent_tokenize(text, language='turkish')
    
    def extract_keywords(self, text: str, top_k: int = 10) -> List[str]:
        """Anahtar kelimeleri çıkar"""
        tokens = self.tokenize(text)
        word_freq = {}
        for token in tokens:
            word_freq[token] = word_freq.get(token, 0) + 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:top_k]]