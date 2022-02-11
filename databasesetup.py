from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey
from pydantic import BaseModel

from datetime import datetime
import os

Base = declarative_base()
postgres = os.getenv("POSTGRES")
engine = create_engine(postgres, echo = False)
session = sessionmaker(bind=engine)

class User(Base):
    __tablename__="users"
    id = Column(Integer(), primary_key=True)
    fullname = Column(String(24), nullable=False)
    username = Column(String(24), nullable=False, unique=True)
    email = Column(String(36),nullable=False,unique=True)
    password = Column(String(100), nullable=False) 
    avatar = Column(String(35),nullable=False, default = 'def_avatar.png') 
    timestamp = Column(DateTime(), default=datetime.utcnow)  
    posts = relationship('Post', backref="artist", cascade="all, delete")
    comments = relationship('Comment', backref="artist", cascade="all, delete",)
    # r2p = relationship('Ireply', backref="artist", cascade="all, delete",)
    # likes = Column(Integer())
    
    def __repr__(self):
        return f"User({self.username}, {self.email})"


class  Post(Base):
    __tablename__ = 'posts'
    id=Column(Integer(),primary_key=True)
    content = Column(String(1000), nullable=False)
    timestamp = Column(DateTime(),default=datetime.utcnow)
    user_id = Column(Integer(), ForeignKey('users.id'), nullable=False )
    comments = relationship('Comment',backref="post",cascade="all, delete")
    likes = Column(Integer())
    # r2p = relationship('Ireply',backref="post",cascade="all, delete")

    def __repr__(self):
        return f"Posts({self.content},{self.timestamp},{self.comments})"


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer(), primary_key=True)
    comment = Column(String(150))
    timestamp = Column(DateTime(),default=datetime.utcnow)
    comment_reply_id = Column(Integer(), ForeignKey('comments.id'), nullable=True,)
    reply_to_reply_id = Column(Integer(),  nullable=True,)
    post_id = Column(Integer(), ForeignKey('posts.id'),nullable=False)
    user_id = Column(Integer(), ForeignKey('users.id'),nullable=False)
    replies = relationship('Comment', backref=backref('reply_to_comment', remote_side ='Comment.id'))
    # rep2rep = relationship('Ireply',backref="rp2rp",cascade="all, delete")

    def __repr__(self):
        return f"Comments({self.comment}, replies({self.replies}))"


class Createdb():
    def createdb():
        Base.metadata.create_all(engine)