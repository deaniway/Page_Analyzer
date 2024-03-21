import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()


def insert_url(url):
    cur.execute("INSERT INTO urls (name) VALUES (%s)", (url,))
    conn.commit()