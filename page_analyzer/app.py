from flask import (
    Flask, render_template, request, flash,
    get_flashed_messages, redirect, url_for
)
from dotenv import load_dotenv
from validators import url as validate
from page_analyzer.db import DbManager
from page_analyzer.html_parser import HTMLParser
from urllib.parse import urlparse
import os
import requests

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

manager = DbManager()


@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    return render_template('index.html', messages=messages), 200


@app.post('/urls')
def urls():
    url_chek = request.form.get('url')
    parse_url = urlparse(url_chek)
    normal_url = f'{parse_url.scheme}://{parse_url.netloc}'
    if not validate(normal_url):
        flash('Некорректный URL', 'danger')
        messages = get_flashed_messages(with_categories=True)
        return render_template('index.html', messages=messages), 422
    url_id = manager.get_id_from_url(normal_url)
    if url_id:
        flash('Страница уже существует', 'warning')
        return redirect(url_for('get_url_list', id=url_id))
    url = manager.insert_url(normal_url)
    flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url_list', id=url.id))


@app.get('/urls')
def get_user():
    messages = get_flashed_messages(with_categories=True)
    all_urls = manager.get_urls_list()
    return render_template('urls.html', messages=messages, urls=all_urls), 200


@app.get('/urls/<int:id>')
def get_url_list(id):
    messages = get_flashed_messages(with_categories=True)
    url = manager.get_url_from_urls_list(id)
    if not url:
        flash('Запрашиваемая страница не найдена', 'warning')
        return redirect(url_for('index'), 404)
    checks_list = manager.get_url_from_urls_checks_list(id)
    return render_template('list.html', messages=messages,
                           url=url, checks_list=checks_list)


@app.post('/urls/<int:id>/check')
def check_url(id):
    url = manager.get_url_from_urls_list(id).name
    if not url:
        flash('Запрашиваемая страница не найдена', 'warning')
        return redirect(url_for('index'), 404)
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url_list', id=id, code=400))

    responses_html = response.content
    soup = HTMLParser(responses_html)
    check = soup.chek()
    full_check = dict(check, url_id=id, response=response.status_code)

    manager.insert_url_check(full_check)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url_list', id=id))
