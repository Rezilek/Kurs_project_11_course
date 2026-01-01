# scripts/check_db_encoding.py
import psycopg2
from decouple import config


def check_db_encoding():
    conn = psycopg2.connect(
        dbname=config('DB_NAME'),
        user=config('DB_USER'),
        password=config('DB_PASSWORD'),
        host=config('DB_HOST', default='localhost'),
        port=config('DB_PORT', default='5432')
    )
    cur = conn.cursor()
    cur.execute("SELECT datname, encoding FROM pg_database WHERE datname = %s", (config('DB_NAME'),))
    result = cur.fetchone()
    cur.close()
    conn.close()

    if result:
        db_name, encoding = result
        encoding_map = {
            0: 'SQL_ASCII',
            6: 'UTF8',
            8: 'LATIN1',
            # Добавьте другие кодировки по необходимости
        }
        print(f"База данных: {db_name}")
        print(f"Кодировка: {encoding} ({encoding_map.get(encoding, 'Неизвестно')})")

        if encoding != 6:  # UTF8
            print("ВНИМАНИЕ: База данных не использует UTF-8 кодировку!")
            print("Создайте новую БД с командой:")
            print(f"createdb -E UTF8 {db_name}")
    else:
        print("База данных не найдена!")


if __name__ == "__main__":
    check_db_encoding()