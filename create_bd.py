from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import inspect
from sqlalchemy.sql.schema import Table
import asyncio

# Importa la configuración de la base de datos
from database.database import Base, DATABASE_URL

# Importa tus modelos
from database.models.word import Word, DefinitionsEs, DefinitionsEn, TranslationEs, TranslationEn, Imagen, Audio, Curso, Asignatura
from database.models.usuario import Usuario, SesionUsuario
from database.models.reto import Reto


async def create_tables():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("¡Tablas creadas con Éxito. Una cosa Menos!")


async def check_tables_exist():
    engine = create_async_engine(DATABASE_URL)
    async with engine.connect() as conn:
        def get_tables(sync_conn):
            inspector = inspect(sync_conn)
            return inspector.get_table_names()

        tables = await conn.run_sync(get_tables)

    model_tables = [
        Word.__tablename__,
        DefinitionsEs.__tablename__,
        DefinitionsEn.__tablename__,
        TranslationEs.__tablename__,
        TranslationEn.__tablename__,
        Imagen.__tablename__,
        # WordImagenes.__tablename__,
        Audio.__tablename__,
        # WordAudio.__tablename__,
        Curso.__tablename__,
        Asignatura.__tablename__,
        Usuario.__tablename__,
        SesionUsuario.__tablename__,
        # ResultadoEjercicio.__tablename__,
        Reto.__tablename__,
        # WordReto.__tablename__,
        # ResultadoReto.__tablename__,
        # WordModification.__tablename__  # Asegúrate de incluir el nuevo modelo
    ]

    tables_to_create = [table for table in model_tables if table not in tables]

    if tables_to_create:
        await create_tables()
    else:
        print("Las tablas ya existen en la base de datos.")


async def main():
    await check_tables_exist()

if __name__ == "__main__":
    asyncio.run(main())
