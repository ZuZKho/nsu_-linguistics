from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from db.repositories.TextRepository import TextRepository
from db.repositories.CorpusRepository import CorpusRepository

@require_http_methods(["POST"])
def create_text(request):
    try:
        data = json.loads(request.body)
        
        # Валидация
        if not data.get('title'):
            return JsonResponse({'error': 'Title is required'}, status=400)
        if not data.get('corpus_id'):
            return JsonResponse({'error': 'Corpus ID is required'}, status=400)
            
        # Проверяем существование корпуса
        corpus = CorpusRepository.get_by_id(data['corpus_id'])
        if not corpus:
            return JsonResponse({'error': 'Corpus not found'}, status=404)
            
        text_data = {
            'title': data['title'],
            'description': data.get('description', ''),
            'content': data.get('content', ''),
            'corpus_id': data['corpus_id']
        }
        
        # Обработка перевода, если есть
        if 'has_translation' in data:
            translation_text = TextRepository.get_by_id(data['has_translation'])
            if not translation_text:
                return JsonResponse({'error': 'Translation text not found'}, status=404)
            text_data['has_translation_id'] = data['has_translation']
        
        text = TextRepository.create(text_data)
        
        return JsonResponse({
            'id': text.id,
            'title': text.title,
            'description': text.description,
            'content': text.content,
            'corpus_id': text.corpus_id,
            'has_translation': text.has_translation_id
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["PUT"])
def update_text(request, text_id):
    try:
        data = json.loads(request.body)
        text = TextRepository.get_by_id(text_id)
        
        if not text:
            return JsonResponse({'error': 'Text not found'}, status=404)
        
        update_data = {}
        if 'title' in data:
            update_data['title'] = data['title']
        if 'description' in data:
            update_data['description'] = data['description']
        if 'content' in data:
            update_data['content'] = data['content']
        if 'corpus_id' in data:
            # Проверяем существование корпуса
            corpus = CorpusRepository.get_by_id(data['corpus_id'])
            if not corpus:
                return JsonResponse({'error': 'Corpus not found'}, status=404)
            update_data['corpus_id'] = data['corpus_id']
        if 'has_translation' in data:
            if data['has_translation'] is not None:
                translation_text = TextRepository.get_by_id(data['has_translation'])
                if not translation_text:
                    return JsonResponse({'error': 'Translation text not found'}, status=404)
            update_data['has_translation_id'] = data['has_translation']
            
        updated_text = TextRepository.update(text, update_data)
        
        return JsonResponse({
            'id': updated_text.id,
            'title': updated_text.title,
            'description': updated_text.description,
            'content': updated_text.content,
            'corpus_id': updated_text.corpus_id,
            'has_translation': updated_text.has_translation_id
        })
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def get_text(request, text_id):
    try:
        text = TextRepository.get_by_id(text_id)
        if not text:
            return JsonResponse({'error': 'Text not found'}, status=404)
        
        text_data = {
            'id': text.id,
            'title': text.title,
            'description': text.description,
            'content': text.content,
            'corpus_id': text.corpus_id,
            'corpus_name': text.corpus.name if text.corpus else None,
            'has_translation': text.has_translation_id,
        }
        
        return JsonResponse(text_data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["DELETE"])
def delete_text(request, text_id):
    try:
        text = TextRepository.get_by_id(text_id)
        if not text:
            return JsonResponse({'error': 'Text not found'}, status=404)
        
        success = TextRepository.delete(text)
        if success:
            return JsonResponse({'message': 'Text deleted successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Failed to delete text'}, status=500)
            
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)