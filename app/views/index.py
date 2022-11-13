from app import app, db
from flask import redirect, render_template, request, session, url_for
import os
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename
from app.helpers import (
    apology,
    login_required,
    recursive_get_subordinados,
    access_level_required,
)
from app.var import ACCESS_LEVEL


@app.route("/", methods=["GET", "POST"])
@login_required
@access_level_required(None)
def index():

    return render_template("index.html")

