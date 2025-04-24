from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime




Base = declarative_base()

DATABASE_URL ="sqlite:///chessdev.db"

engine = create_engine(DATABASE_URL, echo=True)

def delete_tables():
    Base.metadata.drop_all(engine)

Session = sessionmaker(bind=engine)

def create_tables():
    Base.metadata.create_all(engine)

def get_session():
    return Session()

