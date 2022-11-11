from app import app, db
from flask import redirect, render_template, request, session
from app.helpers import apology, login_required


@app.route("/geracao", methods=["GET"])
@app.route("/geracao/list", methods=["GET"])
@login_required
def geracaoList():
    geracoes = db.execute(
        "SELECT geracao.*, geradores.name FROM geracao JOIN geradores ON geradores.id = geracao.gerador_id WHERE geradores.id = ?",
        session["quartel"]["quartel_id"],
    )

    return render_template("geracao/tasks/list.html", geracoes=geracoes)


@app.route("/geracao/add", methods=["GET", "POST"])
@login_required
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
    return render_template("geracao/tasks/add.html", geradores=geradores)


@app.route("/geracao/edit/<int:id>", methods=["GET", "POST"])
@login_required
def geracaoEdit(id=None):
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
            "UPDATE despesas SET gerador_id=?, efetiva=?, reativa=?, consumo=? data_uso WHERE id=?",
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

    return render_template("geracao/tasks/edit.html", geracao=geracao, geradores=geradores)


@app.route("/geracao/delete/<int:id>", methods=["POST"])
@login_required
def delete(id):
    db.execute("DELETE FROM geracao WHERE id=?", id)

    return redirect("/geracao/list")
