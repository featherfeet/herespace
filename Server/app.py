#!/usr/bin/env python3

from flask_login import LoginManager, login_required, current_user, login_user
from flask import render_template, Flask, request, redirect, url_for
from storage.databasestorage import DatabaseStorage
from loginform import LoginForm

app = Flask(__name__)
app.config["SECRET_KEY"] = "alsdkjfl;awehjtoipqglkajdsflkasjdfl;lkajwelihwekja;sdl"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
database_storage = DatabaseStorage("herespace.db")

@login_manager.user_loader
def load_user(user_id):
    print("loading")
    return database_storage.loadUser(user_id)

import home_route
import index_route
import login_route
import logout_route
import klass_route
import create_klass_route

if __name__ == "__main__":
    app.run(host = "0.0.0.0")
