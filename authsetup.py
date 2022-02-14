from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

from jose import jwt
from numpy import deprecate
from passlib.context import CryptContext

from databasesetup import db, User

class Authsetup():
    
    load_dotenv()

    SECRET = os.getenv("SECRET")
    ALGO = os.getenv("ALGO")

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        encoded_jwt = jwt.encode(to_encode,SECRET,algorithm=ALGO)
        return encoded_jwt