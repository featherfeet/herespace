from app import app, database_storage
from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for, Response
import json

@app.route("/create_student", methods = ["POST"])
@login_required
def create_student():
    student_name = request.form["student_name"]
    if student_name == "":
        return "student_name parameter required."
    student_id = database_storage.createStudent(current_user.get_id(), student_name)
    return str(student_id)
