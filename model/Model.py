# standard imports
import os

# third-party imports
from sqlalchemy import Boolean, Column, DateTime, Integer, Text
from sqlalchemy.dialects.sqlite import DATE
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class CollectLog(Base): # {{{
    __tablename__ = 'collect_log'

    _id = Column(Integer, primary_key=True)
    poster = Column(Text)
    url = Column(Text)
    html = Column(Text)
    collect_time = Column(DateTime)
    checked = Column(Boolean)
    checked_time = Column(DateTime)
    published = Column(Boolean)
    published_time = Column(DateTime)
# }}}

class ParsedNews(Base): #{{{
    __tablename__ = 'parsed_news'

    _id = Column(Integer, primary_key=True)
    url = Column(Text, unique=True)
    title = Column(Text)
    article = Column(Text)
    keywords = Column(Text)
    date = Column(DateTime)
# }}}

class User(Base): #{{{
    __tablename__ = 'user'

    _id = Column(Integer, primary_key=True)
    user_id = Column(Text, unique=True)
    user_name = Column(Text)
# }}}
