from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL')


def connect_to_database():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        print("Подключение к базе данных успешно.")
        return conn
    except psycopg2.Error as e:
        print("Ошибка подключения к базе данных:", e)
        return None


def add_url(url):
    conn = connect_to_database()  # Подключение к базе данных
    if conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO urls (name) VALUES (%s)", (url,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Ошибка при добавлении URL в базу данных:", e)
            conn.rollback()
            conn.close()
            return False
    else:
        return False