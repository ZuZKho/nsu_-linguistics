from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from functools import wraps
import json
from django.conf import settings
from db.repositories.ontology_driver.driver import OntologyRepository
from db.services.ontology_service import OntologyService

# Декоратор для обработки сервиса
def with_ontology_service(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        try:
            service = OntologyService(
                OntologyRepository(
                    uri=settings.NEO4J_URI,
                    user=settings.NEO4J_USER,
                    password=settings.NEO4J_PASSWORD
                )
            )
            with service:
                return func(request, service, *args, **kwargs)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    return wrapper

######################################
#      Ontology endpoints            #
######################################

@require_http_methods(["GET"])
@with_ontology_service
def get_ontology(request, service):
    ontology = service.get_ontology()
    return JsonResponse(ontology)

@require_http_methods(["GET"])
@with_ontology_service
def get_ontology_parent_classes(request, service):
    classes = service.get_ontology_parent_classes()
    return JsonResponse({'classes': classes})

######################################
#      Class endpoints               #
######################################

@require_http_methods(["GET"])
@with_ontology_service
def get_class(request, service, uri):
    class_obj = service.get_class(uri)
    if not class_obj:
        return JsonResponse({'error': 'Class not found'}, status=404)
    return JsonResponse(class_obj)

@require_http_methods(["GET"])
@with_ontology_service
def get_class_parents(request, service, uri):
    parents = service.get_class_parents(uri)
    return JsonResponse({'parents': parents})

@require_http_methods(["GET"])
@with_ontology_service
def get_class_children(request, service, uri):
    children = service.get_class_children(uri)
    return JsonResponse({'children': children})

@require_http_methods(["GET"])
@with_ontology_service
def get_class_objects(request, service, uri):
    objects = service.get_class_objects(uri)
    return JsonResponse({'objects': objects})

@csrf_exempt
@require_http_methods(["POST"])
@with_ontology_service
def create_class(request, service):
    data = json.loads(request.body)
    
    if not data.get('title'):
        return JsonResponse({'error': 'Title is required'}, status=400)
    
    uri = service.create_class(
        title=data['title'],
        description=data.get('description', ''),
        parent_uri=data.get('parent_uri')
    )
    return JsonResponse({'uri': uri}, status=201)

@csrf_exempt
@require_http_methods(["PUT"])
@with_ontology_service
def update_class(request, service, uri):
    data = json.loads(request.body)
    
    success = service.update_class(
        uri=uri,
        title=data.get('title'),
        description=data.get('description')
    )
    if success:
        return JsonResponse({'message': 'Class updated successfully'})
    return JsonResponse({'error': 'Class not found'}, status=404)

@csrf_exempt
@require_http_methods(["DELETE"])
@with_ontology_service
def delete_class(request, service, uri):
    success = service.delete_class(uri)
    if success:
        return JsonResponse({'message': 'Class deleted successfully'})
    return JsonResponse({'error': 'Class not found'}, status=404)

@csrf_exempt
@require_http_methods(["POST"])
@with_ontology_service
def add_class_parent(request, service, target_uri):
    data = json.loads(request.body)
    
    if not data.get('parent_uri'):
        return JsonResponse({'error': 'parent_uri is required'}, status=400)
    
    success = service.add_class_parent(
        parent_uri=data['parent_uri'],
        target_uri=target_uri
    )
    if success:
        return JsonResponse({'message': 'Parent class added successfully'})
    return JsonResponse({'error': 'Failed to add parent class'}, status=400)

######################################
#   Class attributes endpoints       #
######################################

@csrf_exempt
@require_http_methods(["POST"])
@with_ontology_service
def add_class_attribute(request, service, uri):
    data = json.loads(request.body)
    
    if not data.get('datatype_title'):
        return JsonResponse({'error': 'datatype_title is required'}, status=400)
    
    uri = service.add_class_attribute(
        uri=uri,
        datatype_title=data['datatype_title']
    )
    return JsonResponse({'uri': uri}, status=201)

@csrf_exempt
@require_http_methods(["DELETE"])
@with_ontology_service
def delete_class_attribute(request, service, attribute_uri):
    success = service.delete_class_attribute(attribute_uri)
    if success:
        return JsonResponse({'message': 'Attribute deleted successfully'})
    return JsonResponse({'error': 'Attribute not found'}, status=404)

@csrf_exempt
@require_http_methods(["POST"])
@with_ontology_service
def add_class_object_attribute(request, service, uri):
    data = json.loads(request.body)
    
    if not data.get('attr_name'):
        return JsonResponse({'error': 'attr_name is required'}, status=400)
    if not data.get('range_uri'):
        return JsonResponse({'error': 'range_uri is required'}, status=400)
    
    uri = service.add_class_object_attribute(
        uri=uri,
        attr_name=data['attr_name'],
        range_uri=data['range_uri']
    )
    return JsonResponse({'uri': uri}, status=201)

@csrf_exempt
@require_http_methods(["DELETE"])
@with_ontology_service
def delete_class_object_attribute(request, service, object_property_uri):
    success = service.delete_class_object_attribute(object_property_uri)
    if success:
        return JsonResponse({'message': 'Object attribute deleted successfully'})
    return JsonResponse({'error': 'Object attribute not found'}, status=404)

######################################
#      Object endpoints              #
######################################

@require_http_methods(["GET"])
@with_ontology_service
def get_object(request, service, uri):
    obj = service.get_object(uri)
    if not obj:
        return JsonResponse({'error': 'Object not found'}, status=404)
    return JsonResponse(obj)

@csrf_exempt
@require_http_methods(["POST"])
@with_ontology_service
def create_object(request, service):
    data = json.loads(request.body)
    
    if not data.get('uri'):
        return JsonResponse({'error': 'uri is required'}, status=400)
    if not data.get('title'):
        return JsonResponse({'error': 'title is required'}, status=400)
    
    uri = service.create_object(
        uri=data['uri'],
        title=data['title'],
        description=data.get('description', ''),
        properties=data.get('properties', {}),
        object_properties=data.get('object_properties', {})
    )
    return JsonResponse({'uri': uri}, status=201)

@csrf_exempt
@require_http_methods(["PUT"])
@with_ontology_service
def update_object(request, service, uri):
    data = json.loads(request.body)
    
    success = service.update_object(
        uri=uri,
        title=data.get('title'),
        description=data.get('description'),
        properties=data.get('properties', {}),
        new_connections=data.get('new_connections', {})
    )
    if success:
        return JsonResponse({'message': 'Object updated successfully'})
    return JsonResponse({'error': 'Object not found'}, status=404)

@csrf_exempt
@require_http_methods(["DELETE"])
@with_ontology_service
def delete_object(request, service, uri):
    success = service.delete_object(uri)
    if success:
        return JsonResponse({'message': 'Object deleted successfully'})
    return JsonResponse({'error': 'Object not found'}, status=404)

######################################
#      Signature endpoints           #
######################################

@require_http_methods(["GET"])
@with_ontology_service
def get_class_signature(request, service, uri):
    signature = service.collect_signature(uri)
    return JsonResponse(signature)
