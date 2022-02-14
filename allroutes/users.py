from fastapi import APIRouter, Body, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List,Optional

from ..databasesetup import User, NewUser, UpdateUser, db, Userdantic, UserLogin
from ..authsetup import AuthSetup


router = APIRouter(prefix="api/v1/users")

@router.get('/',response_model=List[Userdantic],status_code=status.HTTP_200_OK)
async def getUsers():
    users = await db.query(User).all()
    return users


@router.get('/{username}',response_model=Userdantic,status_code=status.HTTP_200_OK)
async def getUsers(username: str):
    user = await db.query(User).filter_by(username == username).firs()
    if(user):
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sorry, the user doesnt exist")


@router.post('/signup')
async def signup(user: NewUser):
    # first run to check if username and email already exist.. if either do, the raise exception else create the user
    # newu = User
    # db.add(newu)
    # db.commit()
    # return AuthSetup.createjwttoken(user.username)
    pass


@router.post('/login')
async def login(user: UserLogin):
    if(AuthSetup.authenticateuser):
        return AuthSetup.createjwttoken(user.username)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


@router.put('/updatecredentials')
async def update(user: UpdateUser):
    pass