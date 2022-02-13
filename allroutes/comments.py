from fastapi import APIRouter, Body, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


router = APIRouter(prefix="api/v1/comments")