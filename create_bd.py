from sqlalchemy import create_engine, inspect
from database.database import Base, DATABASE_URL  # Importa la configuración de la base de datos
from database.models.palabra import *
from database.models.usuario import *
from database.models.ejercicio import *
from database.models.reto import *

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)
tables = inspector.get_table_names()

model_tables = [
    Palabra.__tablename__,
    DefinicionEs.__tablename__,
    DefinicionEn.__tablename__,
    TraduccionEs.__tablename__,
    TraduccionEn.__tablename__,
    Imagen.__tablename__,
    PalabraImagen.__tablename__,
    Audio.__tablename__,
    PalabraAudio.__tablename__,
    Curso.__tablename__,
    Asignatura.__tablename__,
    Usuario.__tablename__,
    SesionUsuario.__tablename__,
    ResultadoEjercicio.__tablename__,
    Reto.__tablename__,
    PalabraReto.__tablename__,
    ResultadoReto.__tablename__,
]

tables_to_create = [table for table in model_tables if table not in tables]

if tables_to_create:
    Base.metadata.create_all(bind=engine)
    print(f"¡Se han creado las siguientes tablas: {', '.join(tables_to_create)}!")
else:
    print("Las tablas ya existen en la base de datos.")