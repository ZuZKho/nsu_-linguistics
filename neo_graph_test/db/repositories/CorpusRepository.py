from typing import List, Optional
from db.models import Corpus

class CorpusRepository:
    
    @staticmethod
    def get_all() -> List[Corpus]:
        return Corpus.objects.all()
    
    @staticmethod
    def get_by_id(corpus_id: int) -> Optional[Corpus]:
        try:
            return Corpus.objects.get(id=corpus_id)
        except Corpus.DoesNotExist:
            return None
    
    @staticmethod
    def create(corpus_data: dict) -> Corpus:
        return Corpus.objects.create(**corpus_data)
    
    @staticmethod
    def update(corpus: Corpus, corpus_data: dict) -> Corpus:
        for field, value in corpus_data.items():
            setattr(corpus, field, value)
        corpus.save()
        return corpus
    
    @staticmethod
    def delete(corpus: Corpus) -> bool:
        try:
            corpus.delete()
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_corpus_with_texts(corpus_id: int) -> Optional[Corpus]:
        try:
            return Corpus.objects.prefetch_related('texts').get(id=corpus_id)
        except Corpus.DoesNotExist:
            return None