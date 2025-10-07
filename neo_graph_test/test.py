#!/usr/bin/env python3

import requests
import json
import sys
import os

# Настройки
BASE_URL = "http://127.0.0.1:8000/api"

class Colors:
    GREEN = '\033[0;32m'
    BLUE = '\033[0;34m'
    YELLOW = '\033[1;33m'
    RED = '\033[0;31m'
    NC = '\033[0m'

def print_color(color, message):
    print(f"{color}{message}{Colors.NC}")

def test_endpoint(method, url, data=None, expected_status=200):
    """Тестирует endpoint и возвращает результат"""
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=data)
        elif method == "PUT":
            response = requests.put(url, json=data)
        elif method == "DELETE":
            response = requests.delete(url)
        
        success = response.status_code == expected_status
        color = Colors.GREEN if success else Colors.RED
        status_icon = "✅" if success else "❌"
        
        print_color(color, f"{status_icon} {method} {url} - Status: {response.status_code} (expected: {expected_status})")
        
        if response.status_code in [200, 201]:
            return response.json(), True
        else:
            print_color(Colors.RED, f"   Response: {response.text}")
            return None, False
            
    except Exception as e:
        print_color(Colors.RED, f"❌ Exception: {e}")
        return None, False

def main():
    print_color(Colors.BLUE, "🧪 ТЕСТИРОВАНИЕ API ENDPOINTS")
    print("=" * 60)
    
    # Словарь для хранения созданных URI
    uris = {}
    
    # 1. ТЕСТИРУЕМ ONTOLOGY ENDPOINTS
    print_color(Colors.BLUE, "\n1. ONTOLOGY ENDPOINTS:")
    
    # Получаем онтологию
    response, success = test_endpoint("GET", f"{BASE_URL}/ontology/")
    if success and response:
        signatures_count = len(response.get('signatures', []))
        objects_count = len(response.get('objects', []))
        print_color(Colors.GREEN, f"   📊 Сигнатур: {signatures_count}, Объектов: {objects_count}")
    
    # Получаем родительские классы
    response, success = test_endpoint("GET", f"{BASE_URL}/ontology/parent-classes/")
    if success and response:
        classes_count = len(response.get('classes', []))
        print_color(Colors.GREEN, f"   🏗️  Родительских классов: {classes_count}")
    
    # 2. СОЗДАЕМ КЛАССЫ
    print_color(Colors.BLUE, "\n2. СОЗДАНИЕ КЛАССОВ:")
    
    classes_to_create = [
        {"title": "Животное", "description": "Базовый класс для всех животных"},
        {"title": "Млекопитающее", "description": "Класс млекопитающих"},
        {"title": "Птица", "description": "Класс птиц"},
        {"title": "Человек", "description": "Класс людей"}, 
        {"title": "Собака", "description": "Класс собак"},
        {"title": "Среда обитания", "description": "Среда обитания"}
    ]
    
    for class_data in classes_to_create:
        response, success = test_endpoint("POST", f"{BASE_URL}/classes/", class_data, 201)
        if success and response and 'uri' in response:
            key = class_data['title'].upper().replace(' ', '_')
            uris[key] = response['uri']
            print_color(Colors.GREEN, f"   🆔 {key}: {response['uri']}")
    
    # 3. ДОБАВЛЯЕМ СВЯЗИ МЕЖДУ КЛАССАМИ
    print_color(Colors.BLUE, "\n3. ИЕРАРХИЯ КЛАССОВ:")
    
    # Добавляем родительские связи
    parent_relations = [
        ("МЛЕКОПИТАЮЩЕЕ", "ЖИВОТНОЕ"),
        ("ПТИЦА", "ЖИВОТНОЕ"), 
        ("ЧЕЛОВЕК", "МЛЕКОПИТАЮЩЕЕ"),
        ("СОБАКА", "МЛЕКОПИТАЮЩЕЕ")
    ]
    
    for child_key, parent_key in parent_relations:
        if child_key in uris and parent_key in uris:
            data = {"parent_uri": uris[parent_key]}
            response, success = test_endpoint("POST", f"{BASE_URL}/classes/{uris[child_key]}/add-parent/", data)
    
    # 4. ДОБАВЛЯЕМ DATATYPE PROPERTIES
    print_color(Colors.BLUE, "\n4. DATATYPE PROPERTIES:")
    
    attributes_to_create = [
        ("ЖИВОТНОЕ", "количество_ног"),
        ("ЖИВОТНОЕ", "продолжительность_жизни"),
        ("ПТИЦА", "размах_крыльев"),
        ("СОБАКА", "порода"),
        ("ЧЕЛОВЕК", "интеллект")
    ]
    
    for class_key, attr_name in attributes_to_create:
        if class_key in uris:
            data = {"datatype_title": attr_name}
            response, success = test_endpoint("POST", f"{BASE_URL}/classes/{uris[class_key]}/attributes/", data, 201)
            if success and response and 'uri' in response:
                print_color(Colors.GREEN, f"   📝 {attr_name} -> {response['uri']}")
    
    # 5. ДОБАВЛЯЕМ OBJECT PROPERTIES
    print_color(Colors.BLUE, "\n5. OBJECT PROPERTIES:")
    
    object_attributes_to_create = [
        ("ЖИВОТНОЕ", "имеет_родителя", "ЖИВОТНОЕ"),
        ("ЖИВОТНОЕ", "живет_в", "СРЕДА_ОБИТАНИЯ"),
        ("СОБАКА", "дрессируется_у", "ЧЕЛОВЕК")
    ]
    
    for class_key, attr_name, range_key in object_attributes_to_create:
        if class_key in uris and range_key in uris:
            data = {
                "attr_name": attr_name,
                "range_uri": uris[range_key]
            }
            response, success = test_endpoint("POST", f"{BASE_URL}/classes/{uris[class_key]}/object-attributes/", data, 201)
            if success and response and 'uri' in response:
                print_color(Colors.GREEN, f"   🔗 {attr_name} -> {response['uri']}")
    
    # 6. ТЕСТИРУЕМ ПОЛУЧЕНИЕ ИНФОРМАЦИИ О КЛАССАХ
    print_color(Colors.BLUE, "\n6. ИНФОРМАЦИЯ О КЛАССАХ:")
    
    for class_key in ["СОБАКА", "ЖИВОТНОЕ"]:
        if class_key in uris:
            # Получаем информацию о классе
            response, success = test_endpoint("GET", f"{BASE_URL}/classes/{uris[class_key]}/")
            if success:
                print_color(Colors.GREEN, f"   ℹ️  {class_key}: {response.get('title')}")
            
            # Получаем сигнатуру
            response, success = test_endpoint("GET", f"{BASE_URL}/classes/{uris[class_key]}/signature/")
            if success:
                datatype_props = [p['title'] for p in response.get('params', [])]
                object_props = [p['title'] for p in response.get('obj_params', [])]
                print_color(Colors.GREEN, f"   📋 {class_key} сигнатура: {len(datatype_props)} datatype, {len(object_props)} object")
            
            # Получаем родителей
            response, success = test_endpoint("GET", f"{BASE_URL}/classes/{uris[class_key]}/parents/")
            if success:
                parents_count = len(response.get('parents', []))
                print_color(Colors.GREEN, f"   👪 {class_key} родителей: {parents_count}")
            
            # Получаем детей
            response, success = test_endpoint("GET", f"{BASE_URL}/classes/{uris[class_key]}/children/")
            if success:
                children_count = len(response.get('children', []))
                print_color(Colors.GREEN, f"   👶 {class_key} детей: {children_count}")
    
    # 7. СОЗДАЕМ ОБЪЕКТЫ
    print_color(Colors.BLUE, "\n7. СОЗДАНИЕ ОБЪЕКТОВ:")
    
    # Создаем среды обитания
    habitats = [
        {"uri": uris["СРЕДА_ОБИТАНИЯ"], "title": "Дом", "description": "Дом для проживания"},
        {"uri": uris["СРЕДА_ОБИТАНИЯ"], "title": "Будка", "description": "Будка для собаки"}
    ]
    
    for habitat in habitats:
        data = {
            "uri": habitat["uri"],
            "title": habitat["title"],
            "description": habitat["description"]
        }
        response, success = test_endpoint("POST", f"{BASE_URL}/objects/", data, 201)
        if success and response and 'uri' in response:
            uris[habitat['title'].upper()] = response['uri']
            print_color(Colors.GREEN, f"   🏠 {habitat['title']}: {response['uri']}")
    
    # Создаем человека
    human_data = {
        "uri": uris["ЧЕЛОВЕК"],
        "title": "Матвей",
        "description": "Человек который дрессирует собак",
        "properties": {"продолжительность_жизни": 80},
        "object_properties": {"живет_в": uris["ДОМ"]}
    }
    response, success = test_endpoint("POST", f"{BASE_URL}/objects/", human_data, 201)
    if success and response and 'uri' in response:
        uris['MATVEY'] = response['uri']
        print_color(Colors.GREEN, f"   👨 Матвей: {response['uri']}")
    
    # Создаем собаку
    dog_data = {
        "uri": uris["СОБАКА"],
        "title": "Рекс", 
        "description": "Дружелюбная собака породы овчарка",
        "properties": {"продолжительность_жизни": 18},
        "object_properties": {
            "живет_в": uris["БУДКА"],
            "дрессируется_у": uris["MATVEY"]
        }
    }
    response, success = test_endpoint("POST", f"{BASE_URL}/objects/", dog_data, 201)
    if success and response and 'uri' in response:
        uris['REX'] = response['uri']
        print_color(Colors.GREEN, f"   🐶 Рекс: {response['uri']}")
    
    # 8. ТЕСТИРУЕМ ОБЪЕКТЫ
    print_color(Colors.BLUE, "\n8. ТЕСТИРОВАНИЕ ОБЪЕКТОВ:")
    
    for obj_key in ["REX", "MATVEY"]:
        if obj_key in uris:
            response, success = test_endpoint("GET", f"{BASE_URL}/objects/{uris[obj_key]}/")
            if success:
                print_color(Colors.GREEN, f"   📦 {obj_key}: {response.get('title')} - {response.get('description')}")
    
    # 9. ФИНАЛЬНАЯ ПРОВЕРКА
    print_color(Colors.BLUE, "\n9. ФИНАЛЬНАЯ ПРОВЕРКА:")
    
    # Получаем полную онтологию
    response, success = test_endpoint("GET", f"{BASE_URL}/ontology/")
    if success and response:
        signatures_count = len(response.get('signatures', []))
        objects_count = len(response.get('objects', []))
        print_color(Colors.GREEN, f"   📊 Итоговая онтология: {signatures_count} сигнатур, {objects_count} объектов")
    
    # Сохраняем URI для последующего использования
    with open('test_uris.json', 'w') as f:
        json.dump(uris, f, indent=2)
    
    print_color(Colors.GREEN, "\n✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
    print_color(Colors.YELLOW, "📁 URI сохранены в test_uris.json")

if __name__ == "__main__":
    main()