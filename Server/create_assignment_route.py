from __main__ import app, database_storage
from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for, Response
import json

@app.route("/create_assignment", methods = ["POST"])
@login_required
def create_assignment():
    assignment_name = request.form["assignment_name"]
    assignment_points = request.form["assignment_points"]
    klass_id = request.form["klass_id"]
    if assignment_name == "":
        return "assignment_name parameter required."
    if assignment_points == "":
        return "assignment_points parameter required."
    if klass_id == "":
        return "klass_id parameter required."
    assignment_id = database_storage.createAssignment(current_user.get_id(), klass_id, assignment_name, assignment_points)
    return str(assignment_id)
