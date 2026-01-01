import requests
import json
import sys

def print_section(title):
    print(f'\n{'='*60}')
    print(f' {title}')
    print(f'{'='*60}')

def test_api():
    base_url = 'http://localhost:8000'
    
    print_section('ТСТ API С Т ')
    
    # 1. олучение токена
    print('1. олучение JWT токена:')
    login_data = {
        'email': 'test@example.com',
        'password': 'testpass123'
    }
    
    try:
        response = requests.post(
            f'{base_url}/api/users/token/',
            json=login_data,
            headers={
                'Content-Type': 'application/json; charset=utf-8'
            },
            timeout=10
        )
        
        print(f'   Статус: {response.status_code}')
        print(f'   Content-Type ответа: {response.headers.get(\"Content-Type\")}')
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data['access']
            print(f'   ✓ Токен получен: {access_token[:30]}...')
        else:
            print(f'   ✗ шибка: {response.text}')
            return
            
    except Exception as e:
        print(f'   ✗ сключение: {e}')
        return
    
    # 2. олучение профиля с разными заголовками
    headers_options = [
        {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'},
        {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json; charset=utf-8'},
        {'Authorization': f'Bearer {access_token}', 'Accept': 'application/json; charset=utf-8'},
        {'Authorization': f'Bearer {access_token}', 'Accept-Charset': 'utf-8'},
    ]
    
    for i, headers in enumerate(headers_options, 1):
        print_section(f'2.{i} апрос профиля (вариант {i})')
        print(f'   аголовки: {headers}')
        
        try:
            response = requests.get(
                f'{base_url}/api/users/me/',
                headers=headers,
                timeout=10
            )
            
            print(f'   Статус: {response.status_code}')
            print(f'   Content-Type: {response.headers.get(\"Content-Type\")}')
            print(f'   одировка ответа: {response.encoding}')
            
            # Сырой ответ
            raw_text = response.text
            print(f'\n   Сырой ответ (первые 300 символов):')
            print(f'   \"{raw_text[:300]}\"')
            
            # опробуем декодировать
            try:
                data = response.json()
                print(f'\n   JSON данные:')
                print(json.dumps(data, ensure_ascii=False, indent=2))
                
                # роверка русских символов
                if data.get('first_name'):
                    print(f'\n   роверка данных:')
                    print(f'   мя: \"{data['first_name']}\" (тип: {type(data['first_name'])})')
                    print(f'   Repr: {repr(data['first_name'])}')
                    
            except json.JSONDecodeError as e:
                print(f'   ✗ шибка JSON: {e}')
                
        except Exception as e:
            print(f'   ✗ сключение: {e}')
    
    # 3. Тест обновления
    print_section('3. бновление профиля')
    
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json; charset=utf-8'
    }
    
    update_data = {
        'first_name': 'лексей',
        'last_name': 'Сидоров',
        'city': 'катеринбург',
        'phone': '+7 (912) 345-67-89'
    }
    
    print(f'   тправляемые данные: {json.dumps(update_data, ensure_ascii=False)}')
    
    try:
        response = requests.patch(
            f'{base_url}/api/users/me/',
            json=update_data,
            headers=headers,
            timeout=10
        )
        
        print(f'   Статус: {response.status_code}')
        print(f'   Content-Type: {response.headers.get(\"Content-Type\")}')
        
        if response.status_code == 200:
            data = response.json()
            print(f'\n   бновленные данные:')
            print(json.dumps(data, ensure_ascii=False, indent=2))
            
            # роверка
            if (data.get('first_name') == 'лексей' and 
                data.get('city') == 'катеринбург'):
                print(f'\n   ✓ СС СЫ ТТ!')
            else:
                print(f'\n   ✗ роблема: данные не совпадают')
                
        else:
            print(f'   ✗ шибка: {response.text}')
            
    except Exception as e:
        print(f'   ✗ сключение: {e}')
    
    # 4. роверка в базе данных
    print_section('4. роверка в базе данных')
    
    import os
    import django
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()
    
    from django.db import connection
    from users.models import User
    
    user = User.objects.get(email='test@example.com')
    print(f'   ерез Django ORM:')
    print(f'   мя: \"{user.first_name}\"')
    print(f'   амилия: \"{user.last_name}\"')
    print(f'   ород: \"{user.city}\"')
    
    with connection.cursor() as cursor:
        cursor.execute('SELECT first_name, last_name, city FROM users_user WHERE email = %s', ['test@example.com'])
        row = cursor.fetchone()
        print(f'\n   ерез raw SQL:')
        print(f'   мя: \"{row[0]}\"')
        print(f'   амилия: \"{row[1]}\"')
        print(f'   ород: \"{row[2]}\"')

if __name__ == '__main__':
    # становим кодировку stdout
    sys.stdout.reconfigure(encoding='utf-8')
    test_api()
