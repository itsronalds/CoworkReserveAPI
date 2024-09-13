from fastapi import APIRouter, Path, Depends, HTTPException, status

# database
from sqlalchemy.orm import Session
from database.deps import get_db

# models
import models.reservation as reservation_model

# schemas
import schemas.reservation as reservation_schema

# utils
import utils.logger as logger_utils
import utils.jwt as jwt_utils


router = APIRouter(prefix='/reservation', tags=['reservation'])


@router.get('/')
def get_reservations(db: Session = Depends(get_db), token_payload: dict = Depends(jwt_utils.check_jwt)):
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
        reservations = db.query(reservation_model.Reservation).all()
    except Exception as e:
        logger_utils.logger.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={'message': 'Server internal error'}
        )

    return reservations


@router.post('/', dependencies=[Depends(jwt_utils.check_jwt)])
def create_reservation(reservation: reservation_schema.ReservationBase, db: Session = Depends(get_db), token_payload: dict = Depends(jwt_utils.check_jwt)):
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

    new_reservation = reservation_model.Reservation(
        coworking_id=reservation.coworking_id,
        user_id=reservation.user_id,
        date=reservation.date,
        start_time=reservation.start_time,
        end_time=reservation.end_time
    )

    try:
        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)
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
def update_reservation(reservation: reservation_schema.ReservationBase, db: Session = Depends(get_db), token_payload: dict = Depends(jwt_utils.check_jwt), id: int = Path()):
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
        reservation_by_id = db.query(reservation_model.Reservation).filter(
            reservation_model.Reservation.id == id).first()
    except Exception as e:
        logger_utils.logger.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={'message': 'Server internal error'}
        )

    if not reservation_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'message': 'Reservation not found'}
        )

    # update coworking
    try:
        db.query(reservation_model.Reservation).filter(reservation_model.Reservation.id == id).update({
            reservation_model.Reservation.coworking_id: reservation.coworking_id,
            reservation_model.Reservation.user_id: reservation.user_id,
            reservation_model.Reservation.date: reservation.date,
            reservation_model.Reservation.start_time: reservation.start_time,
            reservation_model.Reservation.end_time: reservation.end_time
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
def delete_reservation(id: int = Path(), db: Session = Depends(get_db), token_payload: dict = Depends(jwt_utils.check_jwt)):
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
        reservation_by_id = db.query(reservation_model.Reservation).filter(
            reservation_model.Reservation.id == id).first()
    except Exception as e:
        logger_utils.logger.debug(str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={'message': 'Server internal error'}
        )

    if not reservation_by_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={'message': 'Reservation not found'}
        )

    try:
        db.delete(reservation_by_id)
        db.commit()
    except Exception as e:
        logger_utils.logger.debug(str(e))
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={'message': 'Server internal error'}
        )
