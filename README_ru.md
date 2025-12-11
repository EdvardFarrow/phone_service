# Phone Address Microservice

[![En](https://img.shields.io/badge/lang-en-grey.svg)](README.md)

![CI Status](https://github.com/EdvardFarrow/phone_service/actions/workflows/tests.yml/badge.svg)
![Coverage](./coverage.svg)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.124.2-009688.svg)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?&logo=redis&logoColor=white)


Высокопроизводительный асинхронный микросервис для управления связками "телефон-адрес".

---

## Функциональность

Сервис предоставляет REST API для операций CRUD:

- **GET** `/phones/{phone}` — Получение адреса по номеру (O(1)).
- **POST** `/phones` — Создание записи.
    - *Особенность:* Атомарная проверка дубликатов (`SET NX`).
- **PUT** `/phones/{phone}` — Обновление адреса.
    - *Особенность:* Обновляет только существующие записи (`SET XX`).
- **DELETE** `/phones/{phone}` — Удаление записи.

## Технологический стек

- **Core:** Python 3.12, FastAPI, Pydantic 2.0
- **Database:** Redis (Async)
- **Infrastructure:** Docker, Docker Compose
- **Testing:** Pytest, Fakeredis, Pytest-cov
- **Tools:** Makefile, Black, Flake8, GitHub Actions

---

## Установка и запуск

Проект полностью автоматизирован через `Makefile`.

### Вариант 1: Запуск в Docker (Рекомендуется)
Разворачивает изолированную среду с приложением и базой данных Redis.

```bash
# Сборка и запуск контейнеров в фоне
make up

# Просмотр логов
make logs

# Остановка
make down
```

API будет доступно по адресу: http://127.0.0.1:8000

### Вариант 2: Локальная разработка
Требует установленного Python 3.11+ и запущенного локально Redis.

```bash
# Установка зависимостей
make install

# Запуск сервера (с hot-reload)
make run
```

## Тестирование и Качество
В проекте реализованы интеграционные тесты с использованием fakeredis, что позволяет запускать их мгновенно без поднятия реальной БД.

```bash
# Запуск тестов + отчет о покрытии
make test

# Проверка стиля кода (Black + Flake8)
make lint
```

## Документация API
После запуска приложения документация доступна автоматически:
 * Swagger UI: http://127.0.0.1:8000/docs — интерактивное тестирование.

 * ReDoc: http://127.0.0.1:8000/redoc — документация для чтения.

## Структура проекта
```plaintext
.
├── app
│   ├── main.py        # Точка входа, роутинг и логи
│   ├── schemas.py     # Pydantic модели и валидация
│   ├── deps.py        # Зависимости (DI) и подключение к Redis
│   └── config.py      # Управление конфигурацией
├── tests              # Тесты (Pytest + Fakeredis)
├── docker-compose.yml # Оркестрация
├── Dockerfile         # Сборка образа
├── Makefile           # Автоматизация команд
└── requirements.txt   # Зависимости
```

