from fastapi import APIRouter, Path, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database.deps import get_db

import models.coworking as coworking_model
import schemas.coworking as coworking_schema
import utils.logger as logger_utils


router = APIRouter(prefix='/coworking', tags=['coworking'])


@router.get('/')
def get_coworkings(name: str = '', price_by_hour: float = 0.0, is_available: int = 1, db: Session = Depends(get_db)):
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


@router.post('/')
def create_coworking(coworking: coworking_schema.CoworkingBase, db: Session = Depends(get_db)):
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
def update_coworking(coworking: coworking_schema.Coworking, db: Session = Depends(get_db), id: int = Path()):
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
            coworking_by_id.name: coworking.name,
            coworking_by_id.ubication: coworking.ubication,
            coworking_by_id.price_by_hour: coworking.price_by_hour,
            coworking_by_id.capacity: coworking.capacity,
            coworking_by_id.is_available: coworking.is_available
        })

        db.commit()
        db.refresh(coworking_by_id)
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


@router.delete('/{id}')
def delete_coworking(id: int = Path(), db: Session = Depends(get_db)):
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
