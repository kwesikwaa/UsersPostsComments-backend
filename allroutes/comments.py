from os import stat
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from databasesetup import Commentdantic,NewComment, Postdantic, User,db,Post, Comment, UserDisplay, UpdateComment
from authsetup import AuthSetup

router = APIRouter(prefix="/api/v1/comments")

@router.get('/', response_model=List[Commentdantic], status_code=200)
async def comments(post: Postdantic):
    post = db.query(Post).filter_by(id=post.id).first()
    return await db.query(Comment).order_by(Comment.datecreated.desc()).all()
# PRETTY UNNECESSARY COS POSTS WILL POPULATE THEIROWN 


@router.post('/newcomment', status_code=status.HTTP_201_CREATED, response_model= NewComment)
async def newcomment(newcomment: NewComment, currentuser: UserDisplay= Depends(AuthSetup.getcurrentuser)):
    post = await db.query(Post).filter_by(id = newcomment.post_id).first()

    if(newcomment.isReply):
        parent = await db.query(Comment).filter_by(id = newcomment.parentcomment_id).first()
        new = await Comment(comment = newcomment.comment,post=post, artist = currentuser,isReply = newcomment.isReply, parentcomment = parent)
        db.add(new)
        db.commit()
    else:
        new = await Comment(comment = newcomment.comment,post=post, artist = currentuser)
        db.add(new)
        db.commit()
    # return HTTPException(status_code=status.HTTP_201_CREATED,detail="Comment created succcessfully")


@router.put('/updatecomment/{id}', status_code=status.HTTP_202_ACCEPTED)
async def updatecomment(id: str, updatedcomment: UpdateComment, currentuser: UserDisplay= Depends(AuthSetup.getcurrentuser)):
    commenttodelete = db.query(Comment).filter_by(id=id).first()
    commenttodelete.comment = updatecomment
    db.commit()
    

@router.delete('/deletecomment/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def deletecomment(id:str ,currentuser: UserDisplay= Depends(AuthSetup.getcurrentuser)):
    commenttodelete = db.query(Comment).filter_by(id=id).first()
    db.delete(commenttodelete)
    db.commit()