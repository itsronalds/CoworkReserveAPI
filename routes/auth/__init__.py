from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.deps import get_db

import models.user as user_model
import schemas.user as user_schema
import utils.bcrypt as bcrypt_utils
import utils.logger as logger_utils
import utils.jwt as jwt_utils


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post('/login')
def login(user: user_schema.UserLogin, db: Session = Depends(get_db)):
    try:
        user_by_email = db.query(user_model.User).with_entities(user_model.User.email,
                                                                user_model.User.password).filter(user_model.User.email == user.email).first()
        if not user_by_email:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={'message': 'User not found'}
            )

        if not bcrypt_utils.verify_password(user.password, user_by_email.password):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={'message': 'Wrong password'}
            )

        token = jwt_utils.encode_jwt({'email': user_by_email.email})

        return {'token': token}
    except Exception as e:
        logger_utils.logger.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={'message': 'Internal server error'}
        )


@router.post('/register')
def register(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    try:
        user_by_email = db.query(user_model.User).with_entities(
            user_model.User.email).filter(user_model.User.email == user.email).first()

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
    except Exception as e:
        logger_utils.logger.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={'message': 'Internal server error'}
        )
