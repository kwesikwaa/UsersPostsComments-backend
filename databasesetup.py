import email
from typing import Optional
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey,  Boolean
from pydantic import BaseModel, Field
import uuid

from datetime import datetime
import os

Base = declarative_base()
postgres = os.getenv("POSTGRES")
engine = create_engine(postgres, echo = False)
db = sessionmaker(bind=engine)

class User(Base):
    __tablename__="users"
    id = Column(Integer(), primary_key=True)
    fullname = Column(String(24), nullable=False)
    username = Column(String(24), nullable=False, unique=True)
    email = Column(String(36),nullable=False,unique=True)
    password = Column(String(100), nullable=False) 
    avatar = Column(String(35),nullable=False, default = os.getenv("DEFAULT_AVATAR")) 
    datecreated = Column(DateTime(), default=datetime.utcnow)  
    isblackstarartist = Column(Boolean(),nullable=False, default=False)
    posts = relationship('Post', backref="artist", cascade="all, delete")
    comments = relationship('Comment', backref="artist", cascade="all, delete",)
    # r2p = relationship('Ireply', backref="artist", cascade="all, delete",)
    # likes = Column(Integer())
    
    def __repr__(self):
        return f"User({self.username}, {self.email})"

class NewUser(BaseModel):
    id: str = Field(default_factory=uuid.uuid4)
    fullname: str = Field(...)
    username: str = Field(...)
    email: email = Field(...)
    password: str = Field(...)
    avatar: Optional[str]


class UpdateUser(BaseModel):
    fullname: Optional[str]
    username: Optional[str]
    avatar: Optional[str]


class  Post(Base):
    __tablename__ = 'posts'
    id=Column(Integer(),primary_key=True)
    description = Column(String(1000), nullable=False)
    datecreated = Column(DateTime(),default=datetime.utcnow)
    user_id = Column(Integer(), ForeignKey('users.id'), nullable=False )
    comments = relationship('Comment',backref="post",cascade="all, delete")
    likes = Column(Integer())
    # r2p = relationship('Ireply',backref="post",cascade="all, delete")

    def __repr__(self):
        return f"Posts({self.description},{self.datecreated},{self.comments})"


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer(), primary_key=True)
    comment = Column(String(150))
    datecreated = Column(DateTime(),default=datetime.utcnow)
    post_id = Column(Integer(), ForeignKey('posts.id'),nullable=False)
    user_id = Column(Integer(), ForeignKey('users.id'),nullable=False)
    comment_reply_id = Column(Integer(), ForeignKey('comments.id'), nullable=True,)
    replies = relationship('Comment', backref=backref('reply_to_comment', remote_side ='Comment.id'))



    # reply_to_reply_id = Column(Integer(),  nullable=True,)
    
    

    def __repr__(self):
        return f"Comments({self.comment}, replies({self.replies}))"


class Createdb():
    def createdb():
        Base.metadata.create_all(engine)