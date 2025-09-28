from pprint import pprint
from ontology_driver.driver import OntologyRepository

# ТЕСТОВЫЙ ЗАПУСК
if __name__ == "__main__":
    print("=== ТЕСТОВЫЙ ЗАПУСК ONTOLOGY REPOSITORY ===\n")
    
    # Настройки подключения к Neo4j
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USER = "neo4j"
    NEO4J_PASSWORD = "password"
    
    try:
        with OntologyRepository(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD) as repo:
            
            print("1. СОЗДАНИЕ ИЕРАРХИИ КЛАССОВ:")
            print("-" * 40)
            
            # Создаем корневой класс и получаем его URI
            animal_uri = repo.create_class("Животное", "Базовый класс для всех животных")
            print(f"✓ Создан класс: Животное (URI: {animal_uri})")
            
            # Создаем дочерние классы
            mammal_uri = repo.create_class("Млекопитающее", "Класс млекопитающих", animal_uri)
            bird_uri = repo.create_class("Птица", "Класс птиц", animal_uri)
            print(f"✓ Созданы дочерние классы:")
            print(f"  - Млекопитающее (URI: {mammal_uri})")
            print(f"  - Птица (URI: {bird_uri})")
            
            # Создаем конкретные классы
            dog_uri = repo.create_class("Собака", "Класс собак", mammal_uri)
            cat_uri = repo.create_class("Кошка", "Класс кошек", mammal_uri)
            eagle_uri = repo.create_class("Орел", "Класс орлов", bird_uri)
            print(f"✓ Созданы конкретные классы:")
            print(f"  - Собака (URI: {dog_uri})")
            print(f"  - Кошка (URI: {cat_uri})")
            print(f"  - Орел (URI: {eagle_uri})")
            
            print("\n2. ДОБАВЛЕНИЕ АТРИБУТОВ КЛАССОВ:")
            print("-" * 40)
            
            # Добавляем datatype properties и получаем их URI
            legs_attr_uri = repo.add_class_attribute(animal_uri, "количество_ног")
            habitat_attr_uri = repo.add_class_attribute(animal_uri, "среда_обитания")
            lifespan_attr_uri = repo.add_class_attribute(animal_uri, "продолжительность_жизни")
            diet_attr_uri = repo.add_class_attribute(mammal_uri, "тип_питания")
            wingspan_attr_uri = repo.add_class_attribute(bird_uri, "размах_крыльев")
            size_attr_uri = repo.add_class_attribute(dog_uri, "размер")
            fur_attr_uri = repo.add_class_attribute(cat_uri, "тип_шерсти")
            
            print("✓ Добавлены datatype properties:")
            print(f"  - количество_ног (URI: {legs_attr_uri})")
            print(f"  - среда_обитания (URI: {habitat_attr_uri})")
            print(f"  - продолжительность_жизни (URI: {lifespan_attr_uri})")
            print(f"  - тип_питания (URI: {diet_attr_uri})")
            print(f"  - размах_крыльев (URI: {wingspan_attr_uri})")
            print(f"  - размер (URI: {size_attr_uri})")
            print(f"  - тип_шерсти (URI: {fur_attr_uri})")
            
            print("\n3. ДОБАВЛЕНИЕ ОБЪЕКТНЫХ СВОЙСТВ:")
            print("-" * 40)
            
            # Добавляем object properties и получаем их URI
            parent_prop_uri = repo.add_class_object_attribute(animal_uri, "имеет_родителя", animal_uri)
            lives_in_prop_uri = repo.add_class_object_attribute(animal_uri, "живет_в", animal_uri)
            trained_by_prop_uri = repo.add_class_object_attribute(dog_uri, "дрессируется_у", animal_uri)
            
            print("✓ Добавлены object properties:")
            print(f"  - имеет_родителя (URI: {parent_prop_uri})")
            print(f"  - живет_в (URI: {lives_in_prop_uri})")
            print(f"  - дрессируется_у (URI: {trained_by_prop_uri})")
            
            print("\n4. ПРОВЕРКА СТРУКТУРЫ КЛАССОВ:")
            print("-" * 40)
            
            # Проверяем получение классов
            dog_class = repo.get_class(dog_uri)
            if dog_class:
                print(f"✓ Получен класс: {dog_class.title} - {dog_class.description}")
            
            # Проверяем родителей
            dog_parents = repo.get_class_parents(dog_uri)
            print(f"✓ Родители класса Собака: {[p.title for p in dog_parents]}")
            
            # Проверяем детей
            mammal_children = repo.get_class_children(mammal_uri)
            mammal_child_titles = [c.title for c in mammal_children if hasattr(c, 'title')]
            print(f"✓ Дети класса Млекопитающее: {mammal_child_titles}")
            
            # Проверяем корневые классы
            root_classes = repo.get_ontology_parent_classes()
            print(f"✓ Корневые классы в системе: {[cls.title for cls in root_classes]}")
            
            print("\n5. ТЕСТИРОВАНИЕ СИГНАТУР:")
            print("-" * 40)
            
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
            rex_uri = repo.create_object(
                dog_uri, 
                "Рекс", 
                "Дружелюбная собака породы овчарка",
                properties={"размер": "большой", "количество_ног": 4},
                object_properties={"имеет_родителя": animal_uri}
            )
            print(f"✓ Создан объект собаки: Рекс (URI: {rex_uri})")
            
            murka_uri = repo.create_object(
                cat_uri,
                "Мурка", 
                "Пушистая домашняя кошка",
                properties={"тип_шерсти": "длинная", "количество_ног": 4, "продолжительность_жизни": 15}
            )
            print(f"✓ Создан объект кошки: Мурка (URI: {murka_uri})")
            
            # Проверяем получение объектов
            rex_obj = repo.get_object(rex_uri)
            if rex_obj:
                print(f"✓ Получен объект: {rex_obj.title} - {rex_obj.description}")
            
            print("\n7. ТЕСТИРОВАНИЕ ОБНОВЛЕНИЯ:")
            print("-" * 40)
            
            # Обновляем класс
            repo.update_class(dog_uri, "Собака - домашнее животное", "Дружелюбное домашнее животное, друг человека")
            updated_dog = repo.get_class(dog_uri)
            print(f"✓ Обновлен класс Собака:")
            print(f"  - Новое описание: {updated_dog.description}")
            
            # Обновляем объект
            repo.update_object(
                rex_uri, 
                title="Рекс Великий",
                description="Очень умная и преданная собака",
                properties={"размер": "очень большой"}
            )
            updated_rex = repo.get_object(rex_uri)
            if updated_rex:
                print(f"✓ Обновлен объект: {updated_rex.title} - {updated_rex.description}")
            
            print("\n8. ПОЛНАЯ ОНТОЛОГИЯ:")
            print("-" * 40)
            
            # Получаем всю онтологию
            ontology = repo.get_ontology()
            print(f"✓ Полная онтология системы:")
            print(f"  - Сигнатур классов: {len(ontology.signatures)}")
            print(f"  - Объектов: {len(ontology.objects)}")
            
            # Показываем информацию о сигнатурах
            for signature in ontology.signatures:
                class_obj = repo.get_class(signature.uri)
                if class_obj:
                    print(f"  - Класс '{class_obj.title}': {len(signature.params)} datatype props, {len(signature.obj_params)} object props")
            
            print("\n9. ТЕСТИРОВАНИЕ УДАЛЕНИЯ:")
            print("-" * 40)
            
            # Создаем временный класс для тестирования удаления
            temp_class_uri = repo.create_class("ВременныйКласс", "Класс для тестирования удаления", animal_uri)
            print(f"✓ Создан временный класс для теста удаления (URI: {temp_class_uri})")
            
            # Удаляем временный класс
            repo.delete_class(temp_class_uri)
            deleted_class = repo.get_class(temp_class_uri)
            if not deleted_class:
                print("✓ Временный класс успешно удален")
            
            print("\n" + "=" * 50)
            print("ТЕСТИРОВАНИЕ ЗАВЕРШЕНО УСПЕШНО!")
            print("=" * 50)
            
    except Exception as e:
        print(f"❌ Ошибка при тестировании: {e}")
        import traceback
        traceback.print_exc()