from flask import redirect, render_template, request, session
from functools import wraps
from app.var import DEFAULT_APOLOGY, ALLOWED_EXTENSIONS
import json

def apology(message, code=400):
    """
        Render message as an apology to user.
    """
    def escape(s):
        """
        Escape special characters.
        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s

    if message in DEFAULT_APOLOGY:
        code = DEFAULT_APOLOGY[message]["code"]
        message = DEFAULT_APOLOGY[message]["message"]

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
    
def access_level_required(level):
    """
        Decorator to check access level
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if level != None:
                if session["main"]["access_level"] > level:
                    return apology(f"access level needed {level}")
            return f(*args, **kwargs)
        return decorated_function
    return decorator


class filters():
    def brl(value):
        """Format value as BRL."""
        return f"R${value:,.2f}"

    def kwh(value):
        """Format value as energy in kwh"""
        if value == None:
            return ""
        return f"{value:,.2f}kWh"

    def kw(value):
        """Format value as energy in kwh"""
        if value == None:
            return ""
        return f"{value:,.2f}kW"

    def m2(value):
        """Format value as energy in kwh"""
        return f"{value:,.2f}m\u00b2"

    def sn(value):
        if value:
            return "Sim"
        else:
            return "Não"
    
    def date(value):
        year = value[:4]
        month = value[5:7]
        return f"{month}/{year}"
    
    def sigla(value):
        spaces = value.replace("_", " ")
        #bolinha = spaces.replace("°", "")
        return spaces



def recursive_get_subordinados(db, OM):
    brasao = db.execute("SELECT brasao FROM quarteis WHERE sigla=?", OM)[0]["brasao"]
    lista = {
        "brasao":brasao,
        "subs":{}
    }
    quartel_id = db.execute("SELECT id FROM quarteis WHERE sigla=?", OM)[0]["id"]
    subs = db.execute("SELECT * FROM hierarquia WHERE quartel_id=?", quartel_id)[0]
    subs.pop("id")
    subs.pop("quartel_id")
    for poss_sub in subs:
        if subs[poss_sub] == 1:
            lista["subs"][poss_sub] = recursive_get_subordinados(db, poss_sub)
    return lista


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


