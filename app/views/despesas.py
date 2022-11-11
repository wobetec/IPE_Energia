from app import app, db
from flask import redirect, render_template, request, session
from app.helpers import apology, login_required


@app.route("/despesa", methods=["GET", "POST"])
@app.route("/despesa/add", methods=["GET", "POST"])
@login_required
def despesaAdd():
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
            valor
            or demanda
            or efetiva
            or reativa
            or data_fatura
            or multa
        ):
            return apology("missing")

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

    return render_template("despesa/tasks/add.html")


@app.route("/despesa/edit/<int:id>", methods=["GET", "POST"])
@login_required
def despesaEdit(id=None):
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

    despesa = db.execute("SELECT * FROM despesas WHERE id=?", id)[0]

    return render_template("despesa/tasks/edit.html", despesa=despesa)


@app.route("/despesa/list", methods=["GET"])
@login_required
def despesaList():
    despesas = db.execute(
        "SELECT * FROM despesas WHERE quartel_id=?",
        session["quartel"]["quartel_id"],
    )
    return render_template("despesa/tasks/list.html", despesas=despesas)


@app.route("/despesa/delete", methods=["POST"])
@login_required
def despesaDelete():
    db.execute("DELETE FROM despesas WHERE id=?", id)

    return redirect("/despesa/list")

