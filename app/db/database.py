from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLITE_DATABASE_URL = 'sqlite:///./database.db'
SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:1234@localhost:5432/kindergarten'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
sqlite_engine = create_engine(SQLITE_DATABASE_URL)

SessionLocalSQLite = sessionmaker(autocommit=False, autoflush=False, bind=sqlite_engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
