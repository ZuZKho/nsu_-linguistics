#!/usr/bin/env python3
"""
Запуск этого файла:
python -m db.repositories.ontology_driver.main
"""

import sys
import os

# Добавляем корень проекта в Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, project_root)

from db.repositories.ontology_driver.driver import OntologyRepository

# ТЕСТОВЫЙ ЗАПУСК
if __name__ == "__main__":
    print("=== ТЕСТОВЫЙ ЗАПУСК ONTOLOGY REPOSITORY ===\n")
    
    # Настройки подключения к Neo4j
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "password"
    
    try:
        with OntologyRepository(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD) as repo:
            
            # Создаем корневой класс и получаем его URI
            animal_uri = repo.create_class("Животное", "Базовый класс для всех животных")
            
            # Создаем дочерние классы
            mammal_uri = repo.create_class("Млекопитающее", "Класс млекопитающих", animal_uri)
            bird_uri = repo.create_class("Птица", "Класс птиц", animal_uri)

            human_uri = repo.create_class("Человек", "Класс людей", mammal_uri)
            dog_uri = repo.create_class("Собака", "Класс собак", mammal_uri)
            
            habitat_uri = repo.create_class("Среда обитания", "Среда обитания")

            # Добавляем datatype properties и получаем их URI
            legs_attr_uri = repo.add_class_attribute(animal_uri, "количество_ног")
            lifespan_attr_uri = repo.add_class_attribute(animal_uri, "продолжительность_жизни")
            wingspan_attr_uri = repo.add_class_attribute(bird_uri, "размах_крыльев")
            size_attr_uri = repo.add_class_attribute(dog_uri, "порода")
            iq_attr_uri = repo.add_class_attribute(human_uri, "интеллект")
            
            # Добавляем object properties и получаем их URI
            parent_prop_uri = repo.add_class_object_attribute(animal_uri, "имеет_родителя", animal_uri)
            living_in_uri = repo.add_class_object_attribute(animal_uri, "живет_в", habitat_uri)
            

            trained_by_prop_uri = repo.add_class_object_attribute(dog_uri, "дрессируется_у", human_uri)
            
            # Получаем сигнатуры
            dog_signature = repo.collect_signature(dog_uri)
            print(f"✓ Сигнатура класса Собака:")
            print(f"  - Datatype properties: {[p.title for p in dog_signature.params]}")
            print(f"  - Object properties: {[p.title for p in dog_signature.obj_params]}")
            
            animal_signature = repo.collect_signature(animal_uri)
            print(f"✓ Сигнатура класса Животное:")
            print(f"  - Datatype properties: {[p.title for p in animal_signature.params]}")
            print(f"  - Object properties: {[p.title for p in animal_signature.obj_params]}")
            
            print("\n6. СОЗДАНИЕ ОБЪЕКТОВ:")
            print("-" * 40)
            
            # Создаем объекты и получаем их URI
            house_uri = repo.create_object(habitat_uri, "Дом")
            budka_uri = repo.create_object(habitat_uri, "Будка")

            matvey_uri = repo.create_object(
                human_uri,
                "Матвей", 
                "Пушистая домашняя кошка",
                properties={"продолжительность_жизни": 80},
                object_properties={"живет_в": house_uri}
            )
            rex_uri = repo.create_object(
                dog_uri, 
                "Рекс", 
                "Дружелюбная собака породы овчарка",
                properties={"продолжительность_жизни": 18},
                object_properties={"живет_в": budka_uri, "дрессируется_у": matvey_uri}
            )

            # Проверяем получение объектов
            rex_obj = repo.get_object(rex_uri)
            if rex_obj:
                print(f"✓ Получен объект: {rex_obj.title} - {rex_obj.description}")

            # # Обновляем класс
            # repo.update_class(dog_uri, "Собака - домашнее животное", "Дружелюбное домашнее животное, друг человека")
          
            # # Обновляем объект
            # repo.update_object(
            #     rex_uri, 
            #     title="Рекс Великий",
            #     description="Очень умная и преданная собака"
            # )
            # updated_rex = repo.get_object(rex_uri)
            
            # Получаем всю онтологию
            # ontology = repo.get_ontology()
            # print(f"✓ Полная онтология системы:")
            # print(f"  - Сигнатур классов: {len(ontology.signatures)}")
            # print(f"  - Объектов: {len(ontology.objects)}")
            
            # # Показываем информацию о сигнатурах
            # for signature in ontology.signatures:
            #     class_obj = repo.get_class(signature.uri)
            #     if class_obj:
            #         print(f"  - Класс '{class_obj.title}': {len(signature.params)} datatype props, {len(signature.obj_params)} object props")
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()