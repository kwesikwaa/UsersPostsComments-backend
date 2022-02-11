# import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from allroutes.posts import router as postsrouter

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]

)


app.include_router(postsrouter, prefix="/posts")

