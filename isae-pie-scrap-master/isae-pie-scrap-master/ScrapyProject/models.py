from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import ScrapyProject.settings


DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """

    return create_engine(URL(**ScrapyProject.settings.DATABASE))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class NewsArticles(DeclarativeBase):
    """Sqlalchemy newsarticles model"""
    __tablename__ = "db_api_newsarticle"
    
    tstamp = Column('tstamp', DateTime, nullable=False) 
    url = Column('url', String, primary_key=True)
    title = Column('title', String, nullable=False)
    brief = Column('brief', String, nullable=True)
    body = Column('body', String, nullable=True)
    date = Column('date', DateTime, nullable=False)
    source = Column('source', String, nullable=False, default='UNDEFINED')
    company = Column('company', String, nullable=False, default='UNDEFINED')
    tag = Column('tag', String, nullable=True)
