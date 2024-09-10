from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import CONFIG

# define the database URL
SQLALCHEMY_DATABASE_URL = CONFIG['DATABASE_URI'] or ''

# create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# create a base class for our models
Base = declarative_base()
