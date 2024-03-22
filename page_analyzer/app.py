from flask import Flask, render_template, request, flash, redirect, url_for
from page_analyzer.tools_url import validate_url, normalize_url
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DEBUG_SWITCH = os.getenv("DEBUG_SWITCH")


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

