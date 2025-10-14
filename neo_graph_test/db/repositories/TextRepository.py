from typing import List, Optional
from db.models import Text
from db.services.embedding_service import EmbeddingService
import json

class TextRepository:
    
    @staticmethod
    def get_all() -> List[Text]:
        return Text.objects.select_related('corpus', 'has_translation').all()
    
    @staticmethod
    def get_by_id(text_id: int) -> Optional[Text]:
        try:
            return Text.objects.select_related('corpus', 'has_translation').get(id=text_id)
        except Text.DoesNotExist:
            return None
    
    @staticmethod
    def create(text_data: dict) -> Text:
        service = EmbeddingService()
        chunks = service.get_chunks(text_data.get('content'))
        text_data["embeddings"] = json.dumps(service.get_embeddings(chunks).tolist())
        return Text.objects.create(**text_data)
    
    @staticmethod
    def update(text: Text, text_data: dict) -> Text:
        for field, value in text_data.items():
            setattr(text, field, value)
        service = EmbeddingService()
        chunks = service.get_chunks(text_data.get('content'))
        text_data["embeddings"] = json.dumps(service.get_embeddings(chunks).tolist())
        text.save()
        return text
    
    @staticmethod
    def delete(text: Text) -> bool:
        try:
            text.delete()
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_by_corpus(corpus_id: int) -> List[Text]:
        return Text.objects.filter(corpus_id=corpus_id).select_related('has_translation')