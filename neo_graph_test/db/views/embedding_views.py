from rest_framework.decorators import api_view
from django.http import JsonResponse
from db.services.embedding_service import EmbeddingService

@api_view(["POST"])
def chunk_text(request):
    data = request.data
    text = data.get("text", "")
    service = EmbeddingService()
    chunks = service.get_chunks(text)
    return JsonResponse({"chunks": chunks})

@api_view(["POST"])
def get_embeddings(request):
    data = request.data
    texts = data.get("texts", [])
    service = EmbeddingService()
    embeddings = service.get_embeddings(texts)
    return JsonResponse({"embeddings": embeddings.tolist()})

@api_view(["POST"])
def compare_embeddings(request):
    data = request.data
    service = EmbeddingService()
    similarity = service.cos_compare(data.get("embedding1"), data.get("embedding2"))
    return JsonResponse({"cosine_similarity": similarity})