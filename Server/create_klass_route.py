from __main__ import app, database_storage
from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for
import json

@app.route("/create_klass", methods = ["GET", "POST"])
@login_required
def create_klass():
    if request.method == "GET":
        return app.send_static_file("create_klass.html")
    else:
        raw_json_data = request.form["json"]
        try:
            json_data = json.loads(raw_json_data)
        except JSONDecodeError:
            return "Malformed JSON."
        klass_name = json_data["klass_name"]
        klass_id = database_storage.createKlass(current_user.get_id(), klass_name)
        seatings = json_data["seatings"]
        for seating in seatings:
            print(seating)
        return "OK"
