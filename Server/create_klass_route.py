from __main__ import app, database_storage
from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for

@app.route("/create_klass")
@login_required
def create_klass():
    return app.send_static_file("create_klass.html")
