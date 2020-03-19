#!/usr/bin/env python3

#=========Imports===========

from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for

from storage.databasestorage import DatabaseStorage

from loginform import LoginForm

from pathlib import Path

from multiprocessing import Process

import time

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk
gi.require_version('WebKit2', '4.0')
from gi.repository import WebKit2

import requests

#=========Database Setup===========
database_path = Path.home().joinpath("herespace.db")
database_storage = DatabaseStorage(str(database_path))

#=========Flask Setup==========
app = Flask(__name__)
app.config["SECRET_KEY"] = "alsdkjfl;awehjtoipqglkajdsflkasjdfl;lkajwelihwekja;sdl"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    print("Loading user...")
    return database_storage.loadUser(user_id)

#========Flask Routes Setup==========
# Webpage routes.
import home_route
import index_route
import login_route
import logout_route
import signup_route
import klass_route
import create_klass_route
# API routes (used for AJAX requests).
import get_students_route
import delete_student_route
import create_student_route
import create_klass_route
import get_seatings_route
import get_assignments_route
import create_assignment_route
import delete_assignment_route
import get_scores_route
import add_score_route
import shutdown_route

#===========WebKit/GTK GUI To Access the Web App on Desktop=============

# This process runs the Flask app.
app_process = None
def appProcess():
    app.run(host = "127.0.0.1", port = 5000)

def closeApplication(_):
    requests.post("http://localhost:5000/shutdown")
    Gtk.main_quit()
    exit()

if __name__ == "__main__":
    app_process = Process(target = appProcess)
    app_process.start()
    time.sleep(1)

    window = Gtk.Window()
    window.set_title("HereSpace")
    window.connect("destroy", closeApplication)
    window.maximize()

    browser = WebKit2.WebView()
    browser.load_uri("http://localhost:5000")
    window.add(browser)

    window.show_all()
    Gtk.main()
