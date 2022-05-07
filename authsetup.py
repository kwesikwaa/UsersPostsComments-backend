from base64 import decode
from datetime import datetime, timedelta
from decouple import config
from fastapi import Depends, HTTPException, APIRouter, status, Request, Form,Response
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
import jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from databasesetup import db, User, UserDisplay
from typing import Optional

SECRET_KEY = config("SECRET")
ALGO = config("ALGO")

router = APIRouter()

class Token(BaseModel):
    access_token:str
    token_type: str


class TokenData(Token):
    username: Optional[str] = None

class Logininputs(BaseModel):
    username: str
    password: str

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oathscheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post('/login', status_code=200, )
async def tokentins(user: Logininputs, response: Response):
    print('********')
    print(user.username)
    print(user.password)
    usa = await AuthSetup.authenticateuser(user.username,user.password)
    
    # authorization: str = request.headers.get("Authorization")
    # scheme, param = get_authorization_scheme_param("authorization")
    # if not authorization or scheme.lower() != "bearer"

    if not usa:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = AuthSetup.createjwttoken(data=user.username, expireduration=timedelta(days=6) )
    response.set_cookie(key="access_token",value=f"Bearer {token}",secure=True,httponly=True)
    
    return token


class AuthSetup():

    def genpasswordhash(password: str):
        return pwd_context.hash(password)
        

    async def authenticateuser(username:str, password: str):
            user = db.query(User).filter_by(username = username).first()
            if not user:
                return False
            if not pwd_context.verify(password, user.password):
                return False
            return user


    def createjwttoken(data: str, expireduration: Optional[timedelta]=timedelta(days=6)):
        payload={
            "sub": data,
            "exp": datetime.now() + expireduration,
            "iat": datetime.now(),
            "scope": "access_token",
        }
        encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGO)
        return encoded_jwt


    def decodetoken(token: str):
        decodeam = jwt.decode(token, SECRET_KEY, algorithm=ALGO)
        if(decodeam['scope'] == "access_token"):
            return decodeam['sub']
        return None

    async def getcurrentuser(self,token:str = Depends(oathscheme)):
        credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            username = self.decodetoken(token)
            if username is None:
                raise credentials_exception
            token_data = TokenData(username=username)
            
        except jwt.PyJWTError:
            raise credentials_exception
        # user = get_user(fake_users_db, username=token_data.username)  DELETE WHEN DONE CHECKING
        user = await db.query(User).filter_by(username = token_data.username).first()
        # THE ABOVE DOESNT MAKE SENSE CONSIDERING A DECODE GENERATES SAME USERNME
        if user is None:
            raise credentials_exception
        return user


        
    
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


# ANOTHER APPROACH
class paulbearer(HTTPBearer):
    def __init__(self, auto_Error: bool=True):
        super(paulbearer, self).__init__(auto_error=auto_Error)


    async def __call__(self, request:Request):
        credentials: HTTPAuthorizationCredentials = await super(paulbearer, self).__call__(request)
        if credentials:
            if not credentials.schema == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid or Expired Token")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid or Expired Token")

    def verify_jwt(self, jwtoken: str):
        isTokenValid: bool = False
        payload = AuthSetup.decodetoken(jwtoken)
        if payload:
            isTokenValid = True
        return isTokenValid

