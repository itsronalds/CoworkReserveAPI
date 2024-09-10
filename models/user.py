from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database.session import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(127), index=True, nullable=False)
    email = Column(String(127), unique=True, index=True, nullable=False)
    password = Column(String(127), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
