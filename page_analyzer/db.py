import psycopg2
from psycopg2.extras import NamedTupleCursor
import os
from dotenv import load_dotenv
import datetime

load_dotenv()


def init_connection():
    """Инициализирует соединение с базой данных."""
    try:
        connection = psycopg2.connect(os.getenv('DATABASE_URL'))
        return connection
    except Exception:
        print('Тапок заминирован, доставай дебагер')


def get_cursor(connection):
    """Получает курсор для выполнения запросов."""
    return connection.cursor(cursor_factory=NamedTupleCursor)


def execute_in_db(func):
    """Декоратор для выполнения функций соединения с базой данных."""
    def inner(*args, **kwargs):
        with init_connection() as conn:
            with get_cursor(conn) as cursor:
                result = func(cursor=cursor, *args, **kwargs)
                return result
    return inner


class DbManager:
    @execute_in_db
    def insert_url(self, url, cursor=None):
        """Вставляет URL в базу данных и возвращает его."""
        date = datetime.date.today()
        cursor.execute("INSERT INTO urls (name, created_at)"
                       " VALUES (%s, %s) RETURNING *",
                       (url, date))
        return cursor.fetchone()

    @execute_in_db
    def insert_url_check(self, check, cursor=None):
        """Вставляет результат проверки URL в базу данных."""
        date = datetime.date.today()
        cursor.execute("INSERT INTO url_checks (url_id, created_at, "
                       "status_code, h1, title, description) "
                       "VALUES (%s, %s, %s, %s, %s, %s)",
                       (check['url_id'], date, check['response'],
                        check["h1"], check['title'], check['content']))

    @execute_in_db
    def get_url_from_urls_list(self, url_id, cursor=None):
        """Получает URL из базы данных по его ID."""
        cursor.execute("SELECT * FROM urls WHERE id=%s", (url_id,))
        desired_url = cursor.fetchone()
        return desired_url if desired_url else False

    @execute_in_db
    def get_url_from_urls_checks_list(self, url_id, cursor=None):
        """Получает результаты проверки URL из базы данных по ID URL."""
        cursor.execute("SELECT * FROM url_checks "
                       "WHERE url_id=%s ORDER BY id DESC", (url_id,))
        return cursor.fetchall()

    @execute_in_db
    def get_id_from_url(self, url, cursor=None):
        """Получает ID URL из базы данных по его имени."""
        cursor.execute("SELECT * FROM urls WHERE name=%s", (url,))
        url_id = cursor.fetchone()
        return url_id.id if url_id else None

    @execute_in_db
    def get_urls_list(self, cursor=None):
        """Получает список URL из базы данных."""
        cursor.execute("SELECT DISTINCT ON (urls.id) urls.id "
                       "AS id, url_checks.id "
                       "AS check_id, url_checks.status_code "
                       "AS status_code, url_checks.created_at "
                       "AS created_at, urls.name "
                       "AS name FROM urls "
                       "LEFT JOIN url_checks "
                       "ON urls.id = url_checks.url_id "
                       "ORDER BY urls.id DESC, "
                       "check_id DESC")

        return cursor.fetchall()
