from app import app, db
from flask import redirect, render_template, request, session
from app.helpers import apology, login_required, recursive_get_subordinados, access_level_required


@app.route("/quartel/list", methods=["GET"])
@login_required
@access_level_required(2)
def quartelList():
    subordinados = {
        session["quartel"]["sigla"]: recursive_get_subordinados(
            db, session["quartel"]["sigla"]
        )
    }

    return render_template("quartel/tasks/list.html", subordinados=subordinados)


@app.route("/quartel/add", methods=["GET", "POST"])
@login_required
@access_level_required(2)
def quartelAdd():
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

    return render_template("quartel/tasks/add.html")


@app.route("/quartel", methods=["GET"])
@app.route("/quartel/edit", methods=["GET", "POST"])
@login_required
@access_level_required(3)
def quartelEdit():
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

        return redirect("/quartel/list")

    quartel = db.execute(
        "SELECT * FROM quarteis WHERE id=?", session["quartel"]["quartel_id"]
    )[0]

    return render_template("quartel/tasks/edit.html", quartel=quartel)


@app.route("/quartel/select/<string:sigla>", methods=["GET"])
@access_level_required(2)
@login_required
def quartelSelect(sigla):
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

