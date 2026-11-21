# Study service

Django + DRF сервис учебных сущностей: **materials**, **assignments**, **tests**. Полный CRUD, без авторизации (пока).

## Запуск
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
python manage.py test
```

## Документация
- Swagger UI: http://127.0.0.1:8000/api/docs/
- ReDoc: http://127.0.0.1:8000/api/redoc/
- OpenAPI: http://127.0.0.1:8000/api/schema/

## Эндпоинты (`/api/study/`)
Для каждой сущности: `GET /` (список), `POST /`, `GET /{id}/`, `PUT /{id}/`, `PATCH /{id}/`, `DELETE /{id}/`.

| Ресурс | URL | Поля |
|---|---|---|
| Material | `materials/` | title, description, content, url |
| Assignment | `assignments/` | title, description, material, due_date, max_score |
| Test | `tests/` | title, description, material, time_limit_minutes, passing_score, is_published |

Списки: пагинация (`?page=`), поиск (`?search=`), сортировка (`?ordering=-created_at`),
для assignments и tests — фильтр `?material=<id>`.
При удалении материала связанные задания и тесты сохраняются (`material` становится `null`).
# Study_service
