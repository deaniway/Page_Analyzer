import psycopg2
from psycopg2.extras import NamedTupleCursor
import datetime


class DbManager:
    def __init__(self, app):
        self.app = app

    @staticmethod
    def execute_in_db(func):
        """Декоратор для выполнения функций соединения с базой данных."""
        def inner(*args, **kwargs):
            with psycopg2.connect(args[0].app.config['DATABASE_URL']) as conn:
                with conn.cursor(cursor_factory=NamedTupleCursor) as cursor:
                    result = func(cursor=cursor, *args, **kwargs)
                    conn.commit()
                    return result
        return inner

    @staticmethod
    def with_commit(func):
        def inner(self, *args, **kwargs):
            try:
                with psycopg2.connect(self.app.config['DATABASE_URL']) as connection:
                    cursor = connection.cursor(cursor_factory=NamedTupleCursor)
                    result = func(self, cursor, *args, **kwargs)
                    connection.commit()
                    return result
            except psycopg2.Error as e:
                print(f'Ошибка при выполнении транзакции: {e}')
                raise e

        return inner

    @with_commit
    def insert_url(self, cursor, url):
        date = datetime.date.today()
        cursor.execute("INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING *", (url, date))
        url_data = cursor.fetchone()
        return url_data

    @with_commit
    def insert_url_check(self, cursor, check):
        date = datetime.date.today()
        cursor.execute("INSERT INTO url_checks (url_id, created_at, status_code, h1, title, description) "
                       "VALUES (%s, %s, %s, %s, %s, %s)",
                       (check['url_id'], date, check['response'], check["h1"], check['title'], check['content']))

    @execute_in_db
    def get_url_from_urls_list(self, url_id, cursor=None):
        cursor.execute("SELECT * FROM urls WHERE id=%s", (url_id,))
        desired_url = cursor.fetchone()
        return desired_url if desired_url else False

    @execute_in_db
    def get_url_from_urls_checks_list(self, url_id, cursor=None):
        cursor.execute("SELECT * FROM url_checks WHERE url_id=%s ORDER BY id DESC", (url_id,))
        result = cursor.fetchall()
        return result

    @execute_in_db
    def get_url_by_name(self, url, cursor=None):
        cursor.execute("SELECT * FROM urls WHERE name=%s", (url,))
        url_id = cursor.fetchone()
        return url_id.id if url_id else None

    @execute_in_db
    def get_urls_list(self, cursor=None):
        query = (
            "SELECT DISTINCT ON (urls.id) urls.id AS id, "
            "url_checks.id AS check_id, "
            "url_checks.status_code AS status_code, "
            "url_checks.created_at AS created_at, "
            "urls.name AS name "
            "FROM urls "
            "LEFT JOIN url_checks ON urls.id = url_checks.url_id "
            "ORDER BY urls.id DESC, check_id DESC"
        )
        cursor.execute(query)
        return cursor.fetchall()
