from app import app, db
from flask import redirect, render_template, request, session
from app.helpers import apology, login_required, recursive_get_subordinados, access_level_required


@app.route("/quartel", methods=["GET"])
@app.route("/quartel/list", methods=["GET"])
@login_required
@access_level_required(1)
def quartelList():
    subs = {
        session["quartel"]["sigla"]: recursive_get_subordinados(
            db, session["quartel"]["sigla"]
        )
    }
    
    return render_template("pages/quarteis.html", aba="list", subordinados=subs)


@app.route("/quartel/add", methods=["GET", "POST"])
@login_required
@access_level_required(1)
def quartelAdd():
    if request.method == "POST":
        name = request.form.get("name")
        sigla = request.form.get("sigla")
        sigla = sigla.replace(" ", "_")
        efetivo = request.form.get("efetivo")
        area = request.form.get("area")

        tolerancia_ultrapassagem_demanda = request.form.get("tolerancia_ultrapassagem_demanda")
        concessionaria_id = request.form.get("concessionaria_id")
        grupo_tarifario = request.form.get("grupo_tarifario")
        modalidade = request.form.get("modalidade")
        subgrupo = request.form.get("subgrupo")
        tem_subordinado = 1 if request.form.get("tem_subordinado") else 0
        tem_geracao_distribuida = 1 if request.form.get("tem_geracao_distribuida") else 0

        umida_ponta = request.form.get("umida_ponta")
        umida_fora_ponta = request.form.get("umida_fora_ponta")
        seca_ponta = request.form.get("seca_ponta")
        seca_fora_ponta = request.form.get("seca_fora_ponta")
        umida = request.form.get("umida")
        seca = request.form.get("seca")

        if not(
            name 
            and sigla 
            and efetivo 
            and area 
            and concessionaria_id 
            and grupo_tarifario 
            and subgrupo 
        ):
            return apology("missing")


        # adiciona em quarteis
        db.execute(
            "INSERT INTO quarteis (name, sigla, efetivo, area, concessionaria_id, grupo_tarifario, modalidade, subgrupo, tem_subordinado, tem_geracao_distribuida, tolerancia_ultrapassagem_demanda) VALUES(?,?,?,?,?,?,?,?,?,?,?)",
            name,
            sigla,
            efetivo,
            area,
            concessionaria_id,
            grupo_tarifario,
            modalidade,
            subgrupo,
            tem_subordinado,
            tem_geracao_distribuida,
            tolerancia_ultrapassagem_demanda
        )

        quartel_id = db.execute("SELECT id FROM quarteis WHERE name= ? ", name)[0]["id"]

        db.execute(
            "INSERT INTO quarteis_demanda_contratada (quartel_id, umida_ponta, umida_fora_ponta, seca_ponta, seca_fora_ponta, umida, seca) VALUES(?,?,?,?,?,?,?)",
            quartel_id,
            umida_ponta,
            umida_fora_ponta,
            seca_ponta,
            seca_fora_ponta,
            umida,
            seca 
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

    concs = db.execute("SELECT id, name FROM concessionarias")

    return render_template("pages/quarteis.html", aba="add", concessionarias=concs)


@app.route("/quartel/select/<string:sigla>", methods=["GET"])
@access_level_required(1)
@login_required
def quartelSelect(sigla):
    data = db.execute(
        "SELECT * FROM quarteis WHERE sigla=?",
        sigla,
    )[0]

    session["quartel"] = {
        "quartel_id": data["id"],
        "sigla": data["sigla"],
        "name": data["name"],
        "brasao": data["brasao"],
        "tem_subordinado": data["tem_subordinado"],
        "tem_geracao_distribuida": data["tem_geracao_distribuida"],
    }

    return redirect("/")

