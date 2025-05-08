from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime

from database.models.word import Curso
from database.models.word import Asignatura
from database.database import get_db
from fastapi import Depends, FastAPI, HTTPException, APIRouter

Base = declarative_base()

# class Curso(Base):
#     __tablename__ = 'curso'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)

# class Asignatura(Base):
#     __tablename__ = 'asignatura'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)

# db: AsyncSession = Depends(get_db)

# Corrección aquí


async def get_curso_and_asignatura_id(year_nacimiento: int, num_repetidos: int, asignatura_name: str,  db: AsyncSession = Depends(get_db),):
    """
    Calcula el curso y devuelve el ID del curso y de la asignatura correspondiente.

    Args:
        year_nacimiento (int): Año de nacimiento de la persona.
        num_repetidos (int): Número de cursos que ha repetido.
        db_path (str): Ruta a la base de datos.

    Returns:
        tuple: Una tupla con el ID del curso y el ID de la asignatura.
               Devuelve (None, None) si no se encuentra el curso o la asignatura.
    """
    current_year = datetime.now().year
    edad_escolar = current_year - year_nacimiento - num_repetidos

    curso_name = ""

    if edad_escolar <= 3:
        curso_name = "Guardería"
    elif edad_escolar == 4:
        curso_name = "Guardería"
    elif edad_escolar == 5:
        curso_name = "Primero de Infantil"
    elif edad_escolar == 6:
        curso_name = "Segundo de Infantil"
    elif edad_escolar == 7:
        curso_name = "Primero de Primaria"
    elif edad_escolar == 8:
        curso_name = "Segundo de Primaria"
    elif edad_escolar == 9:
        curso_name = "Tercero de Primaria"
    elif edad_escolar == 10:
        curso_name = "Cuarto de Primaria"
    elif edad_escolar == 11:
        curso_name = "Quinto de Primaria"
    elif edad_escolar == 12:
        curso_name = "Sexto de Primaria"
    elif edad_escolar == 13:
        curso_name = "Primero de Secundaria"
    elif edad_escolar == 14:
        curso_name = "Segundo de Secundaria"
    elif edad_escolar == 15:
        curso_name = "Tercero de Secundaria"
    elif edad_escolar == 16:
        curso_name = "Cuarto de Secundaria"
    elif edad_escolar == 17:
        curso_name = "Primero de Bachillerato"
    elif edad_escolar == 18:
        curso_name = "Segundo de Bachillerato"

    print(f"Curso calculado: {curso_name}")
    result_curso = await db.execute(select(Curso).where(Curso.nombre_curso == curso_name))

    curso_id = result_curso.scalar_one_or_none().id

    print(f"ID del curso: {curso_id}")

    print(f"Nombre de la asignatura: {asignatura_name.lower()}")

    result_asignatura = await db.execute(select(Asignatura).where(Asignatura.nombre_asignatura == asignatura_name.lower(), Asignatura.curso_id == curso_id))
    resultado_asignatura = result_asignatura.scalar_one_or_none()

    if resultado_asignatura is None:
        # If no result is found, it's helpful to query all Asignatura records
        # with the matching curso_id to see if there are any name discrepancies.
        all_asignaturas_for_curso = await db.execute(select(Asignatura).where(Asignatura.curso_id == curso_id))
        print(f"Todas las asignaturas para curso_id {curso_id}:")
        for asignatura in all_asignaturas_for_curso.scalars().all():
            print(
                f"- Nombre: {asignatura.nombre_asignatura}, Curso ID: {asignatura.curso_id}")

    print(f"Resultado de la consulta de asignatura:")
    print(resultado_asignatura)

    asignatura_id = resultado_asignatura.id

    print(
        f"Función get_curso_and_asignatura_id: ID de la asignatura: {asignatura_id}")
    print(f"Función get_curso_and_asignatura_id: ID del curso: {curso_id}")

    response = {
        "curso_id": curso_id,
        "asignatura_id": asignatura_id
    }

    return response
