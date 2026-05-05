from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from Models.table import Users
from fastapi.security import OAuth2PasswordRequestForm
from Auth.auth import hash_password, verify_password, create_access_token
from Models.Auth_schemas import UserCreate, Token
from Database.database import get_db


router = APIRouter(prefix="/Auth",tags=["Auth"])

@router.post("/register")
def register(user:UserCreate,db:Session=Depends(get_db)):
    existing=db.query(Users).filter(Users.username==user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_user=Users(
        username=user.username,
        hashed_Password=hash_password(user.password),
        roles=user.roles
    )
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    db_user=db.query(Users).filter(Users.username==form_data.username).first()
    if not db_user or not verify_password(form_data.password,db_user.hashed_Password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token=create_access_token({"sub":db_user.username,"role": db_user.roles,"user_id": db_user.id})
    return {"access_token":token,"token_type": "bearer"}