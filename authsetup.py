from datetime import datetime, timedelta
import os
import time
from dotenv import load_dotenv

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext

from databasesetup import db, User

load_dotenv()

SECRET_KEY = os.getenv("SECRET")
ALGO = os.getenv("ALGO")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthSetup():

    def genpasswordhash(password: str):
        return pwd_context.hash(password)
        

    def authenticateuser(username:str, password: str):
        try:
            user = db.query(User).filter_by(username = username).first()
            pwd_check = pwd_context.verify(password, user['password'])
            return pwd_check
        except:
            return False


    def createjwttoken(data: dict, expireduration: timedelta):
        to_encode = data
        expiry = datetime.now() + expireduration
        to_encode.update({"exp": expiry})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGO)
        return {"access token" : encoded_jwt, "token_type" : "bearer"}


    def decodetoken(token: str):
        try:
            decodeam = jwt.decode(token, SECRET_KEY, algorithm=ALGO)
            if(decodeam['exp'] >= time.time()):
                return decodeam
        except:
            return HTTPException()