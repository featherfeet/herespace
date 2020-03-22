"""
This file sets up (but does not yet run) the Flask app instance and its associated DB.
"""

#=========Imports===========
from flask_login import LoginManager
from flask import Flask

from storage.databasestorage import DatabaseStorage

from pathlib import Path
import os

#=========Database Setup===========
database_path = Path.home().joinpath("herespace.db")
database_storage = DatabaseStorage(str(database_path))

#=========Flask Setup==========
app = Flask(__name__, template_folder = "templates", root_path = os.getcwd())
app.config["SECRET_KEY"] = "alsdkjfl;awehjtoipqglkajdsflkasjdfl;lkajwelihwekja;sdl"
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    print("Loading user...")
    return database_storage.loadUser(user_id)
