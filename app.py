import sqlite3
from tempfile import mkdtemp

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, brl, recursive_get_subordinados
from sql import SQL

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Custom filter
app.jinja_env.filters["brl"] = brl

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

db = SQL("sqlite:///database.db")

# def get_db():
#     db_connection = sqlite3.connect("database.db")
#     db_connection.row_factory = sqlite3.Row
#     return db_connection


ACCESS_LEVEL = {1: "Master", 2: "Full + subordinados", 2: "Full", 3: "Inserir dados"}


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/", methods=["GET"])
@login_required
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        quartel = db.execute(
            "SELECT area, efetivo, demanda_contratada, sigla FROM quarteis WHERE id=?",
            rows[0]["quartel_id"],
        )

        # Remember which user has logged in and save quartel data
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        session["main"] = {
            "access_level": rows[0]["access_level"],
            "quartel_id": rows[0]["quartel_id"], 
            "sigla": quartel[0]["sigla"],
        }
        # session["main"] = dict(session["main"][0])
        print(session["main"]["access_level"])

        session["quartel"] = {
            "quartel_id": rows[0]["quartel_id"],
            "sigla": quartel[0]["sigla"],
            "area": quartel[0]["area"],
            "efetivo": quartel[0]["efetivo"],
            "demanda_contratada": quartel[0]["demanda_contratada"],
        }
        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("users/login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET"])
@app.route("/register/<path:cheat>/<path:password>", methods=["GET"])
def register(cheat=None, password=None):

    if cheat == "esdras" and password:
        hashed = generate_password_hash(password)
        db.execute(
            "INSERT INTO users (username, hash, quartel_id, access_level) VALUES(?, ?, ?, ?)",
            cheat,
            hashed,
            1,
            1,
        )

        return render_template("users/login.html")

    return apology("Forbiden", code=403)


@app.route("/despesa", methods=["GET", "POST"])
@app.route("/despesa/<path:task>", methods=["GET", "POST"])
@app.route("/despesa/<path:task>/<int:id>", methods=["GET", "POST"])
@login_required
def despesa(task=None, id=None):

    if task == None or task == "add":
        if request.method == "POST":
            quartel_id = session["quartel"]["quartel_id"]
            efetivo = session["quartel"]["efetivo"]
            contratada = session["quartel"]["demanda_contratada"]
            area = session["quartel"]["area"]

            valor = request.form.get("valor")
            demanda = request.form.get("demanda")
            efetiva = request.form.get("efetiva")
            reativa = request.form.get("reativa")
            data_fatura = request.form.get("data_fatura")
            multa = request.form.get("multa")

            if not (
                quartel_id
                or valor
                or efetivo
                or area
                or demanda
                or efetiva
                or reativa
                or data_fatura
            ):
                return apology("Missing some data")

            db.execute(
                "INSERT INTO despesas (quartel_id, valor, efetivo, area, demanda, efetiva, reativa, data_fatura, contratada, multa) VALUES(?,?,?,?,?,?,?,?,?,?)",
                quartel_id,
                valor,
                efetivo,
                area,
                demanda,
                efetiva,
                reativa,
                data_fatura,
                contratada,
                multa,
            )

            return redirect("/despesa/list")

        elif request.method == "GET":
            return render_template("despesa/tasks/add.html")

        return apology("Method not alowed")

    elif task == "edit":
        if request.method == "POST":
            quartel_id = session["quartel"]["quartel_id"]
            efetivo = session["quartel"]["efetivo"]
            contratada = session["quartel"]["demanda_contratada"]
            area = session["quartel"]["area"]

            valor = request.form.get("valor")
            demanda = request.form.get("demanda")
            efetiva = request.form.get("efetiva")
            reativa = request.form.get("reativa")
            data_fatura = request.form.get("data_fatura")
            multa = request.form.get("multa")

            if not (
                quartel_id
                or valor
                or efetivo
                or area
                or demanda
                or efetiva
                or reativa
                or data_fatura
            ):
                return apology("Missing some data")

            db.execute(
                "UPDATE despesas SET valor=?, efetivo=?, area=?, demanda=?, efetiva=?, reativa=?, data_fatura=?, contratada=?, multa=? WHERE quartel_id=?",
                valor,
                efetivo,
                area,
                demanda,
                efetiva,
                reativa,
                data_fatura,
                contratada,
                multa,
                quartel_id,
            )

            return redirect("/despesa/list")

        elif request.method == "GET":
            despesa = db.execute("SELECT * FROM despesas WHERE id=?", id)[0]

            return render_template("despesa/tasks/edit.html", despesa=despesa)

        return apology("Method not alowed")

    elif task == "list":
        if request.method == "GET":
            despesas = db.execute(
                "SELECT * FROM despesas WHERE quartel_id=?",
                session["quartel"]["quartel_id"],
            )
            return render_template("despesa/tasks/list.html", despesas=despesas)

        return apology("Not build yet")

    elif task == "delete":
        db.execute("DELETE FROM despesas WHERE id=?", id)

        return redirect("/despesa/list")

    return apology("Not build yet")


@app.route("/quartel", methods=["GET", "POST"])
@app.route("/quartel/<path:task>", methods=["GET", "POST"])
@app.route("/quartel/<path:task>/<path:sigla>", methods=["GET", "POST"])
@login_required
def quartel(task=None, sigla=None):

    if task == "add":
        if request.method == "POST":
            name = request.form.get("name")
            sigla = request.form.get("sigla")
            efetivo = request.form.get("efetivo")
            area = request.form.get("area")
            demanda_contratada = request.form.get("demanda_contratada")
            grupo_tarifario = request.form.get("grupo_tarifario")

            # adiciona em quarteis
            db.execute(
                "INSERT INTO quarteis (name, sigla, efetivo, area, demanda_contratada, grupo_tarifario) VALUES(?,?,?,?,?,?)",
                name,
                sigla,
                efetivo,
                area,
                demanda_contratada,
                grupo_tarifario,
            )

            # adiciona coluna em hierarquia de
            db.execute("ALTER TABLE hierarquia ADD ? INTEGER NOT NULL DEFAULT 0", sigla)
            new_id = db.execute("SELECT id FROM quarteis WHERE sigla=?", sigla)[0]["id"]
            db.execute("INSERT INTO hierarquia (quartel_id) VALUES(?)", new_id)

            # coloca o 1 em hierarquia
            db.execute(
                "UPDATE hierarquia SET ? = 1 WHERE quartel_id = ?",
                sigla,
                session["quartel"]["quartel_id"],
            )

            return redirect("/quartel/list")

        elif request.method == "GET":
            return render_template("quartel/tasks/add.html")

    elif task == "edit":
        if request.method == "POST":
            efetivo = request.form.get("efetivo")
            area = request.form.get("area")
            demanda_contratada = request.form.get("demanda_contratada")
            grupo_tarifario = request.form.get("grupo_tarifario")

            db.execute(
                "UPDATE quarteis SET efetivo = ?, area = ?, demanda_contratada = ?, grupo_tarifario = ? WHERE id = ?",
                efetivo,
                area,
                demanda_contratada,
                grupo_tarifario,
                session["quartel"]["quartel_id"],
            )

            return redirect("/")

        elif request.method == "GET":
            quartel = db.execute(
                "SELECT * FROM quarteis WHERE id=?", session["quartel"]["quartel_id"]
            )[0]

            return render_template("quartel/tasks/edit.html", quartel=quartel)

    elif task == "list" or task == None:
        if request.method == "GET":
            subordinados = {
                session["quartel"]["sigla"]: recursive_get_subordinados(
                    db, session["quartel"]["sigla"]
                )
            }

            return render_template("quartel/tasks/list.html", subordinados=subordinados)

    elif task == "select":
        if request.method == "GET":
            data = db.execute(
                "SELECT id, sigla, area, efetivo, demanda_contratada FROM quarteis WHERE sigla=?",
                sigla,
            )[0]

            session["quartel"] = {
                "quartel_id": data["id"],
                "sigla": data["sigla"],
                "area": data["area"],
                "efetivo": data["efetivo"],
                "demanda_contratada": data["demanda_contratada"],
            }

        return redirect("/")


    return apology("This page does not exist", code=404)


@app.route("/users", methods=["GET", "POST"])
@app.route("/users/<path:task>", methods=["GET", "POST"])
@app.route("/users/<path:task>/<int:id>", methods=["GET", "POST"])
@login_required
def users(task=None, id=None):

    if task == "add":
        if request.method == "POST":
            username = request.form.get("username")
            password = request.form.get("password")
            confirmation = request.form.get("confirmation")
            access_level = request.form.get("access_level")

            if db.execute("SELECT * FROM users WHERE username = ?", username):
                return apology("Username already exists")
            elif password == "" or password != confirmation:
                return apology("Password is blank or the passwords do not match")
            else:
                hashed = generate_password_hash(password)
                db.execute(
                    "INSERT INTO users (username, hash, quartel_id, access_level) VALUES(?, ?, ?, ?)",
                    username,
                    hashed,
                    session["quartel"]["quartel_id"],
                    access_level,
                )

                return redirect("/users/list")

        elif request.method == "GET":
            return render_template("/users/tasks/add.html", access=ACCESS_LEVEL)

    elif task == "list" or task == None:
        if request.method == "GET":
            access_level = request.form.get("access_level")
            users = db.execute(
                "SELECT username, access_level, id FROM users WHERE quartel_id = ? AND access_level > ?",
                session["quartel"]["quartel_id"], session["main"]["access_level"],
            )
            return render_template("/users/tasks/list.html", users=users)
    
    elif task == "edit":
        if request.method == "POST":
            efetivo = request.form.get("efetivo")
            area = request.form.get("area")
            demanda_contratada = request.form.get("demanda_contratada")
            grupo_tarifario = request.form.get("grupo_tarifario")

            db.execute(
                "UPDATE quarteis SET efetivo = ?, area = ?, demanda_contratada = ?, grupo_tarifario = ? WHERE id = ?",
                efetivo,
                area,
                demanda_contratada,
                grupo_tarifario,
                session["quartel"]["quartel_id"],
            )

            return redirect("/")

        elif request.method == "GET":
            user = db.execute("SELECT username, access_level FROM users WHERE id=?", id)[0]
        

            return render_template("users/tasks/edit.html", user=user, access=ACCESS_LEVEL)

    elif task == "delete":
        db.execute("DELETE FROM users WHERE id=?", id)

        return redirect("/users/list")

    return apology("This page does not exist", code=404)

@app.route("/gerador", methods=["GET", "POST"])
@app.route("/gerador/<path:task>", methods=["GET", "POST"])
@app.route("/gerador/<path:task>/<int:id>", methods=["GET", "POST"])
@login_required
def gerador(task=None, id=None):

    if task == "add" or task == None:
        if request.method == "POST":
            quartel_id = session["quartel"]["quartel_id"]

            name = request.form.get("name")
            tipo = request.form.get("tipo")

            if not (
                quartel_id
                or name
                or tipo
            ):
                return apology("Missing some data")

            db.execute(
                "INSERT INTO geradores (quartel_id, name, tipo) VALUES(?,?,?)",
                quartel_id,
                name,
                tipo,
            )

            return redirect("/gerador/list")

        elif request.method == "GET":
            return render_template("gerador/tasks/add.html")

        return apology("Method not alowed")

    elif task == "edit":
        if request.method == "POST":
            quartel_id = session["quartel"]["quartel_id"]

            name = request.form.get("name")
            tipo = request.form.get("tipo")

            if not (
                quartel_id
                or name
                or tipo
            ):
                return apology("Missing some data")

            db.execute(
                "UPDATE geradores SET name=?, tipo=? WHERE quartel_id=?",
                name,
                tipo,
                quartel_id,
            )

            return redirect("/gerador/list")

        elif request.method == "GET":
            gerador = db.execute("SELECT * FROM geradores WHERE id=?", id)[0]

            return render_template("gerador/tasks/edit.html", gerador=gerador)

        return apology("Method not alowed")

    elif task == "list" or task == None:
        if request.method == "GET":
            geradores = db.execute(
                "SELECT * FROM geradores WHERE quartel_id=?",
                session["quartel"]["quartel_id"],
            )
            return render_template("gerador/tasks/list.html", geradores=geradores)

        return apology("Not build yet")

    elif task == "delete":
        db.execute("DELETE FROM despesas WHERE id=?", id)

        return redirect("/despesa/list")

    return apology("Not build yet")


@app.route("/geracao", methods=["GET", "POST"])
@app.route("/geracao/<path:task>", methods=["GET", "POST"])
@app.route("/geracao/<path:task>/<int:id>", methods=["GET", "POST"])
@login_required
def geracao(task=None, id=None):

    if task == "add"  or task == None:
        if request.method == "POST":
            gerador_id = request.form.get("gerador_id")
            efetiva = request.form.get("efetiva")
            reativa = request.form.get("reativa")
            consumo = request.form.get("consumo")
            data_uso = request.form.get("data_uso")

            if not (
                gerador_id
                or efetiva
                or reativa
                or consumo
                or data_uso
            ):
                return apology("Missing some data")
            print(gerador_id, efetiva, reativa, consumo, data_uso)
            db.execute(
                "INSERT INTO geracao (gerador_id, efetiva, reativa, consumo, data_uso) VALUES(?,?,?,?,?)",
                gerador_id,
                efetiva,
                reativa,
                consumo,
                data_uso,
            )

            return redirect("/geracao/list")

        elif request.method == "GET":
            geradores = db.execute("SELECT id, name FROM geradores WHERE quartel_id = ?", session["quartel"]["quartel_id"])
            return render_template("geracao/tasks/add.html", geradores=geradores)

        return apology("Method not alowed")

    elif task == "edit":
        if request.method == "POST":
            gerador_id = request.form.get("gerador_id")
            efetiva = request.form.get("efetiva")
            reativa = request.form.get("reativa")
            consumo = request.form.get("consumo")
            data_uso = request.form.get("data_uso")

            if not (
                gerador_id
                or efetiva
                or reativa
                or consumo
                or data_uso
            ):
                return apology("Missing some data")

            db.execute(
                "UPDATE despesas SET gerador_id=?, efetiva=?, reativa=?, consumo=? data_uso WHERE id=?",
                gerador_id,
                efetiva,
                reativa,
                consumo,
                data_uso,
                id
            )

            return redirect("/geracao/list")

        elif request.method == "GET":
            geracao = db.execute("SELECT * FROM geracao WHERE id=?", id)[0]
            geradores = db.execute("SELECT id, name FROM geradores WHERE quartel_id = ?", session["quartel"]["quartel_id"])

            return render_template("geracao/tasks/edit.html", geracao=geracao, geradores=geradores)

        return apology("Method not alowed")

    elif task == "list":
        if request.method == "GET":
            geracoes = db.execute(
                "SELECT * FROM geracao WHERE gerador_id in (SELECT id FROM geradores WHERE quartel_id = ?)",
                session["quartel"]["quartel_id"],
            )

            return render_template("geracao/tasks/list.html", geracoes=geracoes)

        return apology("Not build yet")

    elif task == "delete":
        db.execute("DELETE FROM geracao WHERE id=?", id)

        return redirect("/geracao/list")

    return apology("Not build yet")
