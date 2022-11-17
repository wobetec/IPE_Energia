from app import app, db
from flask import redirect, render_template, request, session
from app.helpers import apology, login_required, recursive_get_subordinados, access_level_required



@app.route("/quartel_profile", methods=["GET"])
@app.route("/quartel_profile/edit", methods=["GET", "POST"])
@login_required
@access_level_required(3)
def quartel_profileEdit():
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

    return render_template("pages/quartel_profile.html", aba="edit", quartel=quartel)


