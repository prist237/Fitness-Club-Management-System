# app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base

# Adjust credentials/DB name for your setup
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
