from flask import Flask, render_template, jsonify, url_for, request, flash, redirect, session
from flask.ext.sqlalchemy import SQLAlchemy
import config

from models import Article, Topic, User
from database_seed import base_query, database_seed

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask.ext.github import GitHub

engine = create_engine(config.DATABASE_CONNECTION)
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

app = Flask(__name__)
app.debug = config.DEBUG
app.secret_key = config.SECRET_KEY

app.config['GITHUB_CLIENT_ID'] = config.GITHUB_CLIENT_ID
app.config['GITHUB_CLIENT_SECRET'] = config.GITHUB_CLIENT_SECRET
github = GitHub(app)

api_route = config.API_ROUTE


# Github auth
@app.route('/login')
def login():
    """ login route """
    return github.authorize(redirect_uri=url_for('authorized', _external=True))


@app.route('/logout')
def logout():
    """ logout route """
    session.pop('user_id', None)
    session.pop('access_token', None)
    return redirect(url_for('index'))


@app.route('/github-callback')
@github.authorized_handler
def authorized(token):
    """ callback for github auth """
    redirect_to = request.args.get('next')
    if token is None:
        return redirect(redirect_to)

    user = db_session.query(User).filter_by(access_token=token).first()
    if user is None:
        user = User(access_token=token)
        db_session.add(user)

    user.access_token = token
    db_session.commit()

    session['user_id'] = user.id
    session['user_token'] = user.access_token

    return redirect(url_for('index'))


def authenticated():
    """ check if user is authenticated or not """
    if session.has_key('user_id') and session.has_key('user_token'):
        user = db_session.query(User).filter_by(id=session['user_id']).first()
        
        if user:
            return user.access_token == session['user_token']
    return False


# Routes
@app.route('/')
def index():
    """ index page """
    database_seed(db_session)

    topics, articles = base_query(db_session)
    return render_template('topics.html', topics=topics, articles=articles, is_authenticated=authenticated)


@app.route('/topics/<topic_id>/articles')
def view_topics(topic_id):
    """ show filtered articles """
    topics, _articles = base_query(db_session)
    articles = db_session.query(Article).filter_by(topic_id=topic_id)

    return render_template('topics.html', topics=topics, articles=articles, is_authenticated=authenticated)


# API JSON routes
@app.route(api_route + '/topics')
def get_topics():
    """ route for topics """
    topics, _ = base_query(db_session)
    return jsonify(topics=[p.serialize for p in topics])


@app.route(api_route + '/topics/<topic_id>/articles')
def get_topics_articles(topic_id):
    """ route for filtering articles by topic """
    articles = db_session.query(Article).filter_by(topic_id=topic_id)
    return jsonify(articles=[p.serialize for p in articles])


@app.route('/articles')
def get_articles():
    """ route for all articles """
    _, articles = base_query(db_session)
    return jsonify(articles=[p.serialize for p in articles])


# Server
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
