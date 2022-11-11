from flask import Flask
from app.sql import SQL
from flask_session import Session
from app.helpers import brl


# define app
app = Flask(__name__)


# configure app
app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"  # Better than cookies


# custom jinja
app.jinja_env.filters["brl"] = brl  # formater para real


# set session for app
Session(app)


# set database for the application
db = SQL("sqlite:///database.db")


# import views
from app import views
