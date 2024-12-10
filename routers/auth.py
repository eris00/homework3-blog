
from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from crud.user import get_user_by_email, verify_password, create_user
from schemas.user import Token, User, UserCreate
from database import get_db
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from database import get_db

from utils.auth import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

router = APIRouter(tags=["auth"])

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = get_user_by_email(db, email=form_data.username)
    is_pwd_verify = verify_password(form_data.password, user.password)
    if not user or not is_pwd_verify:
        raise HTTPException(
            status_code=404,
            detail = "Incorrect username or passsword"
        )
    access_token = create_access_token(data={"sub": user.email}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=User)
def register(db: Annotated[Session, Depends(get_db)], user_data: UserCreate):
    existing_user = get_user_by_email(db, email=user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists."
        )
    return create_user(db, user_data)
    
