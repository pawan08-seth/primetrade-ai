from pydantic import BaseModel,EmailStr

class UserCreate(BaseModel):
    username: str
    password: str
    roles:list

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"