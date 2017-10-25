from flask import Flask, flash, g, jsonify, redirect, render_template, request, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route('/')
def index():
    """ index page """
    return("Hello world")

if __name__ == '__main__':
    app.debug = True;
    app.run(host='0.0.0.0', port=5000)