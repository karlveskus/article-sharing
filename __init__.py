from flask import Flask, render_template, jsonify, url_for, request, flash,\
                  redirect, session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models import Base, Article, Topic, User


DEBUG = True
SECRET_KEY = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'

DATABASE_CONNECTION = 'postgresql://catalog:password@localhost/catalog'
#DATABASE_CONNECTION = 'sqlite:///catalog.db'

GITHUB_CLIENT_ID = '7d4f47c88e6da7febbbb'
GITHUB_CLIENT_SECRET = 'ecb9f99a072a97dafb9cf7d4ae7974bf6e0a99ea'
API_ROUTE = '/api'



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



engine = create_engine(DATABASE_CONNECTION)
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
db_session = DBSession()

app = Flask(__name__)

#github = GitHub(app)

api_route = API_ROUTE


@app.route('/')
def hello_world():
  return 'Hello from Flask!'

if __name__ == '__main__':
  app.run()