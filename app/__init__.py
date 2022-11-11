from flask import Flask
from app.sql import SQL
from flask_session import Session
from app.helpers import brl


# define app
app = Flask(__name__, instance_relative_config=True)


# configure app usin /instance
#app.config.from_object('config')
app.config.from_pyfile('config.py')


# custom jinja
app.jinja_env.filters["brl"] = brl  # formater para real


# set session for app
Session(app)


# set database for the application
db = SQL("sqlite:///database.db")


# import views
from app import views
