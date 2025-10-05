from django.urls import path
from django.conf.urls import url
import db.views.corpus_views as corpus_views
import db.views.text_views as text_views
from db.views.ontology_views import *

urlpatterns = [
    # Corpus endpoints
    path('corpus/', corpus_views.create_corpus, name='create_corpus'),
    path('corpus/<int:corpus_id>/', corpus_views.update_corpus, name='update_corpus'),
    path('corpus/<int:corpus_id>/details/', corpus_views.get_corpus, name='get_corpus'),
    path('corpus/<int:corpus_id>/delete/', corpus_views.delete_corpus, name='delete_corpus'),
    
    # Text endpoints
    path('text/', text_views.create_text, name='create_text'),
    path('text/<int:text_id>/', text_views.update_text, name='update_text'),
    path('text/<int:text_id>/details/', text_views.get_text, name='get_text'),
    path('text/<int:text_id>/delete/', text_views.delete_text, name='delete_text'),

    # Ontology endpoints
    path('ontology/', get_ontology, name='get_ontology'),
    path('ontology/parent-classes/', get_ontology_parent_classes, name='get_ontology_parent_classes'),
    
    # Class endpoints
    path('classes/<path:uri>/parents/', get_class_parents, name='get_class_parents'),
    path('classes/<path:uri>/children/', get_class_children, name='get_class_children'),
    path('classes/<path:uri>/objects/', get_class_objects, name='get_class_objects'),
    path('classes/<path:uri>/signature/', get_class_signature, name='get_class_signature'),
    path('classes/<path:target_uri>/add-parent/', add_class_parent, name='add_class_parent'),
    path('classes/<path:uri>/update/', update_class, name='update_class'),
    path('classes/<path:uri>/delete/', delete_class, name='delete_class'),
    path('classes/<path:uri>/', get_class, name='get_class'),
    path('classes/', create_class, name='create_class'),
    
    # Class attributes endpoints
    path('classes/<path:class_uri>/attributes/', add_class_attribute, name='add_class_attribute'),
    path('attributes/<path:attribute_uri>/delete/', delete_class_attribute, name='delete_class_attribute'),
    path('classes/<path:class_uri>/object-attributes/', add_class_object_attribute, name='add_class_object_attribute'),
    path('object-attributes/<path:object_property_uri>/delete/', delete_class_object_attribute, name='delete_class_object_attribute'),
    
    # Object endpoints
    path('objects/<path:uri>/', get_object, name='get_object'),
    path('objects/', create_object, name='create_object'),
    path('objects/<path:uri>/update/', update_object, name='update_object'),
    path('objects/<path:uri>/delete/', delete_object, name='delete_object'),
]


"""
# Создать корпус
curl -X POST http://127.0.0.1:8000/api/corpus/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Русская классика", "description": "Классическая литература", "genre": "fiction"}'

# Получить корпус с текстами
curl http://127.0.0.1:8000/api/corpus/1/details/

# Создать текст
curl -X POST http://127.0.0.1:8000/api/text/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Война и мир", "description": "Роман", "content": "Текст...", "corpus": 1}'

# Обновить текст
curl -X PUT http://127.0.0.1:8000/api/text/1/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Война и мир - отрывок"}'

# Создать корпус
curl -X POST http://127.0.0.1:8000/api/corpora/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Russian Classics", "description": "Classic literature", "genre": "fiction"}'

# Получить корпус с текстами
curl http://127.0.0.1:8000/api/corpora/1/detail/



# Получить сигнатуру класса
curl http://127.0.0.1:8000/api/classes/http%3A%2F%2Fexample.org%2FPerson/signature/

# Поиск классов
curl http://127.0.0.1:8000/api/search/classes/?q=Person

# Полная иерархия онтологии
curl http://127.0.0.1:8000/api/ontology/hierarchy/

# Добавить родительский класс
curl -X POST http://127.0.0.1:8000/api/classes/http%3A%2F%2Fexample.org%2FStudent/add-parent/ \
  -H "Content-Type: application/json" \
  -d '{"parent_uri": "http://example.org/Person"}'

# Создать объектный атрибут
curl -X POST http://127.0.0.1:8000/api/classes/http%3A%2F%2Fexample.org%2FPerson/object-attributes/ \
  -H "Content-Type: application/json" \
  -d '{"attr_name": "hasFriend", "range_class_uri": "http://example.org/Person"}'

"""
