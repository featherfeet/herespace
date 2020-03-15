#!/usr/bin/env python3

#=========Imports===========

from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for

from storage.databasestorage import DatabaseStorage

from loginform import LoginForm

from pathlib import Path

import tkinter
import webbrowser

from threading import Thread
from multiprocessing import Process

import time

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

#===========Tkinter GUI for Launching the App=============

# This thread runs the Flask app.

app_process = None

def appProcess():
    app.run(host = "127.0.0.1", port = 5000)

# This process is started by the "Start Server" button callback. It starts the Flask app in another process, waits 1 second, then opens the browser.
def startAppProcessThread():
    global app_process
    app_process = Process(target = appProcess)
    app_process.start()
    time.sleep(1)
    webbrowser.open("http://localhost:5000")

# This callback fires when the "Start Server" button is pressed. Since callbacks block the main process, it spawns a new process to do the work.
def startServerButtonPressed():
    start_app_process_thread = Thread(target = startAppProcessThread)
    start_app_process_thread.start()

# This callback fires when the Tkinter GUI window is closed.
def handleWindowDestroy():
    app_process.terminate()
    exit()

# Set up the Tkinter GUI.
if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("HereSpace Server Controller")
    root.protocol("WM_DELETE_WINDOW", handleWindowDestroy)
    tkinter.Label(root, text = "This interface controls the HereSpace server. Press \"Start Server\" to start the server and automatically open a browser.").grid(row = 0, column = 0)
    tkinter.Button(root, text = "Start Server", command = startServerButtonPressed).grid(row = 1, column = 0)
    tkinter.mainloop()
