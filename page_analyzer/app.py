from flask import Flask, render_template, request, redirect, url_for
import os
from page_analyzer.db import insert_url

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html'), 200


@app.post('/urls')
def submit():
    url = request.form['url']
    insert_url(url)
    return redirect(url_for('index'))


@app.route('/urls')
def urls():
    urls = ["https://example.com", "https://example.org"]
    return render_template('urls.html', urls=urls)

