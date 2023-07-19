from typing import Annotated
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import Depends

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:valentina@localhost:5432/todos'

engine = create_engine(SQLALCHEMY_DATABASE_URL); # crear manipular tablas - motor

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine); # obj de coneccion 

Base = declarative_base();

def create_tables():
  Base.metadata.create_all(bind=engine);
  
def get_db():
  db = SessionLocal();
  try:
    yield db;
  finally:
    db.close();

db_dependency = Annotated[Session, Depends(get_db)]
