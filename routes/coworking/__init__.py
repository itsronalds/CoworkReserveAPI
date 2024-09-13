from fastapi import APIRouter, Path, Depends, HTTPException, status

# database
from sqlalchemy.orm import Session
from database.deps import get_db

# models
import models.coworking as coworking_model

# schemas
import schemas.coworking as coworking_schema

# utils
import utils.logger as logger_utils
import utils.jwt as jwt_utils


router = APIRouter(prefix='/coworking', tags=['coworking'])


@router.get('/')
def get_coworkings(name: str = '', price_by_hour: float = 0.0, is_available: int = 1, db: Session = Depends(get_db), token_payload: dict = Depends(jwt_utils.check_jwt)):
    try:
        if token_payload['role'] != 'admin':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'message': 'Unauthorized'}
            )
    except Exception as e:
        logger_utils.logger.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'message': 'Unauthorized'}
        )

    try:
        query = db.query(coworking_model.Coworking).filter(coworking_model.Coworking.name.like(
            f'{name}%')).where(coworking_model.Coworking.is_available == is_available)

        if price_by_hour != 0.0:
            query.where(coworking_model.Coworking.price_by_hour == price_by_hour)

        coworkings = query.all()
    except Exception as e:
        logger_utils.logger.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={'message': 'Server internal error'}
        )

    return coworkings


@router.post('/', dependencies=[Depends(jwt_utils.check_jwt)])
def create_coworking(coworking: coworking_schema.CoworkingBase, db: Session = Depends(get_db), token_payload: dict = Depends(jwt_utils.check_jwt)):
    try:
        if token_payload['role'] != 'admin':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'message': 'Unauthorized'}
            )
    except Exception as e:
        logger_utils.logger.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'message': 'Unauthorized'}
        )

    try:
        coworking_by_name = db.query(coworking_model.Coworking).with_entities(
            coworking_model.Coworking.name).filter(coworking_model.Coworking.name == coworking.name).first()
    except Exception as e:
        logger_utils.logger.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={'message': 'Server internal error'}
        )

    if coworking_by_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={'message': 'Coworking name already exist'}
        )

    new_coworking = coworking_model.Coworking(
        name=coworking.name,
        ubication=coworking.ubication,
        price_by_hour=coworking.price_by_hour,
        capacity=coworking.capacity,
        is_available=coworking.is_available
    )

    try:
        db.add(new_coworking)
        db.commit()
        db.refresh(new_coworking)
    except Exception as e:
        logger_utils.logger.debug(str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={'message': 'Server internal error'}
        )

    return {
        'message': 'Coworking created'
    }


@router.put('/{id}')
def update_coworking(coworking: coworking_schema.CoworkingBase, db: Session = Depends(get_db), token_payload: dict = Depends(jwt_utils.check_jwt), id: int = Path()):
    try:
        if token_payload['role'] != 'admin':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'message': 'Unauthorized'}
            )
    except Exception as e:
        logger_utils.logger.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'message': 'Unauthorized'}
        )

    try:
        coworking_by_id = db.query(coworking_model.Coworking).filter(coworking_model.Coworking.id == id).first()
    except Exception as e:
        logger_utils.logger.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={'message': 'Server internal error'}
        )

    if not coworking_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'message': 'Coworking not found'}
        )

    # update coworking
    try:
        db.query(coworking_model.Coworking).filter(coworking_model.Coworking.id == id).update({
            coworking_model.Coworking.name: coworking.name,
            coworking_model.Coworking.ubication: coworking.ubication,
            coworking_model.Coworking.price_by_hour: coworking.price_by_hour,
            coworking_model.Coworking.capacity: coworking.capacity,
            coworking_model.Coworking.is_available: coworking.is_available
        })

        db.commit()
    except Exception as e:
        logger_utils.logger.debug(str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={'message': 'Server internal error'}
        )

    return {
        'message': 'Coworking updated'
    }


@router.delete('/{id}', dependencies=[Depends(jwt_utils.check_jwt)])
def delete_coworking(id: int = Path(), db: Session = Depends(get_db), token_payload: dict = Depends(jwt_utils.check_jwt)):
    try:
        if token_payload['role'] != 'admin':
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={'message': 'Unauthorized'}
            )
    except Exception as e:
        logger_utils.logger.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={'message': 'Unauthorized'}
        )

    try:
        coworking_by_id = db.query(coworking_model.Coworking).filter(coworking_model.Coworking.id == id).first()
    except Exception as e:
        logger_utils.logger.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={'message': 'Server internal error'}
        )

    if not coworking_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'message': 'Coworking not found'}
        )

    try:
        db.delete(coworking_by_id)
        db.commit()
    except Exception as e:
        logger_utils.logger.debug(str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={'message': 'Server internal error'}
        )
