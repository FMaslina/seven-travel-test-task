# Task Management API

## Описание проекта
Task Management API - это RESTful API сервис для управления задачами, построенный с использованием FastAPI и SQLAlchemy. API позволяет создавать, просматривать, обновлять и удалять задачи (CRUD операции), а также отслеживать их статус выполнения.

## Технологический стек
- Python
- FastAPI
- SQLAlchemy
- Pydantic
- PostgreSQL (база данных)

## Функциональность
API предоставляет следующие возможности:
- Создание новых задач с заголовком и описанием
- Получение списка всех задач с возможностью пагинации
- Фильтрация задач по статусу
- Получение детальной информации о конкретной задаче
- Обновление существующих задач
- Удаление задач
- Автоматическое отслеживание времени создания и обновления задач

## Структура задачи
Каждая задача содержит следующие поля:
- `id`: уникальный идентификатор задачи
- `title`: заголовок задачи
- `description`: описание задачи
- `status`: статус задачи (todo, in_progress, done)
- `created_at`: дата и время создания
- `updated_at`: дата и время последнего обновления

## API Endpoints

### POST /tasks/
Создание новой задачи

### GET /tasks/
Получение списка задач
- Параметры:
  - `skip`: пропуск N первых задач (по умолчанию 0)
  - `limit`: максимальное количество задач в ответе (по умолчанию 100)
  - `status`: фильтрация по статусу (опционально)

### GET /tasks/{task_id}
Получение информации о конкретной задаче

### PUT /tasks/{task_id}
Обновление существующей задачи

### DELETE /tasks/{task_id}
Удаление задачи

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Настройте переменные окружения:
```bash
DATABASE_URL=postgresql://user:password@localhost/dbname
```

4. Примените миграции:
```bash
alembic upgrade head
```

5. Запустите сервер:
```bash
uvicorn main:app --reload
```

## Документация API
После запуска сервера, документация API доступна по следующим URL:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Примеры использования

### Создание новой задачи
```bash
curl -X POST "http://localhost:8000/tasks/" \
     -H "Content-Type: application/json" \
     -d '{"title": "Новая задача", "description": "Описание задачи"}'
```

### Получение списка задач
```bash
curl "http://localhost:8000/tasks/?limit=10&status=todo"
```