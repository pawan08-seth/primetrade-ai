from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer,OAuth2PasswordBearer,HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import JWTError
from Database.database import get_db
from Auth.auth import decode_token
from Models.table import Users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login") 
http_bearer = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer), 
    db: Session = Depends(get_db) ):
    token = credentials.credentials
    
    auth_error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_token(token)
        username = payload.get("sub")
        if not username:
            raise auth_error
    except JWTError:
        raise auth_error

    user = db.query(Users).filter(Users.username == username).first()

    if not user:
        raise auth_error

    return user


def require_role(required_roles: list):
    def role_checker(user: Users = Depends(get_current_user)):
        if not any(role in user.roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions")
        return user
    return role_checker
