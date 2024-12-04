from sqlmodel import Session, SQLModel, create_engine
from typing import Annotated
from fastapi import Depends

# Database URLs
SQLITE_FILE_NAME = "hilbre.db"
SQLITE_URL = f"sqlite:///{SQLITE_FILE_NAME}"

# Database configuration
connect_args = {"check_same_thread": False}
engine = create_engine(SQLITE_URL, connect_args=connect_args)

def get_session():
    with Session(engine) as session:
        yield session

# Dependency for routes
SessionDep = Annotated[Session, Depends(get_session)]

def create_hilbre_db_and_tables():
    SQLModel.metadata.create_all(engine)