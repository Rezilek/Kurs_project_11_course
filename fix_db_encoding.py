import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def fix_database_encoding():
    print('справление настроек базы данных...')
    
    with connection.cursor() as cursor:
        # 1. роверка текущих настроек
        print('\n1. Текущие настройки:')
        cursor.execute('''
            SELECT 
                datname,
                pg_encoding_to_char(encoding) as encoding,
                datcollate,
                datctype
            FROM pg_database 
            WHERE datname = current_database()
        ''')
        
        db_info = cursor.fetchone()
        print(f'аза: {db_info[0]}')
        print(f'одировка: {db_info[1]}')
        print(f'Collate: {db_info[2]}')
        print(f'Ctype: {db_info[3]}')
        
        # 2. роверка подключения клиента
        print('\n2. астройки клиента:')
        cursor.execute('SHOW client_encoding')
        print(f'client_encoding: {cursor.fetchone()[0]}')
        
        cursor.execute('SHOW lc_messages')
        print(f'lc_messages: {cursor.fetchone()[0]}')
        
        # 3. опробуем установить кодировку клиента
        print('\n3. становка кодировки клиента...')
        try:
            cursor.execute('SET client_encoding TO \'UTF8\'')
            print('✓ client_encoding установлен в UTF8')
        except:
            print('✗ е удалось установить client_encoding')
        
        # 4. Тест записи
        print('\n4. Тест записи русских символов...')
        try:
            # Создаем временную таблицу для теста
            cursor.execute('''
                CREATE TEMP TABLE test_encoding (
                    id SERIAL PRIMARY KEY,
                    russian_text TEXT,
                    latin_text TEXT
                )
            ''')
            
            # ставляем тестовые данные
            test_data = [
                ('ривет мир', 'Hello world'),
                ('Тест кодировки', 'Encoding test'),
                ('усский текст', 'Russian text')
            ]
            
            for rus, lat in test_data:
                cursor.execute(
                    'INSERT INTO test_encoding (russian_text, latin_text) VALUES (%s, %s)',
                    [rus, lat]
                )
            
            # итаем обратно
            cursor.execute('SELECT russian_text, latin_text FROM test_encoding')
            rows = cursor.fetchall()
            
            print('рочитанные данные:')
            for rus, lat in rows:
                print(f'  усский: {repr(rus)}, атинский: {repr(lat)}')
            
            # даляем временную таблицу
            cursor.execute('DROP TABLE test_encoding')
            print('✓ Тест пройден успешно')
            
        except Exception as e:
            print(f'✗ шибка теста: {e}')
        
        # 5. екомендации
        print('\n5. екомендации:')
        if db_info[1] != 'UTF8':
            print('⚠️  аза данных не в UTF8. ужно создать новую :')
            print('CREATE DATABASE new_db ENCODING \'UTF8\' LC_COLLATE \'Russian_Russia.1251\' LC_CTYPE \'Russian_Russia.1251\' TEMPLATE template0;')
        else:
            print('✓ аза в UTF8')
        
        if 'C' in db_info[2] or 'POSIX' in db_info[2]:
            print('⚠️  Collate C/POSIX. огут быть проблемы с сортировкой русских символов')

if __name__ == '__main__':
    fix_database_encoding()
