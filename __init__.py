from flask import Flask, render_template, jsonify, url_for, request, flash,\
                  redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_github import GitHub

import config
from models import Base, Article, Topic, User
from database_seed import base_query, database_seed

from datetime import date
import requests


app = Flask(__name__)




@app.route('/')
def hello_world():
  return 'Hello from Flask!'

if __name__ == '__main__':
  app.run()