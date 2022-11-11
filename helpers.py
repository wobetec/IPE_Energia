import os
import requests
import urllib.parse

from flask import redirect, render_template, request, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.
    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def brl(value):
    """Format value as BRL."""
    return f"R${value:,.2f}"


def recursive_get_subordinados(db, OM):
    lista = {}
    quartel_id = db.execute("SELECT id FROM quarteis WHERE sigla=?", OM)[0]["id"]
    subs = db.execute("SELECT * FROM hierarquia WHERE quartel_id=?", quartel_id)[0]
    subs.pop("id")
    subs.pop("quartel_id")
    for poss_sub in subs:
        if subs[poss_sub] == 1:
            lista[poss_sub] = recursive_get_subordinados(db, poss_sub)
    return lista