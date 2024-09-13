from sqlalchemy import Column, Integer, DECIMAL, String, DateTime
from sqlalchemy.sql import func
from database.session import Base


class Coworking(Base):
    __tablename__ = 'coworking'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(127), nullable=False)
    ubication = Column(String(127), nullable=False)
    price_by_hour = Column(DECIMAL(10, 2), nullable=True)
    capacity = Column(Integer, nullable=False)
    is_available = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
