from flask import Flask, render_template, jsonify, url_for, request, flash,\
                  redirect, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_github import GitHub



app = Flask(__name__)

#github = GitHub(app)

api_route = API_ROUTE


@app.route('/')
def hello_world():
  return 'Hello from Flask!'

if __name__ == '__main__':
  app.run()