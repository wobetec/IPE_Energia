from app import app, db
from flask import render_template
from app.helpers import (
    login_required,
    access_level_required,
)
from datetime import datetime

@app.route("/", methods=["GET", "POST"])
@login_required
@access_level_required(None)
def index():

    return render_template("pages/dashboard.html")

