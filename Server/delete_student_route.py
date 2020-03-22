from app import app, database_storage
from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for, Response
import json

@app.route("/delete_student", methods = ["POST"])
@login_required
def delete_student():
    database_storage.deleteStudentByStudentId(current_user.get_id(), request.form["student_id"])
    return "OK"
