from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import inspect
from sqlalchemy.sql.schema import Table
import asyncio

# Importa la configuración de la base de datos
from database.database import Base, DATABASE_URL

# Importa tus modelos
from database.models.word import Word, DefinitionsEs, DefinitionsEn, TranslationEs, TranslationEn, Imagen, Audio
from database.models.word import Curso
from database.models.word import Asignatura
from database.models.usuario import Usuario, SesionUsuario
from database.models.reto import Reto


async def create_tables():
    engine = create_async_engine(DATABASE_URL)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("¡Tablas creadas con Éxito. Una cosa Menos!")


async def insert_initial_data(engine):
    async with AsyncSession(engine) as session:
        # Insertar datos en la tabla 'cursos'
        cursos_data = [
            {'id': 1, 'nombre_curso': 'Guardería', 'level': 0},
            {'id': 2, 'nombre_curso': 'Primero de Infantil', 'level': 1},
            {'id': 3, 'nombre_curso': 'Segundo de Infantil', 'level': 2},
            {'id': 4, 'nombre_curso': 'Primero de Primaria', 'level': 3},
            {'id': 5, 'nombre_curso': 'Segundo de Primaria', 'level': 4},
            {'id': 6, 'nombre_curso': 'Tercero de Primaria', 'level': 5},
            {'id': 7, 'nombre_curso': 'Cuarto de Primaria', 'level': 6},
            {'id': 8, 'nombre_curso': 'Quinto de Primaria', 'level': 7},
            {'id': 9, 'nombre_curso': 'Sexto de Primaria', 'level': 8},
            {'id': 10, 'nombre_curso': 'Primero de Secundaria', 'level': 9},
            {'id': 11, 'nombre_curso': 'Segundo de Secundaria', 'level': 10},
            {'id': 12, 'nombre_curso': 'Tercero de Secundaria', 'level': 11},
            {'id': 13, 'nombre_curso': 'Cuarto de Secundaria', 'level': 12},
            {'id': 14, 'nombre_curso': 'Primero de Bachillerato', 'level': 13},
            {'id': 15, 'nombre_curso': 'Segundo de Bachillerato', 'level': 14},
        ]
        for curso_info in cursos_data:
            curso = Curso(**curso_info)
            session.add(curso)

        # Insertar datos en la tabla 'asignaturas'
        asignaturas_data = [
            {'id': 1, 'nombre_asignatura': 'Sciences', 'curso_id': 1},
            {'id': 2, 'nombre_asignatura': 'Sciences', 'curso_id': 2},
            {'id': 3, 'nombre_asignatura': 'Sciences', 'curso_id': 3},
            {'id': 4, 'nombre_asignatura': 'Sciences', 'curso_id': 4},
            {'id': 5, 'nombre_asignatura': 'Sciences', 'curso_id': 5},
            {'id': 6, 'nombre_asignatura': 'Sciences', 'curso_id': 6},
            {'id': 7, 'nombre_asignatura': 'Sciences', 'curso_id': 7},
            {'id': 8, 'nombre_asignatura': 'Sciences', 'curso_id': 8},
            {'id': 9, 'nombre_asignatura': 'Sciences', 'curso_id': 9},
            {'id': 10, 'nombre_asignatura': 'Sciences', 'curso_id': 10},
            {'id': 11, 'nombre_asignatura': 'Sciences', 'curso_id': 11},
            {'id': 12, 'nombre_asignatura': 'Sciences', 'curso_id': 12},
            {'id': 13, 'nombre_asignatura': 'Sciences', 'curso_id': 13},
            {'id': 14, 'nombre_asignatura': 'Sciences', 'curso_id': 14},
            {'id': 15, 'nombre_asignatura': 'English', 'curso_id': 2},
            {'id': 16, 'nombre_asignatura': 'English', 'curso_id': 3},
            {'id': 17, 'nombre_asignatura': 'English', 'curso_id': 4},
            {'id': 18, 'nombre_asignatura': 'English', 'curso_id': 5},
            {'id': 19, 'nombre_asignatura': 'English', 'curso_id': 6},
            {'id': 20, 'nombre_asignatura': 'English', 'curso_id': 7},
            {'id': 21, 'nombre_asignatura': 'English', 'curso_id': 8},
            {'id': 22, 'nombre_asignatura': 'English', 'curso_id': 9},
            {'id': 23, 'nombre_asignatura': 'English', 'curso_id': 10},
            {'id': 24, 'nombre_asignatura': 'English', 'curso_id': 11},
            {'id': 25, 'nombre_asignatura': 'English', 'curso_id': 12},
            {'id': 26, 'nombre_asignatura': 'English', 'curso_id': 13},
        ]
        for asignatura_info in asignaturas_data:
            asignatura = Asignatura(**asignatura_info)
            session.add(asignatura)

        await session.commit()
    print("¡Datos iniciales de Cursos y Asignaturas insertados con éxito!")


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
        Audio.__tablename__,
        Curso.__tablename__,
        Asignatura.__tablename__,
        Usuario.__tablename__,
        SesionUsuario.__tablename__,
        Reto.__tablename__,
    ]

    tables_to_create = [table for table in model_tables if table not in tables]

    if tables_to_create:
        await create_tables()
        engine_insert = create_async_engine(DATABASE_URL)
        await insert_initial_data(engine_insert)
        await engine_insert.dispose()
    else:
        print("Las tablas ya existen en la base de datos.")
        # Puedes optar por insertar los datos también si las tablas ya existen
        # engine_insert = create_async_engine(DATABASE_URL)
        # await insert_initial_data(engine_insert)
        # await engine_insert.dispose()


async def main():
    await check_tables_exist()

if __name__ == "__main__":
    asyncio.run(main())
