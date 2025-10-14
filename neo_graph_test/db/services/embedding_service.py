
from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re

# if model can't be downloaded run the next command in cmd before:
# python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')"

class EmbeddingService:
    def __init__(self):
       self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

    def __enter__(self):
        return self
    
    def get_chunks(self, text: str, max_tokens: int = 128) -> List[str]:
        sentences = re.findall(r'[^.!?]*[.!?]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            if len(current_chunk.split()) + len(sentence.split()) <= max_tokens:
                current_chunk += " " + sentence if current_chunk else sentence
            else:
                if current_chunk:
                    chunks.append(current_chunk)
                current_chunk = sentence
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks

    def get_embeddings(self, texts: List[str]) -> List[np.array]:
        embeddings = self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
        return embeddings
    
    def cos_compare(self, emb1: List[float], emb2: List[float]) -> float:
        emb1 = np.array(emb1).reshape(1, -1)
        emb2 = np.array(emb2).reshape(1, -1)
        return float(cosine_similarity(emb1, emb2)[0][0])

