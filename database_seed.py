from models import Topic, Article
from flask import Flask, flash, session, redirect, url_for

import json
import datetime


def base_query(session):
    topics = session.query(Topic).all()
    articles = session.query(Article).all()

    return topics, articles


def database_seed(session, filename='sample-data.json'):
    """ provide initial data """
    topics, articles = base_query(session)

    if (len(topics) == 0) or (len(articles) == 0):
        with open(filename, 'rb') as f:
            fixtures = json.load(f)
        seed_topics = fixtures['topic']
        seed_articles = fixtures['article']
        for i in seed_topics:
            topic = Topic(name=i['name'])
            session.add(topic)
        for i in seed_articles:
            article = Article(
                title=i['title'],
                url=i['url'],
                data_added=datetime.datetime.strptime(
                    i['data_added'], '%Y-%m-%d').date(),
                description=i['description'],
                topic_id=i['topic_id'])
            session.add(article)
        try:
            session.commit()
            flash('Database seeded with fixture data.', 'warning')
        except Exception as e:
            flash('Something imploded. {}'.format(e), 'danger')
    return redirect(url_for('index'))
