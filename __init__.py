from flask import Flask, render_template, jsonify, url_for, request, flash,\
                  redirect, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_github import GitHub


DEBUG = True
SECRET_KEY = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'

DATABASE_CONNECTION = 'postgresql://catalog:password@localhost/catalog'
#DATABASE_CONNECTION = 'sqlite:///catalog.db'

GITHUB_CLIENT_ID = '7d4f47c88e6da7febbbb'
GITHUB_CLIENT_SECRET = 'ecb9f99a072a97dafb9cf7d4ae7974bf6e0a99ea'
API_ROUTE = '/api'



from datetime import date
import requests




app = Flask(__name__)

#github = GitHub(app)

api_route = API_ROUTE


@app.route('/')
def hello_world():
  return 'Hello from Flask!'

if __name__ == '__main__':
  app.run()