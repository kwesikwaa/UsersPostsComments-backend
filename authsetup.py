from datetime import datetime, timedelta
from operator import sub
import os

import time
from dotenv import load_dotenv

# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
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


    def createjwttoken(data: str, expireduration: timedelta):
        payload={
            "sub": data,
            "exp": datetime.now() + expireduration,
            "iat": datetime.now(),
            "scope": "access_token",
        }
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGO)
        return encoded_jwt


    def decodetoken(token: str):
        try:
            decodeam = jwt.decode(token, SECRET_KEY, algorithm=ALGO)
            if(decodeam['scope'] == "access_token"):
                return decodeam['sub']
            raise HTTPException(status_code=401, detail='Invalid scope')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Token has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code = 401, detail='Invalid token')

    
    def create_refreshtoken(data: str, expireduration: timedelta):
        payload={
            "sub": data,
            "exp": datetime.now() + expireduration,
            "iat": datetime.now(),
            "scope": "refresh_token",
        }
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGO)
        return encoded_jwt


    def decode_refreshtoken(self, token:str):
        try:
            decodeam = jwt.decode(token, SECRET_KEY, algorithm=ALGO)
            if(decodeam['scope'] == 'refresh_token'):
                data = decodeam['sub']
                new_token = self.createjwttoken(data)
                return new_token
            raise HTTPException(status_code=401, detail='Invalid scope for token')
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='Refresh Token has expired')
        except jwt.InvalidTokenError:
            raise HTTPException(status_code = 401, detail='Invalid Refresh Token')
