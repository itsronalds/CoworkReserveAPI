from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.deps import get_db


router = APIRouter(prefix='/coworking', tags=['coworking'])


@router.post('/')
def create_coworking(coworking, db: Session = Depends(get_db)):
    try:
        pass
    except Exception as e:
        print(str(e))
