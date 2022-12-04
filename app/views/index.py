from app import app, db
from flask import redirect, render_template, request, session, url_for, g
import os
import json
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from app.helpers import (
    apology,
    login_required,
    recursive_get_subordinados,
    access_level_required,
)
from app.var import ACCESS_LEVEL


@app.route("/", methods=["GET"])
@login_required
@access_level_required(None)
def index():
    last12 = db.execute('SELECT * FROM despesas_consumo JOIN despesas ON despesas.id = despesas_consumo.despesa_id WHERE despesas.quartel_id = ? ORDER BY despesas.data_fatura DESC LIMIT 12', session['quartel']['quartel_id'])
    om_info = db.execute('SELECT * FROM quarteis WHERE id = ?', session['quartel']['quartel_id'])

    data_last12 = [x['data_fatura'] for x in last12]
    energia_ativa = [x['energia_ativa'] for x in last12]
    energia_reativa = [x['energia_reativa'] for x in last12]
    
    efetivo_om = [x['efetivo'] for x in om_info]
    area_om = [x['area'] for x in om_info]
    sigla_om = [x['sigla'] for x in om_info]
    grupo_tarifario = [x['grupo_tarifario'] for x in om_info]


    consumo_mensal_last12 = []
    consumo_total_last12 = 0
    if grupo_tarifario[0] == 'A':
        consumo_ponta = [x['ponta'] for x in last12]
        consumo_fora_ponta = [x['fora_ponta'] for x in last12]
        consumo_mensal_last12 = [consumo_fora_ponta[i] + consumo_ponta[i] for i in range(len(last12))]
        consumo_total_last12 = sum(consumo_mensal_last12)
    elif grupo_tarifario[0] == 'B':
        consumo_mensal_last12 = [x['energia_ativa'] + x['energia_reativa'] for x in last12]
        consumo_total_last12 = sum(consumo_mensal_last12)
    
    fator_pot = [energia_ativa[i]/(((energia_ativa[i])**2 + (energia_reativa[i])**2)**(0.5)) for i in range(len(last12))]

    data_last12.reverse()
    consumo_mensal_last12.reverse()
    fator_pot.reverse()
    energia_reativa.reverse()
    energia_ativa.reverse()
    return render_template("pages/dashboard.html", consumo_mensal=consumo_mensal_last12, consumo_total=consumo_total_last12, data_mensal=data_last12, fator_pot=fator_pot, energia_ativa=energia_ativa, energia_reativa=energia_reativa, efetivo=efetivo_om, area=area_om, sigla_om=sigla_om)
