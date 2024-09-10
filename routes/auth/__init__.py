from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.deps import get_db

import models.user as user_model
import schemas.user as user_schema
import utils.bcrypt as bcrypt_utils


router = APIRouter(prefix='/auth', tags=['auth'])


@router.get('/login')
def login():
    return {'message': 'Login'}


@router.post('/register')
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    user_by_email = db.query(user_model.User).filter(user_model.User.email == user.email).first()

    if user_by_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'message': 'Email already registered'}
        )

    # hash password using bcrypt
    hashed_password = bcrypt_utils.hash_password(user.password)

    new_user = user_model.User(
        name=user.name,
        email=user.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {'message': 'User registered'}
