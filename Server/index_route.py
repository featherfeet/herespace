from app import app
from flask import render_template, Flask, request, redirect, url_for

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")
