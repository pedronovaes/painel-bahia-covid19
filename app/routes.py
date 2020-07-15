from app import app
from app.dashboard_frontend import appdash
from flask import render_template


# @app.route('/')
# @app.route('/index')
# def index():
#     return render_template('index.html', title='Home')


@app.route('/about')
def info():
    return render_template('about.html', title='Sobre')
