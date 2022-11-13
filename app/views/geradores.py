from app import app, db
from flask import redirect, render_template, request, session
from app.helpers import apology, login_required, access_level_required


@app.route("/gerador", methods=["GET"])
@app.route("/gerador/list", methods=["GET"])
@login_required
@access_level_required(4)
def geradorList():
    geradores = db.execute(
        "SELECT * FROM geradores WHERE quartel_id=?",
        session["quartel"]["quartel_id"],
    )
    return render_template("gerador/tasks/list.html", geradores=geradores)


@app.route("/gerador/add", methods=["GET", "POST"])
@login_required
@access_level_required(3)
def geradorAdd():
    if request.method == "POST":
        quartel_id = session["quartel"]["quartel_id"]

        name = request.form.get("name")
        tipo = request.form.get("tipo")

        if not (
            name
            or tipo
        ):
            return apology("missing")

        db.execute(
            "INSERT INTO geradores (quartel_id, name, tipo) VALUES(?,?,?)",
            quartel_id,
            name,
            tipo,
        )

        return redirect("/gerador/list")

    return render_template("gerador/tasks/add.html")


@app.route("/gerador/edit/<int:id>", methods=["GET", "POST"])
@login_required
@access_level_required(3)
def geradorEdit(id=None):
    if request.method == "POST":
        quartel_id = session["quartel"]["quartel_id"]

        name = request.form.get("name")
        tipo = request.form.get("tipo")

        if not (
            name
            or tipo
        ):
            return apology("missing")

        db.execute(
            "UPDATE geradores SET name=?, tipo=? WHERE quartel_id=?",
            name,
            tipo,
            quartel_id,
        )

        return redirect("/gerador/list")


    gerador = db.execute("SELECT * FROM geradores WHERE id=?", id)[0]

    return render_template("gerador/tasks/edit.html", gerador=gerador)


@app.route("/gerador/delete/<int:id>", methods=["POST"])
@login_required
@access_level_required(3)
def geradorDelete(id = None):
    ids = [i["id"] for i in db.execute("SELECT id FROM geradores WHERE quartel_id = ?", session["quartel"]["quartel_id"])]
    totals = [i["id"] for i in db.execute("SELECT id FROM geradores")]

    if id in totals and id not in ids:
        apology("forbiden")
    elif id not in totals:
        apology("notFound")

    db.execute("DELETE FROM geradores WHERE id=?", id)

    return redirect("/despesa/list")

