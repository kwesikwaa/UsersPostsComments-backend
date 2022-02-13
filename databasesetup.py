import email
from typing import Optional, List
from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey,  Boolean, null
from pydantic import BaseModel, Field
import uuid

from datetime import datetime
import os
from dotenv import load_dotenv

Base = declarative_base()
load_dotenv()
postgres = os.getenv("XX")
engine = create_engine(postgres, echo = True)
Session = sessionmaker(bind=engine)
db = Session(bind=engine)

class User(Base):
    __tablename__="users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
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
    fullname:str
    username: str
    password: str
    email: str
    avatar: Optional[str]

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    fullname: Optional[str]
    username: Optional[str]
    email: Optional[str]
    avatar: Optional[str]

    class Config:
        orm_mode = True


class  Post(Base):
    __tablename__ = 'posts'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title: Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    datecreated = Column(DateTime(),default=datetime.utcnow)
    user_id = Column(UUID(), ForeignKey('users.id'), nullable=False )
    comments = relationship('Comment',backref="post",cascade="all, delete")
    likes = Column(Integer())
    # r2p = relationship('Ireply',backref="post",cascade="all, delete")

    def __repr__(self):
        return f"Posts({self.description},{self.datecreated},{self.comments})"


class NewPost(BaseModel):
    title: str
    description: str
    user_id:UUID

    class Config:
        orm_mode=True


class UpdatePost(BaseModel):
    title: Optional[str]
    description: Optional[str]

    class Config:
        orm_mode=True


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    comment = Column(String(150))
    datecreated = Column(DateTime(),default=datetime.utcnow)
    post_id = Column(UUID(), ForeignKey('posts.id'),nullable=False)
    user_id = Column(UUID(), ForeignKey('users.id'),nullable=False)
    comment_reply_id = Column(UUID(), ForeignKey('comments.id'), nullable=True,)
    replies = relationship('Comment', backref=backref('reply_to_comment', remote_side ='Comment.id'))

    # reply_to_reply_id = Column(Integer(),  nullable=True,)
    def __repr__(self):
        return f"Comments({self.comment}, replies({self.replies}))"


class Commentdantic(BaseModel):
    id: UUID
    comment: str
    datecreated: DateTime
    replies: List[str]
    post_id: UUID
    user_id: UUID
    comment_reply_id= UUID

    class Config:
        orm_mode = True


class Postdantic(BaseModel):
    id: UUID
    title: str
    description: str
    datecreated: DateTime
    likes: int
    comments: List[Commentdantic]
    user_id: UUID

    class Config:
        orm_mode=True


class Userdantic(BaseModel):
    id: UUID
    fullname: str 
    username: str
    email: str
    avatar: str
    datecreated: DateTime
    isblackstarartist: bool
    posts: List[Postdantic]
    # comments: List[]

    class Config:
        orm_mode = True

# Call to create database
class Createdb():
    def createdb():
        Base.metadata.create_all(engine)