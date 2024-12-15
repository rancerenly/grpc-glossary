# Проект глоссария с использованием gRPC
Этот проект представляет собой приложение для создания и управления глоссарием терминов с использованием gRPC. Приложение позволяет добавлять, получать, обновлять и удалять термины через gRPC API.

## Особенности
- Возможность добавлять, получать, обновлять и удалять термины глоссария с помощью gRPC.
- Простой клиент для взаимодействия с сервером.
- Реализовано с использованием Python и библиотеки `grpcio`.

## Установка и развертывание

### 1. Клонирование репозитория

```bash
git clone https://github.com/rancerenly/grpc-glossary.git
cd grpc-glossary
```

### 2. Запуск с Docker
```bash
docker-compose up --build
```

### 3. Зависимости
Для запуска проекта локально без Docker:

```bash
python -m venv venv

source venv/bin/activate # Для Linux/macOS
venv\Scripts\activate # Для Windows

pip install -r requirements.txt
```

### 4. Запуск сервера
```bash
python server.py
```
### 5. Запуск клиента
```bash
python client.py
```

### 6. Методы:

```python
class GlossaryServiceServicer(glossary_pb2_grpc.GlossaryServiceServicer):
    # Добавление
    def AddTerm(self, request, context):
        if request.keyword in terms_db:
            return glossary_pb2.Response(message="Термин уже существует")
        terms_db[request.keyword] = request.description
        return glossary_pb2.Response(message="Термин успешно добавлен")

    # Получение
    def GetTerm(self, request, context):
        term = terms_db.get(request.keyword)
        if term is None:
            return glossary_pb2.Term(keyword=request.keyword, description="Термин не найден")
        return glossary_pb2.Term(keyword=request.keyword, description=term)

    # Получение всех
    def GetTerms(self, request, context):
        terms_list = [glossary_pb2.Term(keyword=key, description=value) for key, value in terms_db.items()]
        return glossary_pb2.TermsList(terms=terms_list)
    
    # Обновление
    def UpdateTerm(self, request, context):
        if request.keyword not in terms_db:
            return glossary_pb2.Response(message="Термин не найден")
        terms_db[request.keyword] = request.description
        return glossary_pb2.Response(message="Термин успешно обновлен")
    
    # Удаление
    def DeleteTerm(self, request, context):
        if request.keyword not in terms_db:
            return glossary_pb2.Response(message="Термин не найден")
        del terms_db[request.keyword]
        return glossary_pb2.Response(message="Термин успешно удален")
```
### 6. Пример запросов с клиентом:
```python
response = stub.AddTerm(glossary_pb2.Term(keyword="Асинхронный рендеринг", description="Рендеринг, который не блокирует основной поток выполнения приложения"))
print("AddTerm:", response.message)

response = stub.GetTerm(glossary_pb2.KeywordRequest(keyword="Python"))
print("GetTerm:", response.keyword, response.description)

response = stub.GetTerms(glossary_pb2.Empty())
for term in response.terms:
    print(f"Term: {term.keyword} - {term.description}")

response = stub.UpdateTerm(glossary_pb2.Term(keyword="Python", description="Популярный язык программирования"))
print("UpdateTerm:", response.message)

response = stub.DeleteTerm(glossary_pb2.KeywordRequest(keyword="Python"))
print("DeleteTerm:", response.message)
```
