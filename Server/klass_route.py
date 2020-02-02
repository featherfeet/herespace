from __main__ import app, database_storage
from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for

@app.route("/klass")
@login_required
def klass():
    klass_id = int(request.args.get("klass_id"))
    klass = database_storage.fetchKlassByKlassId(klass_id)
    return render_template("klass.html", klass = klass)
