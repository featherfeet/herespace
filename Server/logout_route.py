from __main__ import app
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask import render_template, Flask, request, redirect, url_for

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))
