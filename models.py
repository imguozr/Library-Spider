from sqlalchemy import Column, String, Integer, ForeignKey, Text, Float
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Book(Base):
    __tablename__ = 'book'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    author = Column(Integer, ForeignKey('author.id'))
    publisher = Column(Integer, ForeignKey('publisher.id'))
    isbn = Column(String(16), unique=True, index=True)
    price = Column(Float)
    subject = Column(String(64), index=True)
    index_code = Column(String(64))
    description = Column(Text)
    douban_description = Column(Text)


class Author(Base):
    __tablename__ = 'author'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    description = Column(Text)


class Publisher(Base):
    __tablename__ = 'publisher'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), index=True)
    location = Column(String(64))
