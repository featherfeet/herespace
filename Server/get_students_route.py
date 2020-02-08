from __main__ import app, database_storage
from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for, Response
import json

@app.route("/get_students")
@login_required
def get_students():
    students = database_storage.fetchStudents(current_user.get_id())
    students_dicts = []
    for student in students:
        students_dicts.append(student.__dict__)
    json_students = json.dumps(students_dicts)
    return Response(json_students, content_type = "application/json")
