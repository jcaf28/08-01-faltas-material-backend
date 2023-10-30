# app/db/session.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = scoped_session(SessionLocal)

def get_db():
    db = session()
    try:
        yield db
    finally:
        db.close()

class DatabaseSession:
    def __init__(self, session):
        self.session = session

    def __enter__(self):
        self.db = self.session()
        return self.db

    def __exit__(self, exc_type, exc_value, traceback):
        self.db.close()

database_session = DatabaseSession(session)