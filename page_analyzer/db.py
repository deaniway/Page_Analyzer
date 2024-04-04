import psycopg2
from psycopg2.extras import NamedTupleCursor
import datetime
from dotenv import load_dotenv

load_dotenv()


def init_connection(app):
    """Инициализирует соединение с базой данных, используя конфигурацию Flask."""
    try:
        connection = psycopg2.connect(app.config['DATABASE_URL'])
        return connection
    except Exception as e:
        print('Произошла ошибка при инициализации соединения:', e)


def get_cursor(connection):
    """Получает курсор для выполнения запросов."""
    return connection.cursor(cursor_factory=NamedTupleCursor)


def execute_in_db(func):
    """Декоратор для выполнения функций соединения с базой данных."""
    def inner(*args, **kwargs):
        with init_connection(*args, **kwargs) as conn:
            with get_cursor(conn) as cursor:
                result = func(cursor=cursor, *args, **kwargs)
                return result
    return inner


class DbManager:
    def __init__(self, app):
        self.app = app

    @staticmethod
    def with_commit(func):
        def inner(self, *args, **kwargs):
            try:
                with init_connection(self.app) as connection:
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

    @with_commit
    def get_url_from_urls_list(self, cursor, url_id):
        cursor.execute("SELECT * FROM urls WHERE id=%s", (url_id,))
        desired_url = cursor.fetchone()
        return desired_url if desired_url else False

    @with_commit
    def get_url_from_urls_checks_list(self, cursor, url_id):
        cursor.execute("SELECT * FROM url_checks WHERE url_id=%s ORDER BY id DESC", (url_id,))
        result = cursor.fetchall()
        return result

    @with_commit
    def get_url_by_name(self, cursor, url):
        cursor.execute("SELECT * FROM urls WHERE name=%s", (url,))
        url_id = cursor.fetchone()
        return url_id.id if url_id else None

    @with_commit
    def get_urls_list(self, cursor):
        cursor.execute("SELECT DISTINCT ON (urls.id) urls.id AS id, url_checks.id AS check_id, "
                       "url_checks.status_code AS status_code, url_checks.created_at AS created_at, "
                       "urls.name AS name FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id "
                       "ORDER BY urls.id DESC, check_id DESC")
        result = cursor.fetchall()
        return result


'''
Из ревью:

Функция init_connection теперь принимает аргумент app для получения конфигурации Flask
Это позволяет использовать конфигурацию Flask для инициализации соединения с базой данны

Метод __init__  принимает аргумент app и сохраняет его

В методах init_connection изменен на init_connection(self.app),
чтобы передать  Flask для получения конфигурации

Добавлен NamedTupleCursor для получения курсора с именованными кортежами

Исправлен вызов функции init_connection в декораторе execute_in_db, чтобы передать аргументы правильно.
'''
