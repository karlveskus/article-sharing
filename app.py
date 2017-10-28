from flask import Flask, render_template, jsonify
from flask.ext.sqlalchemy import SQLAlchemy

from models import Article
from database_seed import base_query, database_seed

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///catalog.db')

DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

app.secret_key = 'secret'
api_route = '/api'


# Routes
@app.route('/')
def index():
    """ index page """
    database_seed(session)

    topics, articles = base_query(session)
    return render_template('topics.html', topics=topics, articles=articles)


@app.route('/topics/<topic_id>/articles')
def view_topics(topic_id):
    """ show filtered articles """
    topics, _articles = base_query(session)
    articles = session.query(Article).filter_by(topic_id=topic_id)

    return render_template('topics.html', topics=topics, articles=articles)


# API JSON routes
@app.route(api_route + '/topics')
def get_topics():
    """ route for topics """
    topics, _ = base_query(session)
    return jsonify(topics=[p.serialize for p in topics])


@app.route('/articles')
def get_articles():
    """ route for all articles """
    _, articles = base_query(session)
    return jsonify(articles=[p.serialize for p in articles])


@app.route(api_route + '/topics/<topic_id>/articles')
def get_topics_articles(topic_id):
    """ route for articles """
    articles = session.query(Article).filter_by(topic_id=topic_id)
    return jsonify(articles=[p.serialize for p in articles])


# Server
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
