from pydantic import BaseModel
from typing import Optional, List
from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, Session, relationship


'''create app instance'''
app = FastAPI()

'''SqlAlchemy Setup'''
SQLALCHEMY_DATABASE_URL = 'sqlite+pysqlite:///./db.sqlite3:'
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """configure db"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


'''import module related apis'''
from Application.API.people import *
from Application.API.like import *
