from app import app
from app.dashboard_frontend import appdash
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home')


@app.route('/info')
def info():
    return render_template('info.html', title='Info')


@app.route('/updates')
def updates():
    return render_template('updates.html', title='Updates')


# @app.route('/dashboard')
# def dashboard():
#     return appdash.index()
