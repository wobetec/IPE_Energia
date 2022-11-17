from app import app, db
from flask import redirect, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from app.helpers import apology, login_required, access_level_required


@app.route("/profile", methods=["GET"])
@app.route("/profile/change_password", methods=["GET", "POST"])
@login_required
def userProfile():

    if request.method == "POST":
        id = session["user_id"]
        user = db.execute("SELECT * FROM users WHERE id = ?", id)[0]

        old = request.form.get("old")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not check_password_hash(user["hash"], old):
            apology("wrong old password")
        elif password == "" or password != confirmation:
            return apology("Password is blank or the passwords do not match")
        
        hashed = generate_password_hash(password)
        db.execute(
            "UPDATE users SET hash = ? WHERE id = ?",
            hashed,
            id
        )

        return redirect("/")

    return render_template("pages/profile.html", aba="change_password")