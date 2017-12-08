from flask import Flask, render_template, jsonify, url_for, request, flash,\
                  redirect, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base, Article, Topic, User
from datetime import date

import json
import datetime

DEBUG = True
SECRET_KEY = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'

DATABASE_CONNECTION = 'postgresql://postgres:password@localhost/catalog'
#DATABASE_CONNECTION = 'sqlite:///catalog.db'

GITHUB_CLIENT_ID = '7d4f47c88e6da7febbbb'
GITHUB_CLIENT_SECRET = 'ecb9f99a072a97dafb9cf7d4ae7974bf6e0a99ea'
API_ROUTE = '/api'

engine = create_engine(DATABASE_CONNECTION)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

app = Flask(__name__)

#github = GitHub(app)

api_route = API_ROUTE

def base_query(db_session):
    topics = db_session.query(Topic).all()
    articles = db_session.query(Article).all()

    return topics, articles


def database_seed(db_session, filename='sample-data.json'):
    """ provide initial data """
    topics, articles = base_query(db_session)

    if (len(topics) == 0) or (len(articles) == 0):
        with open(filename, 'rb') as f:
            fixtures = json.load(f)
        seed_topics = fixtures['topic']
        seed_articles = fixtures['article']
        for i in seed_topics:
            topic = Topic(name=i['name'])
            db_session.add(topic)
        for i in seed_articles:
            article = Article(
                title=i['title'],
                url=i['url'],
                date_added=datetime.datetime.strptime(
                    i['data_added'], '%Y-%m-%d').date(),
                description=i['description'],
                topic_id=i['topic_id'])
            db_session.add(article)
        db_session.commit()
    return redirect(url_for('index'))


# Github auth
@app.route('/login')
def login():
    """ login route """
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    """ logout route """
    return redirect(url_for('index'))


def authenticated():
    """ check if user is authenticated or not """
    return False


def can_modify(article):
    """ check if article is added by the session user """
    return False


# HTML Routes
@app.route('/', methods=['GET'])
def index():
    """ index page """
    database_seed(db_session)

    topics, articles = base_query(db_session)
    articles_reversed = articles[::-1]

    return render_template('articles.html', can_modify=can_modify,
                           is_authenticated=authenticated,
                           topics=topics, articles=articles_reversed,
                           active_topic=None)


@app.route('/topics/<int:topic_id>/articles', methods=['GET'])
def view_topics(topic_id):
    """ show filtered articles """
    topics, _articles = base_query(db_session)
    articles = db_session.query(Article).filter_by(topic_id=topic_id)
    articles_reversed = articles[::-1]

    return render_template('articles.html', can_modify=can_modify,
                           is_authenticated=authenticated,
                           topics=topics, articles=articles_reversed,
                           active_topic=topic_id)


@app.route('/articles/new', methods=['GET', 'POST'])
def new_article():
    """ add new article """
    if not authenticated():
        return redirect(url_for('login'))

    if request.method == 'GET':
        topics, _articles = base_query(db_session)

        return render_template('article_form.html',
                               is_authenticated=authenticated,
                               topics=topics, article=None,
                               action='new')
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


@app.route('/articles/<int:article_id>/edit', methods=['GET', 'POST'])
def edit_article(article_id):
    """ edit article """
    article = db_session.query(Article).filter_by(id=article_id).one()

    if not authenticated():
        return redirect(url_for('login'))
    if not can_modify(article):
        return redirect(url_for('index'))

    if request.method == 'GET':
        topics, _articles = base_query(db_session)

        return render_template('article_form.html',
                               is_authenticated=authenticated,
                               topics=topics, article=article,
                               action='edit')
    else:
        form = dict(request.form)

        article.title = form['article_title'][0]
        article.url = form['article_url'][0]
        article.description = form['article_description'][0]
        article.topic_id = form['article_topic_id'][0]

        db_session.add(article)
        db_session.commit()

        return redirect(url_for('index'))


@app.route('/articles/<int:article_id>/delete', methods=['GET', 'POST'])
def delete_article(article_id):
    """ delete article """
    article = db_session.query(Article).filter_by(id=article_id).one()

    if not authenticated():
        return redirect(url_for('login'))
    if not can_modify(article):
        return redirect(url_for('index'))

    if request.method == 'GET':
        return render_template('delete_article.html',
                               is_authenticated=authenticated,
                               article=article)
    else:
        db_session.delete(article)
        db_session.commit()

        return redirect(url_for('index'))


# API JSON routes
@app.route(api_route + '/topics', methods=['GET'])
def get_topics():
    """ JSON route - return all topics """
    topics, _ = base_query(db_session)
    return jsonify([p.serialize for p in topics])


@app.route(api_route + '/topics/<int:topic_id>', methods=['GET'])
def get_topic(topic_id):
    """ JSON route - return all topics """
    topic = db_session.query(Topic).filter_by(id=topic_id).one()
    return jsonify(topic.serialize)


@app.route(api_route + '/topics/<int:topic_id>/articles', methods=['GET'])
def get_topics_articles(topic_id):
    """ JSON route - return all articles for specified topic """
    articles = db_session.query(Article).filter_by(topic_id=topic_id)
    return jsonify([p.serialize for p in articles])


@app.route(api_route + '/topics/<int:topic_id>/articles/<article_id>',
           methods=['GET'])
def get_topics_article(topic_id, article_id):
    """ JSON route - return specified article for specified topic """
    article = db_session.query(Article)\
        .filter_by(topic_id=topic_id, id=article_id).one()
    return jsonify(article.serialize)


@app.route(api_route + '/articles', methods=['GET'])
def get_articles():
    """ JSON route - return all articles """
    _, articles = base_query(db_session)
    return jsonify([p.serialize for p in articles])


@app.route(api_route + '/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    """ JSON route - return specified article """
    article = db_session.query(Article)\
        .filter_by(id=article_id).one()
    return jsonify(article.serialize)

if __name__ == '__main__':
  app.run()