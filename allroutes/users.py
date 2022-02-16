from fastapi import APIRouter, Body, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List,Optional

from databasesetup import User, NewUser, UpdateUser, db, Userdantic, UserLogin
from authsetup import AuthSetup
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


router = APIRouter(prefix="/api/v1/users")

@router.get('/',response_model=List[Userdantic],status_code=status.HTTP_200_OK)
async def getUsers():
    users = await db.query(User).all()
    return users


@router.get('/{username}',response_model=Userdantic,status_code=status.HTTP_200_OK)
async def getUsers(username: str):
    user = await db.query(User).filter_by(username == username).first()
    if(user):
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sorry, the user doesnt exist")


@router.post('/signup')
async def signup(user: NewUser):
    if(db.query(User.filterby(User.username==user.username)).first() or db.query(User.filterby(User.email==user.email)).first()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sorry this user already exists")
    try:
        new = User(username = user.username, password = AuthSetup.genpasswordhash(user.password))
        db.add(new)
        db.commit()
        access_token = AuthSetup.createjwttoken(user.username)
        refresh_token = AuthSetup.create_refreshtoken(user.username)
        return {'access token':access_token, 'refresh token': refresh_token}
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error signing up")  


@router.post('/login', status_code=status.HTTP_200_OK)
async def login(user: UserLogin):
    if(AuthSetup.authenticateuser(username=user.username,password=user.password)):
        access_token = AuthSetup.createjwttoken(user.username)
        refresh_token = AuthSetup.create_refreshtoken(user.username)
        return {'access token':access_token, 'refresh token': refresh_token}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


# @router.put('/updatecredentials')
# async def update(user: UpdateUser, credentials: HTTPAuthorizationCredentials = HTTPBearer()):
#     token = credentials.credentials
#     if(AuthSetup.decodetoken(token)):
#         # MAKE THE NEEDED UPDATE
#         pass