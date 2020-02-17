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
        user_id = current_user.get_id()
        raw_json_data = request.form["json"]
        try:
            json_data = json.loads(raw_json_data)
        except JSONDecodeError:
            return "Malformed JSON."
        klass_name = json_data["klass_name"]
        klass_id = database_storage.createKlass(user_id, klass_name)
        seatings = json_data["seatings"]
        for seating in seatings:
            student_schedule = seating["student_schedule"]
            student_id = student_schedule["student"]["student_id"]
            student_schedule_id = database_storage.createStudentSchedule(user_id, student_id, klass_id)
            database_storage.createSeating(user_id, student_schedule_id, seating["desk_x"], seating["desk_y"], seating["desk_width"], seating["desk_height"], seating["desk_angle"])
        return "OK"
