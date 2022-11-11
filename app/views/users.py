from app import app, db
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from app.helpers import apology, login_required


@app.route("/login", methods=["GET", "POST"])
def login():
    """
        Log user in
    """
    session.clear()


    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Ensure that all needed data is passed
        if not (
            username
            or password
        ):
            return apology("missing")

        # Get user in database
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            username
        )

        # Ensure that username and password is correct
        if (
            len(rows) != 1 
            or not check_password_hash(rows[0]["hash"], password)
        ):
            return apology("invalid username and/or password", 403)

        # set user in session
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]

        # get main OM infos
        quartel = db.execute(
            "SELECT area, efetivo, demanda_contratada, sigla FROM quarteis WHERE id=?",
            rows[0]["quartel_id"],
        )
        session["main"] = {
            "access_level": rows[0]["access_level"],
            "quartel_id": rows[0]["quartel_id"], 
            "sigla": quartel[0]["sigla"],
        }
        session["quartel"] = {
            "quartel_id": rows[0]["quartel_id"],
            "sigla": quartel[0]["sigla"],
            "area": quartel[0]["area"],
            "efetivo": quartel[0]["efetivo"],
            "demanda_contratada": quartel[0]["demanda_contratada"],
        }

        return redirect("/")

    return render_template("users/login.html")


@app.route("/logout")
def logout():
    """
        Log user out
    """

    session.clear()

    return redirect("/")


@app.route("/register", methods=["GET"])
@app.route("/register/<path:cheat>/<path:password>", methods=["GET"])
def register(cheat=None, password=None):
    """
        Development tool to help in rebuild entire database
    """

    if cheat == "esdras" and password:

        rows = db.execute(
            "SELECT * FROM users WHERE username = ?",
            "esdras"
        )

        # check if there is no user "esdras"
        if len(rows) == 0:
            hashed = generate_password_hash(password)
            db.execute(
                "INSERT INTO users (username, hash, quartel_id, access_level) VALUES(?, ?, ?, ?)",
                cheat,
                hashed,
                1,
                1,
            )

            return redirect("/")

    return apology("unauthorized")


@app.route("/users", methods=["GET"])
@app.route("/users/list", methods=["GET"])
@login_required
def usersList():
    """
        List all users under the access_level of user
    """

    users = db.execute(
        "SELECT username, access_level, id FROM users WHERE quartel_id = ? AND access_level > ?",
        session["quartel"]["quartel_id"], 
        session["main"]["access_level"],
    )

    return render_template("/users/tasks/list.html", users=users)


@app.route("/users/add", methods=["GET", "POST"])
@login_required
def userAdd():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        access_level = request.form.get("access_level")

        if db.execute(
            "SELECT * FROM users WHERE username = ?",
            username
        ):
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

    return render_template("/users/tasks/add.html")  


@app.route("/users/edit/<int:id>", methods=["GET", "POST"])
@login_required
def userEdit(id=None):
    if request.method == "POST":
        access_level = request.form.get("access_level")

        db.execute(
            "UPDATE users SET access_level = ? WHERE id = ?",
            access_level,
            id,
        )

        return redirect("/users/list")

    user = db.execute("SELECT username, access_level, id FROM users WHERE id=?", id)[0]

    return render_template("users/tasks/edit.html", user=user)


@app.route("/users/edit/<int:id>", methods=["POST"])
@login_required
def userDelete(id=None):
    db.execute("DELETE FROM users WHERE id=?", id)

    return redirect("/users/list")

