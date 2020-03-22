#!/usr/bin/env python3

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

from app import app

from threading import Thread
import time
import requests
import tkinter
import webbrowser

#===========Tkinter GUI for Launching the App=============
# This thread runs the Flask app.

app_thread = None

def appThread():
    global app
    app.run(host = "127.0.0.1", port = 5000)

# This thread is started by the "Start Server" button callback. It starts the Flask app in another thread, waits 1 second, then opens the browser.
def startAppThreadThread():
    global app_thread
    app_thread = Thread(target = appThread)
    app_thread.start()
    time.sleep(1)
    webbrowser.open("http://localhost:5000")

# This callback fires when the "Start Server" button is pressed. Since callbacks block the main thread, it spawns a new thread to do the work.
def startServerButtonPressed():
    start_app_thread_thread = Thread(target = startAppThreadThread)
    start_app_thread_thread.start()

# This callback fires when the Tkinter GUI window is closed.
def handleWindowDestroy():
    requests.post("http://localhost:5000/shutdown")
    exit()

root = tkinter.Tk()
root.title("HereSpace Server Controller")
root.protocol("WM_DELETE_WINDOW", handleWindowDestroy)
tkinter.Label(root, text = "This interface controls the HereSpace server. Press \"Start Server\" to start the server and automatically open a browser.").grid(row = 0, column = 0)
tkinter.Button(root, text = "Start Server", command = startServerButtonPressed).grid(row = 1, column = 0)
tkinter.mainloop()
