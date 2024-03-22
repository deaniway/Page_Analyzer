from flask import Flask, render_template, request, flash, redirect, url_for
from page_analyzer.tools_url import validate_url, normalize_url
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.route('/')
def index():
    return render_template('index.html'), 200

@app.post('/url')
def add_url():
    url = request.form.get('url')
    errors = validate_url(url)
    if errors:
        for i in errors:
            flash(*i)
        return redirect('index.html'), 422

