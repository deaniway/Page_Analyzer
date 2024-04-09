from flask import (
    Flask, render_template, request, flash,
    redirect, url_for,
    abort
)
from dotenv import load_dotenv
from page_analyzer.db import DbManager
from page_analyzer.html_parser import HTMLParser
from page_analyzer.utils import normalize_url, validate_url

import os
import requests


load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')

manager = DbManager(app)


@app.errorhandler(404)
def page_not_found(error):
    return render_template('errors/error404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    return render_template('errors/error500.html'), 500


@app.route('/')
def index():
    return render_template('index.html'), 200


@app.post('/urls')
def show_url_page():
    url_check = request.form.get('url')
    normal_url = normalize_url(url_check)

    validation_error = validate_url(normal_url)
    if validation_error:
        flash(validation_error, 'danger')
        return render_template('index.html'), 422

    existed_url = manager.get_url_by_name(normal_url)

    if existed_url:
        flash('Страница уже существует', 'info')
        url_id = existed_url.id
    else:
        url_id = manager.insert_url(normal_url).id
        flash('Страница успешно добавлена', 'success')
    return redirect(url_for('get_url_list', url_id=url_id))


@app.get('/urls')
def get_user():
    all_urls = manager.get_urls_list()
    return render_template('urls.html', urls=all_urls), 200


@app.get('/urls/<int:id>')
def get_url_list(id):

    url = manager.get_url_from_urls_list(id)
    if not url:
        abort(404)
    get_checks_by_url_id = manager.get_url_from_urls_checks_list(id)
    return render_template('list.html',
                           url=url, checks_list=get_checks_by_url_id)


@app.post('/urls/<int:url_id>/check')
def check_url(url_id):
    url_record = manager.get_url_from_urls_list(url_id)
    if not url_record:
        abort(404)

    try:
        response = requests.get(url_record.name)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        flash('Произошла ошибка при проверке', 'danger')
        return redirect(url_for('get_url_list', id=url_id, code=400))

    page_parser = HTMLParser(response.content)
    page_data = page_parser.get_page_data()
    full_check = dict(page_data, url_id=url_id, response=response.status_code)

    manager.insert_url_check(full_check)
    flash('Страница успешно проверена', 'success')
    return redirect(url_for('get_url_list', id=url_id))
