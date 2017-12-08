from flask import Flask, render_template, jsonify, url_for, request, flash,\
                  redirect, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from flask_github import GitHub



engine = create_engine(config.DATABASE_CONNECTION)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

app = Flask(__name__)
app.config.from_object('config')

github = GitHub(app)

api_route = config.API_ROUTE


@app.route('/')
def hello_world():
  return 'Hello from Flask!'

if __name__ == '__main__':
  app.run()