from app import app, database_storage
from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for

@app.route("/home")
@login_required
def home():
    klasses = database_storage.fetchKlassesByUserId(current_user.get_id())
    return render_template("home.html", klasses = klasses)
