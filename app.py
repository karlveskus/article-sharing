from flask import Flask, render_template, jsonify, url_for, request, flash,\
                  redirect, session
from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask.ext.github import GitHub

import config
from models import Article, Topic, User
from database_seed import base_query, database_seed

from datetime import date
import requests

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
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/github-callback')
@github.authorized_handler
def authorized(token):
    """ callback for github auth """
    url = "https://api.github.com/user?access_token=" + str(token)
    req = requests.get(url)
    github_username = req.json()['login']

    redirect_to = request.args.get('next') or url_for('index')
    if token is None:
        return redirect(redirect_to)

    user = db_session.query(User).filter_by(github_username=github_username).first()
    if user is None:
        user = User(github_username=github_username)
        db_session.add(user)

    user.access_token = token
    db_session.commit()

    session['user_id'] = user.id
    session['access_token'] = user.access_token
    session['username'] = user.github_username

    return redirect(url_for('index'))


def authenticated():
    """ check if user is authenticated or not """
    if 'user_id' in session and 'access_token' in session:
        user = db_session.query(User).filter_by(id=session['user_id']).first()

        if user:
            return user.access_token == session['access_token']
    return False


def can_modify(article):
    """ check if article is added by the session user """
    return authenticated() and article.adder_id == session['user_id']


# HTML Routes
@app.route('/', methods=['GET'])
def index():
    """ index page """
    database_seed(db_session)

    topics, articles = base_query(db_session)
    return render_template('topics.html', can_modify=can_modify,
                           is_authenticated=authenticated,
                           topics=topics, articles=articles)


@app.route('/topics/<topic_id>/articles', methods=['GET'])
def view_topics(topic_id):
    """ show filtered articles """
    topics, _articles = base_query(db_session)
    articles = db_session.query(Article).filter_by(topic_id=topic_id)

    return render_template('topics.html', can_modify=can_modify,
                           is_authenticated=authenticated,
                           topics=topics, articles=articles)


@app.route('/articles/<article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    """ add new article """
    article = db_session.query(Article).filter_by(id=article_id).one()

    if not authenticated():
        return redirect(url_for('login'))

    if not can_modify(article):
        return redirect(url_for('index'))

    if request.method == 'GET':
        topics, _articles = base_query(db_session)

        return render_template('article_form.html',
                               is_authenticated=authenticated,
                               topics=topics, article=article)
    else:
        form = dict(request.form)

        article.title = form['article_title'][0]
        article.url = form['article_url'][0]
        article.description = form['article_description'][0]
        article.topic_id = form['article_topic_id'][0]

        db_session.add(article)
        db_session.commit()

        return redirect(url_for('index'))


@app.route('/articles/new', methods=['GET', 'POST'])
def new_article():
    """ add new article """
    if not authenticated():
        return redirect(url_for('login'))

    if request.method == 'GET':
        topics, _articles = base_query(db_session)
        article = {"title": "", "url": "", "description": "", "topic_id": None}

        return render_template('article_form.html',
                               is_authenticated=authenticated,
                               topics=topics, article=article)
    else:
        form = dict(request.form)

        article = Article(
            title=form['article_title'][0],
            url=form['article_url'][0],
            date_added=date.today(),
            description=form['article_description'][0],
            topic_id=form['article_topic_id'][0],
            adder_id=session['user_id']
        )

        db_session.add(article)
        db_session.commit()

        return redirect(url_for('index'))


# API JSON routes
@app.route(api_route + '/topics', methods=['GET'])
def get_topics():
    """ JSON route - return all topics """
    topics, _ = base_query(db_session)
    return jsonify(topics=[p.serialize for p in topics])


@app.route(api_route + '/topics/<topic_id>/articles', methods=['GET'])
def get_topics_articles(topic_id):
    """ JSON route - return all articles for specified topic """
    articles = db_session.query(Article).filter_by(topic_id=topic_id)
    return jsonify(articles=[p.serialize for p in articles])


@app.route(api_route + '/topics/<topic_id>/articles/<article_id>',
           methods=['GET'])
def get_topics_article(topic_id, article_id):
    """ JSON route - return specified article for specified topic """
    articles = db_session.query(Article)\
        .filter_by(topic_id=topic_id, id=article_id)
    return jsonify(articles=[p.serialize for p in articles])


@app.route('/articles', methods=['GET'])
def get_articles():
    """ JSON route - return all articles """
    _, articles = base_query(db_session)
    return jsonify(articles=[p.serialize for p in articles])


# Server
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
