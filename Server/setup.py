import sys
from cx_Freeze import setup, Executable

# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
# Setting base to Win32GUI supresses the console on Windows but breaks Flask.
#if sys.platform == "win32":
#    base = "Win32GUI"

build_exe_options = {"include_files": ["storage", "createschema.sql", "static", "templates"],
                    "packages": ["sqlite3", "passlib"],
                    "includes": ["jinja2.ext"]}

setup(  name = "main",
        version = "0.0.1",
        description = "Classroom management software.",
        options = {"build_exe": build_exe_options},
        executables = [Executable("main.py", base=base)])
