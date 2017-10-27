from flask import Flask, render_template, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

from seed import base_query, seed_database

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///catalog.db')

DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

app.secret_key = 'secret'


# Routes
@app.route('/')
def index():
    """ index page """
    seed_database(session)
    return("jou")


@app.route('/topics')
def get_topics_json():
    """ route for topics """
    topics, _ = base_query(session)
    return jsonify(topics=[p.serialize for p in topics])


@app.route('/articles')
def get_articles_json():
    """ route for articles """
    _, articles = base_query(session)
    return jsonify(articles=[p.serialize for p in articles])


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
