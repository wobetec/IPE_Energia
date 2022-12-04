from app import app, db
from flask import redirect, render_template, request, session
from app.helpers import apology, login_required, access_level_required


@app.route("/despesa", methods=["GET", "POST"])
@app.route("/despesa/add", methods=["GET", "POST"])
@login_required
@access_level_required(2)
def despesaAdd():
    if request.method == "POST":

        infos = db.execute("SELECT * FROM quarteis WHERE id = ?", 
            session["quartel"]["quartel_id"]
        )[0]

        tarifas = db.execute("SELECT * FROM concessionarias_tarifas WHERE concessionaria_id = ? AND grupo_tarifario = ? AND modalidade = ? AND subgrupo = ?",
            infos["concessionaria_id"],
            infos["grupo_tarifario"],
            infos["modalidade"],
            infos["subgrupo"],
        )[0]

        demandas = db.execute("SELECT * FROM quarteis_demanda_contratada WHERE quartel_id = ?", session["quartel"]["quartel_id"])[0]

        #despesas
        quartel_id = session["quartel"]["quartel_id"]
        efetivo = infos["efetivo"]
        area = infos["area"]
        valor = request.form.get("valor")
        multa = request.form.get("multa")
        data_fatura = request.form.get("data_fatura")

        #despesas_demanda_contratada
        umida_ponta = demandas["umida_ponta"]
        umida_fora_ponta = demandas["umida_fora_ponta"]
        seca_ponta = demandas["seca_ponta"]
        seca_fora_ponta = demandas["seca_fora_ponta"]
        umida = demandas["umida"]
        seca = demandas["seca"]

        #despesas_tarifas
        demanda_ponta = tarifas["demanda_ponta"]
        demanda_fora_ponta = tarifas["demanda_fora_ponta"]
        ultrapassagem_demanda_ponta = tarifas["ultrapassagem_demanda_ponta"]
        ultrapassagem_demanda_fora_ponta = tarifas["ultrapassagem_demanda_fora_ponta"]
        demanda_verde = tarifas["demanda_verde"]
        ultrapassagem_demanda_verde = tarifas["ultrapassagem_demanda_verde"]
        consumo_ponta = tarifas["consumo_ponta"]
        consumo_fora_ponta = tarifas["consumo_fora_ponta"]
        consumo_b = tarifas["consumo_b"]

        #despesas_consumo
        energia_ativa = request.form.get("energia_ativa")
        energia_reativa = request.form.get("energia_reativa")
        ponta = request.form.get("ponta")
        fora_ponta = request.form.get("fora_ponta")
        demanda_consumida = request.form.get("demanda_consumida")
        demanda_consumida_ponta = request.form.get("demanda_consumida_ponta")
        demanda_consumida_fora_ponta = request.form.get("demanda_consumida_fora_ponta")
        

        despesa_id = db.execute(
            "INSERT INTO despesas (quartel_id, valor, efetivo, area, data_fatura, multa) VALUES(?,?,?,?,?,?)",
            quartel_id,
            valor,
            efetivo,
            area,
            data_fatura,
            multa,
        )

        db.execute(
            "INSERT INTO despesas_demanda_contratada (despesa_id, umida_ponta, umida_fora_ponta, seca_ponta, seca_fora_ponta, umida, seca) VALUES(?,?,?,?,?,?,?)",
            despesa_id, 
            umida_ponta,
            umida_fora_ponta,
            seca_ponta,
            seca_fora_ponta,
            umida,
            seca,
        )

        db.execute(
            "INSERT INTO despesas_tarifas (despesa_id, demanda_ponta, demanda_fora_ponta, ultrapassagem_demanda_ponta, ultrapassagem_demanda_fora_ponta, demanda_verde, ultrapassagem_demanda_verde, consumo_ponta, consumo_fora_ponta, consumo_b) VALUES(?,?,?,?,?,?,?,?,?,?)",
            despesa_id,
            demanda_ponta,
            demanda_fora_ponta,
            ultrapassagem_demanda_ponta,
            ultrapassagem_demanda_fora_ponta,
            demanda_verde,
            ultrapassagem_demanda_verde,
            consumo_ponta,
            consumo_fora_ponta,
            consumo_b,
        )
       
        db.execute(
            "INSERT INTO despesas_consumo (despesa_id, energia_ativa, energia_reativa, ponta, fora_ponta, demanda_consumida, demanda_consumida_ponta, demanda_consumida_fora_ponta) VALUES(?,?,?,?,?,?,?,?)",
            despesa_id,
            energia_ativa,
            energia_reativa,
            ponta,
            fora_ponta,
            demanda_consumida,
            demanda_consumida_ponta,
            demanda_consumida_fora_ponta,
        )

        return redirect("/despesa/list")

    infos = db.execute("SELECT * FROM quarteis WHERE id = ?", session["quartel"]["quartel_id"])[0]

    return render_template("pages/despesas.html", aba="add", infos=infos)


@app.route("/despesa/edit/<int:id>", methods=["GET", "POST"])
@login_required
@access_level_required(2)
def despesaEdit(id=None):
    if request.method == "POST":
        valor = request.form.get("valor")
        multa = request.form.get("multa")
        data_fatura = request.form.get("data_fatura")

        energia_ativa = request.form.get("energia_ativa")
        energia_reativa = request.form.get("energia_reativa")
        ponta = request.form.get("ponta")
        fora_ponta = request.form.get("fora_ponta")
        demanda_consumida = request.form.get("demanda_consumida")
        demanda_consumida_ponta = request.form.get("demanda_consumida_ponta")
        demanda_consumida_fora_ponta = request.form.get("demanda_consumida_fora_ponta")

        db.execute("UPDATE despesas SET valor=?, multa=?, data_fatura=? WHERE id=?",
            valor,
            multa,
            data_fatura,
            id
        )
        db.execute("UPDATE despesas_consumo SET energia_ativa = ? , energia_reativa = ? , ponta = ? , fora_ponta = ? , demanda_consumida = ? , demanda_consumida_ponta = ? , demanda_consumida_fora_ponta = ? WHERE despesa_id=?",
            energia_ativa,
            energia_reativa,
            ponta,
            fora_ponta,
            demanda_consumida,
            demanda_consumida_ponta,
            demanda_consumida_fora_ponta,
            id
        )

        return redirect("/despesa/list")

    infos = db.execute("SELECT * FROM quarteis WHERE id = ?", session["quartel"]["quartel_id"])[0]
    despesa = db.execute("SELECT * FROM despesas WHERE id=?", id)[0]
    despesa_consumo = db.execute("SELECT * FROM despesas_consumo WHERE despesa_id=?", id)[0]

    return render_template("pages/despesas.html", aba="edit", despesa=despesa, despesa_consumo=despesa_consumo, infos=infos)


@app.route("/despesa/list", methods=["GET"])
@login_required
@access_level_required(2)
def despesaList():
    despesas = db.execute(
        "SELECT * FROM despesas WHERE quartel_id=?",
        session["quartel"]["quartel_id"],
    )
    return render_template("pages/despesas.html", aba="list", despesas=despesas)


@app.route("/despesa/delete/<int:id>", methods=["GET"])
@login_required
@access_level_required(2)
def despesaDelete(id):
    db.execute("DELETE FROM despesas WHERE id=?", id)

    return redirect("/despesa/list")

