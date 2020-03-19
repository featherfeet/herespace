from __main__ import app, database_storage
from flask import request

@app.route("/shutdown", methods = ["POST"])
def shutdown():
    database_storage.close()
    shutdown_function = request.environ.get("werkzeug.server.shutdown")
    if shutdown_function is None:
        print("Werkzeug Server is not running.")
        return ""
    shutdown_function()
    return ""
