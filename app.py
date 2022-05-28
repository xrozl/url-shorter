import sqlite3
from flask import Flask, render_template, request, g

app = Flask(__name__)

@app.route('/')
def index():
    if 'db' not in g:
        g.db = sqlite3.connect('data.db')
    
    database = g.db
    cursor = database.execute("select count(*) from master where TYPE='table' AND name='urls'")

    for r in cursor:
        if r[0] == 0:
            database.execute("create table urls (url string, short string)")
            database.commit()
    
    cursor = database.execute("select * from urls")
    urls = [dict(url=row[0], short=row[1]) for row in cursor.fetchall()]
    return render_template('index.html', urls=urls)
