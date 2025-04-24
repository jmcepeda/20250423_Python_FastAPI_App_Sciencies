from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define la URL de tu base de datos MariaDB
DATABASE_URL = "mysql+mysqlconnector://jmcepeda:cintiatyron2015@192.168.50.150:3366/app_sciencies?charset=utf8mb4&collation=utf8mb4_unicode_ci" 

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()