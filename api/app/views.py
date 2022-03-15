from app import app
import config
from flask import render_template
import subprocess

@app.route('/')
def index():
    # TODO run background process
    # cmd = config.SUBPROCESS_CMD
    # subprocess.call(cmd)
    return render_template("index.html")

# HTTP error handling
# @app.errorhandler(404)
# def not_found(error):
#     return render_template('404.html'), 404
