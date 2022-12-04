from app import app, db
from flask import redirect, render_template, request, session
from app.helpers import apology, login_required, access_level_required


@app.route("/concessionarias", methods=["GET"])
@app.route("/concessionarias/list", methods=["GET"])
@login_required
@access_level_required(0)
def ConcessionariasList():
    concessionarias = db.execute("SELECT * FROM concessionarias")
    return render_template("/pages/concessionarias.html", aba="list", concessionarias=concessionarias)


@app.route("/concessionarias/add", methods=["GET", "POST"])
@login_required
@access_level_required(0)
def ConcessionariasAdd():

    if request.method == "POST":
        name = request.form.get("name")

        names = [n["name"] for n in db.execute("SELECT name FROM concessionarias")]
        if name in names:
            return apology("This name already exists")

        db.execute("INSERT INTO concessionarias (name) VALUES (?)", name)

        return redirect("/concessionarias/list")

    return render_template("/pages/concessionarias.html", aba="add")


@app.route("/concessionarias/tarifas/<int:id>", methods=["GET"])
@login_required
@access_level_required(0)
def ConcessionariasTarifas(id):
    concessionarias_tarifas = db.execute("SELECT * FROM concessionarias_tarifas WHERE concessionaria_id=?", id)
    concessionaria = db.execute("SELECT * FROM concessionarias WHERE id=?", id)[0]
    return render_template("/pages/concessionarias.html", aba="tarifas", concessionarias_tarifas=concessionarias_tarifas, concessionaria=concessionaria)


@app.route("/concessionarias/tarifas/<int:id>/add", methods=["GET", "POST"])
@login_required
@access_level_required(0)
def ConcessionariasTarifasAdd(id):

    if request.method == "POST":
        grupo_tarifario = request.form.get("grupo_tarifario")
        modalidade = request.form.get("modalidade")
        subgrupo = request.form.get("subgrupo")
        demanda_ponta = request.form.get("demanda_ponta")
        demanda_fora_ponta = request.form.get("demanda_fora_ponta")
        ultrapassagem_demanda_ponta = request.form.get("ultrapassagem_demanda_ponta")
        ultrapassagem_demanda_fora_ponta  = request.form.get("ultrapassagem_demanda_fora_ponta")
        demanda_verde = request.form.get("demanda_verde")
        ultrapassagem_demanda_verde = request.form.get("ultrapassagem_demanda_verde")
        consumo_ponta = request.form.get("consumo_ponta")
        consumo_fora_ponta = request.form.get("consumo_fora_ponta")
        consumo_b = request.form.get("consumo_b")
        


        db.execute("INSERT INTO concessionarias_tarifas (concessionaria_id, grupo_tarifario, modalidade, subgrupo, demanda_ponta, demanda_fora_ponta, ultrapassagem_demanda_ponta, ultrapassagem_demanda_fora_ponta, demanda_verde, ultrapassagem_demanda_verde, consumo_ponta, consumo_fora_ponta, consumo_b) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?)",
            id,
            grupo_tarifario,
            modalidade,
            subgrupo,
            demanda_ponta,
            demanda_fora_ponta,
            ultrapassagem_demanda_ponta,
            ultrapassagem_demanda_fora_ponta,
            demanda_verde,
            ultrapassagem_demanda_verde,
            consumo_ponta,
            consumo_fora_ponta,
            consumo_b
        )

        return redirect(f"/concessionarias/tarifas/{id}")

    concessionaria = db.execute("SELECT * FROM concessionarias WHERE id=?", id)[0]
    return render_template("/pages/concessionarias.html", aba="add_tarifa", concessionaria=concessionaria)

@app.route("/concessionarias/tarifas/<int:id>/edit/<int:tarifa_id>", methods=["GET", "POST"])
@login_required
@access_level_required(0)
def ConcessionariasTarifasEdit(id, tarifa_id):

    if request.method == "POST":
        grupo_tarifario = request.form.get("grupo_tarifario")
        modalidade = request.form.get("modalidade")
        subgrupo = request.form.get("subgrupo")
        demanda_ponta = request.form.get("demanda_ponta")
        demanda_fora_ponta = request.form.get("demanda_fora_ponta")
        ultrapassagem_demanda_ponta = request.form.get("ultrapassagem_demanda_ponta")
        ultrapassagem_demanda_fora_ponta  = request.form.get("ultrapassagem_demanda_fora_ponta")
        demanda_verde = request.form.get("demanda_verde")
        ultrapassagem_demanda_verde = request.form.get("ultrapassagem_demanda_verde")
        consumo_ponta = request.form.get("consumo_ponta")
        consumo_fora_ponta = request.form.get("consumo_fora_ponta")
        consumo_b = request.form.get("consumo_b")
        


        db.execute("UPDATE concessionarias_tarifas SET demanda_ponta=?, demanda_fora_ponta=?, ultrapassagem_demanda_ponta=?, ultrapassagem_demanda_fora_ponta=?, demanda_verde=?, ultrapassagem_demanda_verde=?, consumo_ponta=?, consumo_fora_ponta=?, consumo_b=? WHERE id = ?",
            demanda_ponta,
            demanda_fora_ponta,
            ultrapassagem_demanda_ponta,
            ultrapassagem_demanda_fora_ponta,
            demanda_verde,
            ultrapassagem_demanda_verde,
            consumo_ponta,
            consumo_fora_ponta,
            consumo_b,
            tarifa_id
        )

        return redirect(f"/concessionarias/tarifas/{id}")
    
    tarifa = db.execute("SELECT * FROM concessionarias_tarifas WHERE id=?", tarifa_id)[0]
    concessionaria = db.execute("SELECT * FROM concessionarias WHERE id=?", id)[0]

    return render_template("/pages/concessionarias.html", aba="edit", tarifa=tarifa, concessionaria=concessionaria)


@app.route("/concessionarias/delete/<int:id>", methods=["GET"])
@login_required
@access_level_required(0)
def ConcessionariasDelete(id):
    db.execute("DELETE FROM concessionarias WHERE id=?", id)

    return redirect("/concessionarias/list")

@app.route("/concessionarias/tarifas/<int:id>/delete/<int:tarifa_id>", methods=["GET"])
@login_required
@access_level_required(0)
def ConcessionariasTarifasDelete(id, tarifa_id):
    db.execute("DELETE FROM concessionarias_tarifas WHERE id=?", tarifa_id)

    return redirect(f"/concessionarias/tarifas/{id}")