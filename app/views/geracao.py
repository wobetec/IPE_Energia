from app import app, db
from flask import redirect, render_template, request, session
from app.helpers import apology, login_required, access_level_required


@app.route("/geracao", methods=["GET"])
@app.route("/geracao/list", methods=["GET"])
@login_required
@access_level_required(4)
def geracaoList():
    geracoes = db.execute(
        "SELECT geracao.*, geradores.name FROM geracao JOIN geradores ON geradores.id = geracao.gerador_id WHERE geradores.id = ?",
        session["quartel"]["quartel_id"],
    )

    return render_template("pages/geracao.html", geracoes=geracoes, aba="list")


@app.route("/geracao/add", methods=["GET", "POST"])
@login_required
@access_level_required(4)
def geracaoAdd():
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
            return apology("missing")

        db.execute(
            "INSERT INTO geracao (gerador_id, efetiva, reativa, consumo, data_uso) VALUES(?,?,?,?,?)",
            gerador_id,
            efetiva,
            reativa,
            consumo,
            data_uso,
        )

        return redirect("/geracao/list")

    geradores = db.execute("SELECT id, name FROM geradores WHERE quartel_id = ?", session["quartel"]["quartel_id"])
    return render_template("pages/geracao.html", geradores=geradores, aba="add")


@app.route("/geracao/edit/<int:id>", methods=["GET", "POST"])
@login_required
@access_level_required(4)
def geracaoEdit(id=None):
    if request.method == "POST":
        gerador_id = id
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
            return apology("missing")

        db.execute(
            "UPDATE geracao SET gerador_id=?, efetiva=?, reativa=?, consumo=?, data_uso=? WHERE id=?",
            gerador_id,
            efetiva,
            reativa,
            consumo,
            data_uso,
            id
        )

        return redirect("/geracao/list")

    geracao = db.execute("SELECT * FROM geracao WHERE id=?", id)[0]
    geradores = db.execute("SELECT id, name FROM geradores WHERE quartel_id = ?", session["quartel"]["quartel_id"])

    return render_template("pages/geracao.html", geracao=geracao, geradores=geradores, aba="edit")


@app.route("/geracao/delete/<int:id>", methods=["POST"])
@login_required
@access_level_required(4)
def delete(id):
    db.execute("DELETE FROM geracao WHERE id=?", id)

    return redirect("/geracao/list")
