from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database.session import Base


class Admin(Base):
    __tablename__ = 'admin'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(127), nullable=False)
    email = Column(String(127), nullable=False)
    password = Column(String(127), nullable=False)
    created_at = Column(DateTime, default=func.now())
