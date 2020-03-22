from app import app, database_storage
from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for, Response
import json

@app.route("/add_score", methods = ["POST"])
@login_required
def add_score():
    user_id = int(current_user.get_id())
    assignment_id = int(request.form["assignment_id"])
    student_schedule_id = int(request.form["student_schedule_id"])
    points = float(request.form["points"])

    score_id = database_storage.addScore(user_id, assignment_id, student_schedule_id, points)

    return str(score_id)
