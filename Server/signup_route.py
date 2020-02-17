from __main__ import app, database_storage
from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for
from storage.databasestorage import DatabaseStorage
from signupform import SignupForm

@app.route("/signup", methods = ["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        form = SignupForm()
        if form.validate_on_submit():
            user = database_storage.createTeacherUser(form.username.data, form.password.data, form.email.data)
            login_user(user)
            return redirect(url_for("home"))
    elif request.method == "GET":
        return render_template("signup.html", form = SignupForm())
