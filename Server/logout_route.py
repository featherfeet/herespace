from __main__ import app
from flask_login import LoginManager, login_required, current_user, login_user, logout_user
from flask import render_template, Flask, request, redirect, url_for, flash

@app.route("/logout")
def logout():
    flash("Logout successful.")
    logout_user()
    return redirect(url_for("login"))
