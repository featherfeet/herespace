#!/usr/bin/env python3

from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for
from storage.databasestorage import DatabaseStorage
from loginform import LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "alsdkjfl;awehjtoipqglkajdsflkasjdfl;lkajwelihwekja;sdl"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
database_storage = DatabaseStorage("herespace.db")

@login_manager.user_loader
def load_user(user_id):
    print("loading")
    return database_storage.loadUser(user_id)

@app.route("/login", methods = ["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "POST":
        form = LoginForm()
        if form.validate_on_submit():
            user = database_storage.verifyUser(form.username.data, form.password.data)
            if user is None:
                return redirect(url_for("login"))
            login_user(user)
            return redirect(url_for("home"))
    elif request.method == "GET":
        return render_template("login.html", form = LoginForm())

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/home")
@login_required
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
