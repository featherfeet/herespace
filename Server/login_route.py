from app import app, database_storage
from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for, flash
from storage.databasestorage import DatabaseStorage
from loginform import LoginForm

@app.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        form = LoginForm()
        if form.validate_on_submit():
            user = database_storage.verifyUser(form.username.data, form.password.data)
            if user is None:
                flash("Invalid credentials.")
                return redirect(url_for("login"))
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("You must fill in all fields.")
            return redirect(url_for("login"))
    elif request.method == "GET":
        return render_template("login.html", form = LoginForm())
