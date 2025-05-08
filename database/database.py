from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define la URL de tu base de datos MariaDB (con asyncmy como driver)
DATABASE_URL = "mysql+asyncmy://jmcepeda:cintiatyron2015@192.168.50.150:3366/app_sciencies?charset=utf8mb4"

SQL_INIT_FILE = "database/init.sql"

engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, class_=AsyncSession)
Base = declarative_base()


async def get_db():
    session = async_session_maker()
    try:
        yield session
    finally:
        await session.close()
