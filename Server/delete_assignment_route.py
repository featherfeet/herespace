from app import app, database_storage
from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for, Response
import json

@app.route("/delete_assignment", methods = ["POST"])
@login_required
def delete_assignment():
    database_storage.deleteAssignmentByAssignmentId(current_user.get_id(), request.form["assignment_id"])
    return "OK"
