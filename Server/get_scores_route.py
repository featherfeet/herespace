from __main__ import app, database_storage
from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for, Response
import json

@app.route("/get_scores", methods = ["GET"])
@login_required
def get_scores():
    assignment_id = int(request.args.get("assignment_id"))

    scores = database_storage.fetchMostRecentScoresByAssignmentId(current_user.get_id(), assignment_id)
    json_scores = json.dumps(scores, default = lambda obj: obj.__dict__)

    return Response(json_scores, content_type = "application/json")
