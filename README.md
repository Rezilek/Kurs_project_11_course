# Образовательная платформа на Django DRF

## Описание
API для образовательной платформы с курсами, уроками и системой платежей.

## Функционал
- Кастомная модель пользователя (авторизация по email)
- Курсы и уроки с CRUD операциями
- Система платежей (Payment модель)
- Фильтрация и сортировка платежей
- Расширенные сериализаторы с дополнительными полями

## Установка
1. Клонировать репозиторий
2. Создать виртуальное окружение: `python -m venv venv`
3. Активировать: `venv\Scripts\activate` (Windows)
4. Установить зависимости: `pip install -r requirements.txt`
5. Настроить .env файл: cp .env.example .env
   Отредактировать .env с вашими настройками PostgreSQL
6. Создать базу данных PostgreSQL: `createdb -U postgres kurs_project_db`
5. Применить миграции: `python manage.py migrate`
6. Создать суперпользователя: `python manage.py createsuperuser`
7. Запустить сервер: `python manage.py runserver`

## API Endpoints
- `/api/` - корень API
- `/api/courses/` - курсы (с уроками и их количеством)
- `/api/lessons/` - уроки
- `/api/users/` - пользователи (с историей платежей)
- `/api/users/payments/` - платежи с фильтрацией

## Фильтрация платежей
- `?paid_course=1` - платежи за конкретный курс
- `?paid_lesson=1` - платежи за конкретный урок  
- `?payment_method=transfer` - платежи по методу оплаты
- `?ordering=-payment_date` - сортировка по дате

Примеры
text
# Комбинированная фильтрация
GET /api/users/payments/?paid_course=1&payment_method=transfer&ordering=-payment_date

# Конкретный пользователь с историей платежей
GET /api/users/users/1/

# Структура проекта
project/
├── config/           # Настройки Django
├── users/           # Приложение пользователей
├── courses/         # Приложение курсов
├── .env             # Переменные окружения
├── .env.example     # Шаблон .env
└── requirements.txt # Зависимости
