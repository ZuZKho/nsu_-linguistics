#!/bin/bash

BASE_URL="http://127.0.0.1:8000/api"

# Цвета для вывода
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}🐾 Создаем онтологию животных через API${NC}"
echo "=========================================="

# Функция для извлечения URI из JSON ответа через Python
extract_uri() {
    local json_response="$1"
    echo "$json_response" | python3 -c "
import sys, json
try:
    data = json.loads(sys.stdin.read())
    print(data.get('uri', ''))
except Exception as e:
    print('')
"
}

# Функция для выполнения запросов
api_request() {
    local method=$1
    local url=$2
    local data=$3
    local description=$4
    
    echo -e "${YELLOW}${description}${NC}"
    
    if [ "$method" = "POST" ]; then
        response=$(curl -s -X POST -H "Content-Type: application/json" -d "$data" -w "|%{http_code}" "$url")
    elif [ "$method" = "GET" ]; then
        response=$(curl -s -w "|%{http_code}" "$url")
    fi
    
    body=$(echo "$response" | sed 's/|.*//')
    status_code=$(echo "$response" | sed 's/.*|//')
    
    if [ "$status_code" -eq 200 ] || [ "$status_code" -eq 201 ]; then
        echo -e "${GREEN}✅ УСПЕХ${NC}"
        echo "$body"
        return 0
    else
        echo -e "${RED}❌ ОШИБКА: $status_code${NC}"
        echo "$body"
        return 1
    fi
    echo "---"
}

# Переменные для хранения URI
ANIMAL_URI=""
MAMMAL_URI=""
BIRD_URI=""
HUMAN_URI=""
DOG_URI=""
HABITAT_URI=""
HOUSE_URI=""
BUDKA_URI=""
MATVEY_URI=""
REX_URI=""

echo -e "${BLUE}1. СОЗДАНИЕ КЛАССОВ:${NC}"

# Создаем корневой класс и получаем его URI через Python
echo -e "${YELLOW}Создаем класс 'Животное'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d '{
  "title": "Животное",
  "description": "Базовый класс для всех животных"
}' "$BASE_URL/classes/")

ANIMAL_URI=$(extract_uri "$response")
echo -e "${GREEN}✅ Создан класс Животное: $ANIMAL_URI${NC}"

# Создаем дочерние классы
echo -e "${YELLOW}Создаем класс 'Млекопитающее'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d "{
  \"title\": \"Млекопитающее\",
  \"description\": \"Класс млекопитающих\",
  \"parent_uri\": \"$ANIMAL_URI\"
}" "$BASE_URL/classes/")

MAMMAL_URI=$(extract_uri "$response")
echo -e "${GREEN}✅ Создан класс Млекопитающее: $MAMMAL_URI${NC}"

echo -e "${YELLOW}Создаем класс 'Птица'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d "{
  \"title\": \"Птица\",
  \"description\": \"Класс птиц\", 
  \"parent_uri\": \"$ANIMAL_URI\"
}" "$BASE_URL/classes/")

BIRD_URI=$(extract_uri "$response")
echo -e "${GREEN}✅ Создан класс Птица: $BIRD_URI${NC}"

echo -e "${YELLOW}Создаем класс 'Человек'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d "{
  \"title\": \"Человек\",
  \"description\": \"Класс людей\",
  \"parent_uri\": \"$MAMMAL_URI\"
}" "$BASE_URL/classes/")

HUMAN_URI=$(extract_uri "$response")
echo -e "${GREEN}✅ Создан класс Человек: $HUMAN_URI${NC}"

echo -e "${YELLOW}Создаем класс 'Собака'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d "{
  \"title\": \"Собака\", 
  \"description\": \"Класс собак\",
  \"parent_uri\": \"$MAMMAL_URI\"
}" "$BASE_URL/classes/")

DOG_URI=$(extract_uri "$response")
echo -e "${GREEN}✅ Создан класс Собака: $DOG_URI${NC}"

echo -e "${YELLOW}Создаем класс 'Среда обитания'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d '{
  "title": "Среда обитания",
  "description": "Среда обитания"
}' "$BASE_URL/classes/")

HABITAT_URI=$(extract_uri "$response")
echo -e "${GREEN}✅ Создан класс Среда обитания: $HABITAT_URI${NC}"

echo -e "${BLUE}2. ДОБАВЛЕНИЕ DATATYPE PROPERTIES:${NC}"

# Добавляем datatype properties
echo -e "${YELLOW}Добавляем атрибут 'количество_ног'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d '{
  "datatype_title": "количество_ног"
}' "$BASE_URL/classes/$ANIMAL_URI/attributes/")
attr_uri=$(extract_uri "$response")
if [ -n "$attr_uri" ]; then
    echo -e "${GREEN}✅ Атрибут добавлен: $attr_uri${NC}"
else
    echo -e "${RED}❌ Ошибка при добавлении атрибута${NC}"
fi

echo -e "${YELLOW}Добавляем атрибут 'продолжительность_жизни'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d '{
  "datatype_title": "продолжительность_жизни"
}' "$BASE_URL/classes/$ANIMAL_URI/attributes/")
attr_uri=$(extract_uri "$response")
if [ -n "$attr_uri" ]; then
    echo -e "${GREEN}✅ Атрибут добавлен: $attr_uri${NC}"
fi

echo -e "${YELLOW}Добавляем атрибут 'размах_крыльев'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d '{
  "datatype_title": "размах_крыльев"
}' "$BASE_URL/classes/$BIRD_URI/attributes/")
attr_uri=$(extract_uri "$response")
if [ -n "$attr_uri" ]; then
    echo -e "${GREEN}✅ Атрибут добавлен: $attr_uri${NC}"
fi

echo -e "${YELLOW}Добавляем атрибут 'порода'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d '{
  "datatype_title": "порода"
}' "$BASE_URL/classes/$DOG_URI/attributes/")
attr_uri=$(extract_uri "$response")
if [ -n "$attr_uri" ]; then
    echo -e "${GREEN}✅ Атрибут добавлен: $attr_uri${NC}"
fi

echo -e "${YELLOW}Добавляем атрибут 'интеллект'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d '{
  "datatype_title": "интеллект"
}' "$BASE_URL/classes/$HUMAN_URI/attributes/")
attr_uri=$(extract_uri "$response")
if [ -n "$attr_uri" ]; then
    echo -e "${GREEN}✅ Атрибут добавлен: $attr_uri${NC}"
fi

echo -e "${BLUE}3. ДОБАВЛЕНИЕ OBJECT PROPERTIES:${NC}"

# Добавляем object properties
echo -e "${YELLOW}Добавляем связь 'имеет_родителя'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d "{
  \"attr_name\": \"имеет_родителя\",
  \"range_class_uri\": \"$ANIMAL_URI\"
}" "$BASE_URL/classes/$ANIMAL_URI/object-attributes/")
obj_attr_uri=$(extract_uri "$response")
if [ -n "$obj_attr_uri" ]; then
    echo -e "${GREEN}✅ Связь добавлена: $obj_attr_uri${NC}"
fi

echo -e "${YELLOW}Добавляем связь 'живет_в'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d "{
  \"attr_name\": \"живет_в\",
  \"range_class_uri\": \"$HABITAT_URI\"
}" "$BASE_URL/classes/$ANIMAL_URI/object-attributes/")
obj_attr_uri=$(extract_uri "$response")
if [ -n "$obj_attr_uri" ]; then
    echo -e "${GREEN}✅ Связь добавлена: $obj_attr_uri${NC}"
fi

echo -e "${YELLOW}Добавляем связь 'дрессируется_у'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d "{
  \"attr_name\": \"дрессируется_у\",
  \"range_class_uri\": \"$HUMAN_URI\"
}" "$BASE_URL/classes/$DOG_URI/object-attributes/")
obj_attr_uri=$(extract_uri "$response")
if [ -n "$obj_attr_uri" ]; then
    echo -e "${GREEN}✅ Связь добавлена: $obj_attr_uri${NC}"
fi

echo -e "${BLUE}4. ПОЛУЧЕНИЕ СИГНАТУР:${NC}"

# Получаем сигнатуры
echo -e "${YELLOW}Получаем сигнатуру класса Собака...${NC}"
curl -s "$BASE_URL/classes/$DOG_URI/signature/" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print('Datatype properties:', [p['title'] for p in data.get('params', [])])
    print('Object properties:', [p['title'] for p in data.get('obj_params', [])])
except Exception as e:
    print('Ошибка:', e)
"

echo -e "${YELLOW}Получаем сигнатуру класса Животное...${NC}"
curl -s "$BASE_URL/classes/$ANIMAL_URI/signature/" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print('Datatype properties:', [p['title'] for p in data.get('params', [])])
    print('Object properties:', [p['title'] for p in data.get('obj_params', [])])
except Exception as e:
    print('Ошибка:', e)
"

echo -e "${BLUE}5. СОЗДАНИЕ ОБЪЕКТОВ:${NC}"

# Создаем объекты сред обитания
echo -e "${YELLOW}Создаем объект 'Дом'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d "{
  \"class_uri\": \"$HABITAT_URI\",
  \"title\": \"Дом\",
  \"description\": \"Дом для проживания\"
}" "$BASE_URL/objects/")

HOUSE_URI=$(extract_uri "$response")
echo -e "${GREEN}✅ Создан объект Дом: $HOUSE_URI${NC}"

echo -e "${YELLOW}Создаем объект 'Будка'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d "{
  \"class_uri\": \"$HABITAT_URI\",
  \"title\": \"Будка\", 
  \"description\": \"Будка для собаки\"
}" "$BASE_URL/objects/")

BUDKA_URI=$(extract_uri "$response")
echo -e "${GREEN}✅ Создан объект Будка: $BUDKA_URI${NC}"

# Создаем объект человека
echo -e "${YELLOW}Создаем объект 'Матвей'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d "{
  \"class_uri\": \"$HUMAN_URI\",
  \"title\": \"Матвей\",
  \"description\": \"Человек который дрессирует собак\",
  \"properties\": {\"продолжительность_жизни\": 80},
  \"object_properties\": {\"живет_в\": \"$HOUSE_URI\"}
}" "$BASE_URL/objects/")

MATVEY_URI=$(extract_uri "$response")
echo -e "${GREEN}✅ Создан объект Матвей: $MATVEY_URI${NC}"

# Создаем объект собаки
echo -e "${YELLOW}Создаем объект 'Рекс'...${NC}"
response=$(curl -s -X POST -H "Content-Type: application/json" -d "{
  \"class_uri\": \"$DOG_URI\",
  \"title\": \"Рекс\",
  \"description\": \"Дружелюбная собака породы овчарка\",
  \"properties\": {\"продолжительность_жизни\": 18},
  \"object_properties\": {
    \"живет_в\": \"$BUDKA_URI\",
    \"дрессируется_у\": \"$MATVEY_URI\"
  }
}" "$BASE_URL/objects/")

REX_URI=$(extract_uri "$response")
echo -e "${GREEN}✅ Создан объект Рекс: $REX_URI${NC}"

echo -e "${BLUE}6. ПРОВЕРКА СОЗДАННЫХ ОБЪЕКТОВ:${NC}"

# Проверяем получение объектов через Python
echo -e "${YELLOW}Получаем информацию об объекте Рекс...${NC}"
curl -s "$BASE_URL/objects/$REX_URI/" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f\"Объект: {data.get('title')}\")
    print(f\"Описание: {data.get('description')}\")
    print(f\"Свойства: {data.get('properties', {})}\")
except Exception as e:
    print('Ошибка:', e)
"

echo -e "${YELLOW}Получаем информацию об объекте Матвей...${NC}"
curl -s "$BASE_URL/objects/$MATVEY_URI/" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    print(f\"Объект: {data.get('title')}\")
    print(f\"Описание: {data.get('description')}\") 
    print(f\"Свойства: {data.get('properties', {})}\")
except Exception as e:
    print('Ошибка:', e)
"

echo -e "${BLUE}7. ФИНАЛЬНАЯ ПРОВЕРКА:${NC}"

# Получаем всю онтологию через Python
echo -e "${YELLOW}Получаем всю онтологию...${NC}"
curl -s "$BASE_URL/ontology/" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    signatures = data.get('signatures', [])
    objects = data.get('objects', [])
    print(f'Всего сигнатур: {len(signatures)}')
    print(f'Всего объектов: {len(objects)}')
    print('Первые 3 сигнатуры:')
    for sig in signatures[:3]:
        print(f'  - {sig.get(\"uri\")}')
    print('Первые 3 объекта:')
    for obj in objects[:3]:
        print(f'  - {obj.get(\"title\")}')
except Exception as e:
    print('Ошибка:', e)
"

echo -e "${GREEN}==========================================${NC}"
echo -e "${GREEN}✅ ОНТОЛОГИЯ ЖИВОТНЫХ УСПЕШНО СОЗДАНА!${NC}"
echo -e "${GREEN}==========================================${NC}"

# Сохраняем URI в файл для последующего использования
cat > animal_ontology_uris.txt << EOF
ANIMAL_URI=$ANIMAL_URI
MAMMAL_URI=$MAMMAL_URI
BIRD_URI=$BIRD_URI
HUMAN_URI=$HUMAN_URI
DOG_URI=$DOG_URI
HABITAT_URI=$HABITAT_URI
HOUSE_URI=$HOUSE_URI
BUDKA_URI=$BUDKA_URI
MATVEY_URI=$MATVEY_URI
REX_URI=$REX_URI
EOF

echo -e "${YELLOW}📁 URI сохранены в файл: animal_ontology_uris.txt${NC}"