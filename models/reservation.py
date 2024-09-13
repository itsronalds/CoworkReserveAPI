from sqlalchemy import Column, Integer, TIME, DATE, DateTime
from sqlalchemy.sql import func
from database.session import Base


class Reservation(Base):
    __tablename__ = 'reservation'

    id = Column(Integer, primary_key=True, index=True)
    coworking_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    date = Column(DATE, nullable=False)
    start_time = Column(TIME, nullable=False)
    end_time = Column(TIME, nullable=False)
    created_at = Column(DateTime, default=func.now())
