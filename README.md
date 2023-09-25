## Run app

1. Copy .env.example to .env and set vars  
2. Run:  

    `poetry install`

    `poetry run alembic upgrade head`

    `poetry run hypercorn src/main:app -b 0.0.0.0:8000`

## Run tests

`poetry run pytest tests`

## Generate migration

`alembic revision --autogenerate -m ""`

## pyproject.toml sort:

`poetry run toml-sort pyproject.toml --all --in-place`

## Run formatter
`python3 -m black .`

## Run linters
    python3 -m flake8 --config setup.cfg .
    python3 -m mypy  --disallow-untyped-defs ./


## Дополнительные требования (отметьте [Х] выбранные пункты):

- [ ] (1 балл) Реализуйте метод `GET /ping`, который возвращает информацию о статусе доступности БД.
- [ ] (1 балл) Реализуйте возможность «удаления» сохранённого URL. Запись должна остаться, но помечаться как удалённая. При попытке получения полного URL возвращать ответ с кодом `410 Gone`.
- [Х] (2 балла) Реализуйте middlware, блокирующий доступ к сервису из запрещённых подсетей (black list).
- [Х] (2 балла) Реализуйте возможность передавать ссылки пачками (batch upload).
