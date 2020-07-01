from app import app
from app.dashboard import appdash
from flask import render_template


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


# @app.route('/dashboard')
# def dashboard():
#     return appdash.index()
