from fastapi import FastAPI
from api import api
from Auth import Auth_routes

app=FastAPI()

app.include_router(Auth_routes.router)
app.include_router(api.router) 

