from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from databasesetup import Commentdantic,NewComment, User,db,Post, Comment
from authsetup import AuthSetup

router = APIRouter(prefix="/api/v1/comments")

@router.get('/')
async def comments():
    return {"Asay": "This be comments route"}

@router.post('/newcomment')
async def newcomment(newcomment: NewComment):
    try:
        user = await db.query(User).filter_by(id == newcomment.user_id).first()
        post = await db.query(Post).filter_by(id == newcomment.post_id).first()
        if(newcomment.isReply):
            parent = await db.query(Comment).filter_by(id == newcomment.parentcomment_id).first()
            new = await Comment(comment = newcomment.comment,post=post, artist = user,isReply = newcomment.isReply, parentcomment = parent)
            db.add(new)
            db.commit()
        else:
            new = await Comment(comment = newcomment.comment,post=post, artist = user)
            db.add(new)
            db.commit()
        return HTTPException(status_code=status.HTTP_201_CREATED,detail="Comment created succcessfully")
    except:
        return{'error':'what could this be lol'}


@router.put('/updatecomment/:id')
async def updatecomment():
    pass

@router.delete()
async def deletecomment():
    pass