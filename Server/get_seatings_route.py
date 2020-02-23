from __main__ import app, database_storage
from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for, Response
import json

@app.route("/get_seatings", methods = ["GET"])
@login_required
def get_seatings():
    klass_id = int(request.args.get("klass_id"))

    seatings = database_storage.fetchSeatingsByKlassId(current_user.get_id(), klass_id)
    json_seatings = json.dumps(seatings, default = lambda obj: obj.__dict__)

    return Response(json_seatings, content_type = "application/json")
