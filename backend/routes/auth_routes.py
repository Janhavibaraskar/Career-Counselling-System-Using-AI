from flask import Blueprint, render_template, request, redirect, url_for, session
from backend.models.user_model import db, User

auth = Blueprint("auth", __name__)


# ---------------- LOGIN ----------------
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(email=email, password=password).first()

        if user:
            session["user_id"] = user.id
            return redirect(url_for("assessment"))
        else:
            return "Invalid email or password"

    return render_template("login.html")


# ---------------- SIGNUP ----------------
@auth.route("/signup", methods=["GET", "POST"])
def signup():

    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        new_user = User(name=name, email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login"))

    return render_template("signup.html")


# ---------------- LOGOUT ----------------
@auth.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("home"))