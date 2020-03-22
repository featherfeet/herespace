from app import app, database_storage
from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for, Response
import json

@app.route("/get_assignments", methods = ["GET"])
@login_required
def get_assignments():
    klass_id = int(request.args.get("klass_id"))
    assignments = database_storage.fetchAssignmentsByKlassId(current_user.get_id(), klass_id)

    json_assignments = json.dumps(assignments, default = lambda obj: obj.__dict__)

    return Response(json_assignments, content_type = "application/json")
