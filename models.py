from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class Topic(Base):
    __tablename__ = 'topic'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)


class Article(Base):
    __tablename__ = 'article'

    id = Column(Integer, primary_key=True)
    title = Column(String(80), nullable=False)
    url = Column(String(255))
    data_added = Column(Date)
    description = Column(String(2000))
    topic_id = Column(Integer, ForeignKey('topic.id'))
    topic = relationship(Topic)

if __name__ == '__main__':
    engine = create_engine('sqlite:///catalog.db')
    Base.metadata.create_all(engine)