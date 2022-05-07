
from typing import Optional, List

# from sqlalchemy.dialects.postgresql import UUID
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, backref, declarative_base
from sqlalchemy import Column, Integer, String, DateTime, create_engine, ForeignKey,  Boolean, null, ARRAY
from pydantic import BaseModel, Field
import uuid

from datetime import datetime
from decouple import config

Base = declarative_base()
postgres = config("XX")
engine = create_engine(postgres, echo = True)
Session = sessionmaker(bind=engine)
db = Session()

# USE THIS TO GENERATE UUID AND FEED INTO TABLE/SCHEMA InSTEAD OF sqlachemy's postgres uuid dialect
def genuuidtostr():
    return uuid.uuid4().hex

class User(Base):
    __tablename__="users"
    id = Column(String(), primary_key=True, default=genuuidtostr)
    fullname = Column(String(24), nullable=False)
    username = Column(String(24), nullable=False, unique=True)
    email = Column(String(36),nullable=False,unique=True)
    password = Column(String(100), nullable=False) 
    phonenumber = Column(Integer(),nullable=False)
    avatar = Column(String(35),nullable=True, default = config("DEFAULT_AVATAR")) 
    isstudio = Column(Boolean(), nullable=False)
    coverphoto = Column(String(35), nullable=True)
    datecreated = Column(DateTime(), default=datetime.utcnow)  
    isblackstarartist = Column(Boolean(),nullable=True, default=False)
    following = Column(ARRAY(String),nullable=True)
    followers = Column(ARRAY(String),nullable=True)
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
    phonenumber: int
    isstudio: bool
    coverphoto: Optional[str]


    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    username: str = Field(...)
    password: str = Field(...) 


class UserDisplay(BaseModel):
    id: str
    username: str
    fullname: str
    avatar: str
    datecreated: str
    isblackstarartist: bool


class UpdateUser(BaseModel):
    fullname: Optional[str]
    username: Optional[str]
    isstudio: Optional[bool]
    coverphoto: Optional[str]
    avatar: Optional[str]

    class Config:
        orm_mode = True


class  Post(Base):
    __tablename__ = 'posts'
    id = Column(String(), primary_key=True, default=genuuidtostr)
    title: Column(String(100), nullable=False)
    description = Column(String(1000), nullable=False)
    datecreated = Column(DateTime(),default=datetime.utcnow)
    user_id = Column(String(), ForeignKey('users.id'), nullable=False )
    thumbnail = Column(String())
    tags = Column(ARRAY(String),nullable=True)
    media = Column(ARRAY(String),nullable=False)
    softwaresused = Column(ARRAY(String),nullable=False)
    likes = Column(Integer())
    comments = relationship('Comment',backref="post",cascade="all, delete")
    # r2p = relationship('Ireply',backref="post",cascade="all, delete")

    def __repr__(self):
        return f"Posts({self.description},{self.thumbnail},{self.datecreated},{self.comments})"


class NewPost(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    thumbnail: str
    tags: List[str]
    media: List[str]
    softwaresused: List[str]
    # user_id:UUID

    class Config:
        orm_mode=True


class UpdatePost(BaseModel):
    title: Optional[str]
    description: Optional[str]
    thumbnail: str
    # tags: Optional[List[str]]
    # media: Optional[List[str]]
    # softwaresused: Optional[List[str]] 

    class Config:
        orm_mode=True


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(String(), primary_key=True, default=genuuidtostr)
    comment = Column(String(150))
    datecreated = Column(DateTime(),default=datetime.utcnow)
    post_id = Column(String(), ForeignKey('posts.id'),nullable=False)
    user_id = Column(String(), ForeignKey('users.id'),nullable=False)
    isReply = Column(Boolean(),default=False,nullable=True)
    # origcommentid = Column(String())    
    # replyid is which comment youre replying to
    # PROBABLY WORK ON A USER MENTIONS LATER
    parentcomment_id = Column(String(), ForeignKey('comments.id'), nullable=True,)
    replies = relationship('Comment', backref=backref('parentcomment', remote_side ='Comment.id'))

    def __repr__(self):
        return f"Comments({self.comment}, replies({self.replies}))"


class Commentdantic(BaseModel):
    id: str
    comment: str
    datecreated: datetime
    replies: List[str]
    post_id: str
    user_id: str
    parentcomment_id: str

    class Config:
        orm_mode = True


class NewComment(BaseModel):
    comment : str = Field(...)
    post_id: str = Field(...)
    user_id: str = Field(...)
    isReply: Optional[bool] 
    parentcomment_id: Optional[str]

    class Config:
        orm_mode = True

class UpdateComment(BaseModel):
    comment: Optional[str]=None
    

class Postdantic(BaseModel):
    id: str
    title: str
    description: str
    datecreated: datetime
    likes: int
    comments: List[Commentdantic]
    user_id: str

    class Config:
        orm_mode=True


class Userdantic(BaseModel):
    id: str
    fullname: str 
    username: str
    email: str
    avatar: str
    datecreated: datetime
    isblackstarartist: bool
    posts: List[Postdantic]
    comments: List[Commentdantic]
    followers: List[str]
    following: List[str]
    isstudio: bool
    coverphoto: str

    class Config:
        orm_mode = True

# Call to create database
class Createdb():
    def createdb():
        Base.metadata.create_all(engine)

def get_db():
    dbb = Session()
    try:
        yield dbb
    finally:
        dbb.close()