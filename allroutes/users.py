from fastapi import APIRouter, Body, HTTPException, Response, status, Request
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
    user = await db.query(User).filter_by(username = username).first()
    if(user):
        return user
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sorry, the user doesnt exist")


@router.post('/signup', status_code=status.HTTP_201_CREATED)
async def signup(user: NewUser, response: Response):
    print('in in in')
    print(user)
    print('next next next')
    if(db.query(User).filter_by(username=user.username).first() or db.query(User).filter_by(email=user.email).first()):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sorry this user already exists")
    try:
        print('*************************************')
        new = User(username = user.username, fullname=user.fullname,email=user.email, password = AuthSetup.genpasswordhash(user.password))
        db.add(new)
        print('===========BEFORE')
        db.execute('commit')
        # db.commit() 
        # why this doesnt work but above does
        # print('entering refresh')
        # db.execute('refresh')
        print('************DONE')
        access_token = AuthSetup.createjwttoken(user.username)
        print('***********************jwted')
        print(access_token)
        # refresh_token = AuthSetup.create_refreshtoken(user.username)
        response.set_cookie(key="access_token",value=f"Bearer {access_token}",secure=True,httponly=True)
        print('--------------------it set')
        return{'message': 'bearing tokens '}
        
        # return {'access token':access_token, 'refresh token': refresh_token}
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Error signing up")  

# replace with token router??
@router.post('/login', status_code=status.HTTP_200_OK)
async def login(request:Request, user: UserLogin, response: Response):
    if(AuthSetup.authenticateuser(username=user.username,password=user.password)):
        access_token = AuthSetup.createjwttoken(user.username)
        # IF RESPONSE SET COOKIE WORKS THEN THE COMMENTED CODES CAN DISAPPEAR
        # PLUS AM I MAINTAING PYDANTIC USERLOGIN OR USING REQUEST
        # refresh_token = AuthSetup.create_refreshtoken(user.username)
        response.set_cookie(key="access_token",value=f"Bearer {access_token}",secure=True,httponly=True)
        return{'message': 'bearing tokens '}
        
        # return {'access token':access_token, 'refresh token': refresh_token}

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")


# @router.put('/updatecredentials')
# async def update(user: UpdateUser, credentials: HTTPAuthorizationCredentials = HTTPBearer()):
#     token = credentials.credentials
#     if(AuthSetup.decodetoken(token)):
#         # MAKE THE NEEDED UPDATE
#         pass