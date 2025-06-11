# WEAREWAY Test Task

## Описание

**Цель:** разработать сервис на FastAPI для семантического поиска отзывов в базе данных IMDB.

**Основные задачи:**

* Дообучить модель DistilBERT на датасете отзывов IMDB
* Сохранить векторные представления текстов в базе данных PostgreSQL
* Реализовать асинхронный pipeline с использованием Celery и Redis
* Предоставить REST API для поиска отзывов, схожих по смыслу

---

## Архитектура проекта

Проект реализован с соблюдением принципов чистой архитектуры и состоит из следующих компонентов:

1. **Entities** — бизнес-сущности и их модели
2. **Usecases** — бизнес-логика, взаимодействующая с интерфейсами (база данных, кэш, embedder)
3. **Infrastructure** — конкретные реализации интерфейсов (PostgreSQL, Redis, модель Transformers)

---

## Развёртывание

### Настройка окружения

1. Создайте файл `.env` в корне проекта со следующими переменными:

```txt
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=db
REDIS_PASSWORD=password
```

2. Поместите дообученную модель DistilBERT в папку `models` в корне проекта.

3. Настройте файл `service_config.json` со следующими параметрами:

```json
{
  "embedder_config": {
    "model_path": "models/distilbert-finetuned",
    "device": "cpu"
  },
  "postgres_config": {
    "host": "postgres",
    "port": 5432,
    "user": "user",
    "password": "password",
    "db_name": "db"
  },
  "redis_config": {
    "host": "redis",
    "port": 6379,
    "password": "password",
    "db": 0
  }
}
```

### Запуск

Сервисы развёртываются с помощью Docker Compose:

```bash
docker-compose up -d
```

В результате будут запущены:

* Сервер FastAPI
* Celery воркеры
* База данных PostgreSQL
* Сервер Redis

---

## Дообучение ML-модели

Скрипт для обучения модели расположен в `scripts/finetune_model.py`.

Модель DistilBERT была дообучена на датасете IMDB (отзывы пользователей). Обучение проводилось на GPU (NVIDIA GeForce RTX 2080 Ti) и заняло около 10 минут (2 эпохи).

Для запуска скрипта необходимо установить зависимости из файла `requirements/finetuning_requirements.txt`

---

## Загрузка датасета

Скрипт загрузки отзывов в базу данных находится в `scripts/upload_dataset.py`.

Перед запуском убедитесь, что сервер запущен, так как скрипт отправляет POST-запросы на endpoint `/api/v1/reviews/add`.

Загрузка происходит асинхронно, благодаря чему вставка 1000 отзывов занимает около 12 секунд.

Необходимые зависимости описаны в файле `requirements/upload_requirements.txt`
