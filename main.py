# import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from allroutes.posts import router as postsrouter
from allroutes.comments import router as commentsrouter
from allroutes.users import router as usersrouter


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)


app.include_router(postsrouter)
app.include_router(commentsrouter)
app.include_router(usersrouter)

@app.get('/')
def startpoint():
    return {'message': 'Asay! akwaaba!'}
