from sqlmodel import Field, Session, SQLModel, create_engine, select
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.ext.declarative import declarative_base

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}" # string for sqlite db

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


# what are these for? 
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# Base = declarative_base()

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)