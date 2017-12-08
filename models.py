from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

#DATABASE_CONNECTION = 'postgresql://catalog:password@localhost/catalog'
DATABASE_CONNECTION = 'sqlite:///catalog.db'

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    access_token = Column(String(200), nullable=False)
    github_username = Column(String(200), nullable=False)

    def __init__(self, github_username):
        self.github_username = github_username


class Topic(Base):
    __tablename__ = 'topic'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)

    @property
    def serialize(self):
        """ JSON serializer method """
        return {
            'id': self.id,
            'name': self.name,
        }


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    url = Column(String(255), nullable=False)
    date_added = Column(Date, nullable=False)
    description = Column(String(2000), nullable=False)
    topic_id = Column(Integer, ForeignKey('topic.id'), nullable=False)
    topic = relationship(Topic)
    adder_id = Column(Integer, ForeignKey('user.id'))
    adder = relationship(User)

    @property
    def serialize(self):
        """ JSON serializer method """
        return {
            'id': self.id,
            'title': self.title,
            'url': self.url,
            'date_added': self.date_added,
            'description': self.description,
            'topic_id': self.topic_id,
        }

engine = create_engine(DATABASE_CONNECTION)
Base.metadata.create_all(engine)
