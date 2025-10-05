from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from db.repositories.CorpusRepository import CorpusRepository
from db.repositories.TextRepository import TextRepository

@require_http_methods(["POST"])
def create_corpus(request):
    try:
        data = json.loads(request.body)
        
        # Валидация
        if not data.get('name'):
            return JsonResponse({'error': 'Name is required'}, status=400)
        if not data.get('genre'):
            return JsonResponse({'error': 'Genre is required'}, status=400)
            
        corpus = CorpusRepository.create({
            'name': data['name'],
            'description': data.get('description', ''),
            'genre': data.get('genre')
        })
        
        return JsonResponse({
            'id': corpus.id,
            'name': corpus.name,
            'description': corpus.description,
            'genre': corpus.genre,
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["PUT"])
def update_corpus(request, corpus_id):
    try:
        data = json.loads(request.body)
        corpus = CorpusRepository.get_by_id(corpus_id)
        
        if not corpus:
            return JsonResponse({'error': 'Corpus not found'}, status=404)
        
        update_data = {}
        if 'name' in data:
            update_data['name'] = data['name']
        if 'description' in data:
            update_data['description'] = data['description']
        if 'genre' in data:
            update_data['genre'] = data['genre']
            
        updated_corpus = CorpusRepository.update(corpus, update_data)
        
        return JsonResponse({
            'id': updated_corpus.id,
            'name': updated_corpus.name,
            'description': updated_corpus.description,
            'genre': updated_corpus.genre,
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_corpus(request, corpus_id):
    try:
        corpus = CorpusRepository.get_corpus_with_texts(corpus_id)
        if not corpus:
            return JsonResponse({'error': 'Corpus not found'}, status=404)
        
        # Собираем данные с текстами
        corpus_data = {
            'id': corpus.id,
            'name': corpus.name,
            'description': corpus.description,
            'genre': corpus.genre,
            'texts': [
                {
                    'id': text.id,
                    'title': text.title,
                    'description': text.description,
                    'content': text.content,
                    'has_translation': text.has_translation_id,
                }
                for text in corpus.texts.all()
            ]
        }
        
        return JsonResponse(corpus_data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["DELETE"])
def delete_corpus(request, corpus_id):
    try:
        corpus = CorpusRepository.get_by_id(corpus_id)
        if not corpus:
            return JsonResponse({'error': 'Corpus not found'}, status=404)
        
        success = CorpusRepository.delete(corpus)
        if success:
            return JsonResponse({'message': 'Corpus deleted successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Failed to delete corpus'}, status=500)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)