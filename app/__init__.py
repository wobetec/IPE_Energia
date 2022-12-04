from flask import Flask
from app.sql import SQL
from flask_session import Session
from flask_assets import Environment, Bundle
from app.helpers import filters
from app.var import UPLOAD_FOLDER, GRUPOS_TARIFARIOS


# define app
app = Flask(__name__, instance_relative_config=True)


# configure app usin /instance
app.config.from_pyfile('config.py')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# custom jinja
app.jinja_env.filters["brl"] = filters.brl  # real
app.jinja_env.filters["kwh"] = filters.kwh  # energia
app.jinja_env.filters["kw"] = filters.kw  # energia
app.jinja_env.filters["m2"] = filters.m2  # energia
app.jinja_env.filters["date"] = filters.date  # energia
app.jinja_env.filters["sn"] = filters.sn  # Sim e Não
app.jinja_env.filters["sigla"] = filters.sigla  # Sim e Não

import app.var as var
@app.context_processor
def context_processor():
    return dict(
        ACCESS_LEVEL=var.ACCESS_LEVEL,
        GRUPOS_TARIFARIOS=var.GRUPOS_TARIFARIOS
    )


# set session for app
Session(app)


# set database for the application
db = SQL("sqlite:///database.db")


# set scss
assets = Environment(app)
assets.url = app.static_url_path
sass = Bundle(
    'styles/global.sass', 
    'styles/variables.sass', 
    'styles/components.sass', 
    'styles/pages.sass', 
    filters='sass', output='all.css')
assets.register('sass_all', sass)


# import views
from app import views

# set new erros pages
from app import erros




