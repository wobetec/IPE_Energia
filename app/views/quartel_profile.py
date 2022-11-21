from flask import redirect, render_template, request, session
from werkzeug.utils import secure_filename

from app import app, db
from app.helpers import (access_level_required, allowed_file, apology,
                         login_required)
from app.var import UPLOAD_FOLDER, GRUPOS_TARIFARIOS


@app.route("/quartel_profile/edit", methods=["GET", "POST"])
@login_required
@access_level_required(1)
def quartel_profileEdit():
    if request.method == "POST":
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

        db.execute(
            "UPDATE quarteis SET efetivo=?, area=?, concessionaria_id=?, grupo_tarifario=?, modalidade=?, subgrupo=?, tem_subordinado=?, tem_geracao_distribuida=?, tolerancia_ultrapassagem_demanda=? WHERE id = ?",
            efetivo,
            area,
            concessionaria_id,
            grupo_tarifario,
            modalidade,
            subgrupo,
            tem_subordinado,
            tem_geracao_distribuida,
            tolerancia_ultrapassagem_demanda,
            session["quartel"]["quartel_id"]
        )


        db.execute(
            "UPDATE quarteis_demanda_contratada SET umida_ponta = ?, umida_fora_ponta = ?, seca_ponta = ?, seca_fora_ponta = ?, umida = ?, seca = ? WHERE quartel_id=?",
            umida_ponta,
            umida_fora_ponta,
            seca_ponta,
            seca_fora_ponta,
            umida,
            seca,
            session["quartel"]["quartel_id"]
        )

        return redirect("/quartel_profile")

    infos = db.execute("SELECT * FROM quarteis WHERE id=?", session["quartel"]["quartel_id"])[0]
    demandas = db.execute("SELECT * FROM quarteis_demanda_contratada WHERE quartel_id=?", session["quartel"]["quartel_id"])[0]
    concs = db.execute("SELECT id, name FROM concessionarias")

    return render_template("pages/quartel_profile.html", aba="edit", infos=infos, demandas=demandas, concessionarias=concs)



@app.route("/quartel_profile/brasao", methods=["GET", "POST"])
@login_required
@access_level_required(1)
def quartel_profileBrasao():
    if request.method == 'POST':
        quartel_id = session["quartel"]["quartel_id"]
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            name = f"{quartel_id}.{file.filename.rsplit('.', 1)[1].lower()}"
            filename = secure_filename(name)
            file.save(UPLOAD_FOLDER+filename)
        
            db.execute("UPDATE quarteis SET brasao = ? WHERE id = ?", name, quartel_id)
            session["quartel"]["brasao"] = name

            return redirect(request.url)


    return render_template("pages/quartel_profile.html", aba="brasao")


@app.route("/quartel_profile", methods=["GET"])
@app.route("/quartel_profile/perfil", methods=["GET"])
@login_required
@access_level_required(2)
def quartel_profilePerfil():

    infos = db.execute("SELECT * FROM quarteis WHERE id=?", session["quartel"]["quartel_id"])[0]

    infos["concessionaria_id"] = db.execute(
        "SELECT name FROM concessionarias WHERE id = ? ",
        infos["concessionaria_id"]
    )[0]["name"]
    infos["subgrupo"] = GRUPOS_TARIFARIOS[infos["grupo_tarifario"]]["SUBGRUPO"][infos["subgrupo"]]

    demandas = db.execute("SELECT * FROM quarteis_demanda_contratada WHERE quartel_id=?", infos["id"])[0]

    return render_template("pages/quartel_profile.html", aba="perfil", infos=infos, demandas=demandas)


