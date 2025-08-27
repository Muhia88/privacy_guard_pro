import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#The Database File Path Configuration 
#ensures the database file is always found relative to this script's location

#absolute path for the database file to avoid location issues
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = os.path.join(project_dir, "../..", "privacy_guard.db")
DATABASE_URL = f'sqlite:///{database_path}'

#SQLAlchemy engine and session factory setup
engine = create_engine(DATABASE_URL)
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base class for declarative models
Base = declarative_base()

def get_db_session():
    """Provides a new database session."""
    return Session()