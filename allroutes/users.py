from fastapi import APIRouter, Body, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from ..databasesetup import User, NewUser, UpdateUser, db
from typing import List,Optional

router = APIRouter(prefix="api/v1/users")

@router.get('/',response_model=List[NewUser],status_code=status.HTTP_200_OK)
async def getUsers():
    users = await db.query(User).all()
    return users
