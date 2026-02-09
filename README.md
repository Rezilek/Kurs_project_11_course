# Образовательная платформа на Django

Проект для онлайн-обучения с Django REST Framework, Celery, Redis и PostgreSQL.

## Технологии
- Python 3.11 + Django 4.2
- Django REST Framework
- PostgreSQL 15
- Redis
- Celery + Celery Beat
- Gunicorn
- Docker + Docker Compose
- JWT аутентификация
- Stripe API для платежей
- Swagger/ReDoc документация

## Запуск проекта через Docker Compose

### Требования
- Docker 20.10+
- Docker Compose 2.20+
- Git

### Шаги для запуска

1. **Клонируйте репозиторий**
```bash
git clone https://github.com/Rezilek/Kurs_project_11_course.git
cd Kurs_project_11_course
Создайте файл .env на основе шаблона

bash
cp .env.example .env
Отредактируйте .env файл, указав свои значения (секретные ключи, пароли и т.д.)

Запустите проект

bash
docker-compose up -d
Выполните миграции и создайте суперпользователя

bash
# Выполнить миграции
docker-compose exec backend python manage.py migrate

# Создать суперпользователя
docker-compose exec backend python manage.py createsuperuser

# Собрать статику (если нужно)
docker-compose exec backend python manage.py collectstatic --no-input
Проверка работоспособности сервисов
Бэкенд (Django): http://localhost:8000

API документация (Swagger): http://localhost:8000/api/schema/swagger-ui/

API документация (ReDoc): http://localhost:8000/api/schema/redoc/

Админ-панель: http://localhost:8000/admin/

База данных (PostgreSQL): localhost:5432

Redis: localhost:6379

Управление контейнерами
bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f
docker-compose logs -f backend  # логи только бэкенда

# Пересборка контейнеров
docker-compose up -d --build

# Остановка и удаление volumes
docker-compose down -v
Сервисы проекта
Сервис	Порт	Описание
backend	8000	Django приложение с Gunicorn
db	5432	PostgreSQL база данных
redis	6379	Redis для кеша и Celery
celery_worker	-	Celery воркер для фоновых задач
celery_beat	-	Celery Beat для периодических задач
Переменные окружения
Скопируйте .env.example в .env и настройте:

bash
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=online_education
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Redis
REDIS_HOST=redis
REDIS_PORT=6379

# Celery
CELERY_BROKER_URL=redis://redis:6379/0

# Stripe (опционально)
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLIC_KEY=pk_test_...
Доступные команды
bash
# Запуск тестов
docker-compose exec backend python manage.py test

# Создание миграций
docker-compose exec backend python manage.py makemigrations

# Запуск shell
docker-compose exec backend python manage.py shell

# Проверка статуса Celery
docker-compose exec celery_worker celery -A config status
Разработка
Для разработки с горячей перезагрузкой:

bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
Структура проекта
text
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
├── backend/              # Django проект
│   ├── Dockerfile
│   ├── manage.py
│   └── config/
├── nginx/               # Конфигурация nginx (если есть)
└── celery/              # Конфигурация Celery
Лицензия
MIT