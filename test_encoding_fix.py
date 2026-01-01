# test_encoding_fix.py
import requests
import json
import sys


def print_section(title):
    print(f"\n{'=' * 60}")
    print(f" {title}")
    print(f"{'=' * 60}")


def test_api_encoding():
    base_url = "http://localhost:8000"

    print_section("ТЕСТИРОВАНИЕ КОДИРОВКИ API")

    # Тест 1: Проверка доступности сервера
    try:
        response = requests.get(f"{base_url}/admin/", timeout=5)
        print("✓ Сервер доступен")
    except requests.exceptions.ConnectionError:
        print("✗ Сервер не доступен. Запустите: python manage.py runserver")
        return

    # Тест 2: Получение токена
    print_section("1. ПОЛУЧЕНИЕ JWT ТОКЕНА")

    # Попробуем несколько вариантов учетных данных
    test_credentials = [
        {"email": "admin@example.com", "password": "admin"},
        {"email": "test@example.com", "password": "testpass123"},
        {"email": "user@example.com", "password": "user123"},
    ]

    access_token = None
    for creds in test_credentials:
        try:
            response = requests.post(
                f"{base_url}/api/users/token/",
                json=creds,
                headers={"Content-Type": "application/json"},
                timeout=5
            )

            if response.status_code == 200:
                token_data = response.json()
                access_token = token_data.get("access")
                print(f"✓ Успешный вход: {creds['email']}")
                print(f"  Token получен: {access_token[:30]}...")
                break
            else:
                print(f"✗ Не удалось войти как {creds['email']}: {response.status_code}")
        except Exception as e:
            print(f"✗ Ошибка для {creds['email']}: {e}")

    if not access_token:
        print("✗ Не удалось получить токен. Создайте пользователя:")
        print("  python manage.py createsuperuser")
        print("  или")
        print("  python manage.py shell")
        print('''
from users.models import User
user = User.objects.create_user(
    email="test@example.com",
    password="testpass123",
    first_name="Тест",
    city="Москва"
)
''')
        return

    # Тест 3: Получение профиля
    print_section("2. ПОЛУЧЕНИЕ ПРОФИЛЯ")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json; charset=utf-8"
    }

    try:
        response = requests.get(
            f"{base_url}/api/users/me/",
            headers=headers,
            timeout=5
        )

        print(f"Статус: {response.status_code}")
        print(f"Кодировка ответа: {response.encoding}")
        print(f"Content-Type: {response.headers.get('Content-Type')}")

        if response.status_code == 200:
            print("✓ Профиль получен успешно")

            # Покажем сырой ответ
            raw_text = response.text[:500]
            print(f"\nСырой ответ (первые 500 символов):")
            print(f"'{raw_text}'")

            # Парсим JSON
            try:
                data = response.json()
                print(f"\nJSON данные:")
                print(json.dumps(data, ensure_ascii=False, indent=2))

                # Проверяем существующие русские символы
                if data.get("city"):
                    print(f"\n✓ Город в профиле: '{data['city']}'")
                    print(f"  Тип: {type(data['city'])}")
                    print(f"  Репрезентация: {repr(data['city'])}")
            except json.JSONDecodeError as e:
                print(f"✗ Ошибка парсинга JSON: {e}")
        else:
            print(f"✗ Ошибка: {response.text}")

    except Exception as e:
        print(f"✗ Ошибка запроса: {e}")

    # Тест 4: Обновление с русскими символами
    print_section("3. ОБНОВЛЕНИЕ С РУССКИМИ СИМВОЛАМИ")

    update_data = {
        "city": "Санкт-Петербург",
        "phone": "+7 (999) 123-45-67",
        "first_name": "Иван",
        "last_name": "Петров"
    }

    print(f"Отправляемые данные: {json.dumps(update_data, ensure_ascii=False)}")

    try:
        response = requests.patch(
            f"{base_url}/api/users/me/",
            json=update_data,
            headers=headers,
            timeout=5
        )

        print(f"Статус обновления: {response.status_code}")

        if response.status_code == 200:
            print("✓ Профиль обновлен успешно")

            updated_data = response.json()
            print(f"\nОбновленные данные:")
            print(json.dumps(updated_data, ensure_ascii=False, indent=2))

            # Проверка
            if updated_data.get("city") == "Санкт-Петербург":
                print("✓ Русские символы корректно сохранены и возвращены!")
            else:
                print(f"✗ Проблема: ожидалось 'Санкт-Петербург', получено '{updated_data.get('city')}'")
        else:
            print(f"✗ Ошибка обновления: {response.text}")

    except Exception as e:
        print(f"✗ Ошибка запроса: {e}")

    # Тест 5: Создание курса с русским названием
    print_section("4. СОЗДАНИЕ КУРСА С РУССКИМ НАЗВАНИЕМ")

    course_data = {
        "title": "Программирование на Python",
        "description": "Изучение основ программирования на языке Python",
        "price": 10000
    }

    try:
        response = requests.post(
            f"{base_url}/api/courses/courses/",
            json=course_data,
            headers=headers,
            timeout=5
        )

        print(f"Статус создания курса: {response.status_code}")

        if response.status_code == 201:
            course = response.json()
            print("✓ Курс создан успешно")
            print(json.dumps(course, ensure_ascii=False, indent=2))

            # Проверка
            if course.get("title") == "Программирование на Python":
                print("✓ Русское название курса сохранено корректно!")
            else:
                print(f"✗ Проблема с названием курса")
        else:
            print(f"✗ Ошибка создания курса: {response.text}")

    except Exception as e:
        print(f"✗ Ошибка запроса: {e}")


if __name__ == "__main__":
    test_api_encoding()