from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Palabra(Base):
    __tablename__ = "palabras"

    id = Column(Integer, primary_key=True, index=True)
    palabra_es = Column(String(255), nullable=False)
    palabra_en = Column(String(255), nullable=False)
    edad_minima = Column(Integer)
    edad_maxima = Column(Integer)
    curso_id = Column(Integer, ForeignKey("cursos.id"))
    asignatura_id = Column(Integer, ForeignKey("asignaturas.id"))

    definiciones_es = relationship("DefinicionEs", back_populates="palabra")
    definiciones_en = relationship("DefinicionEn", back_populates="palabra")
    traducciones_es = relationship("TraduccionEs", back_populates="palabra")
    traducciones_en = relationship("TraduccionEn", back_populates="palabra")
    imagenes = relationship("Imagen", secondary="palabras_imagenes", back_populates="palabras")
    audios = relationship("Audio", secondary="palabras_audios", back_populates="palabras")
    curso = relationship("Curso", back_populates="palabras")
    asignatura = relationship("Asignatura", back_populates="palabras")
    resultados = relationship("ResultadoEjercicio", back_populates="palabra")
    palabras_reto = relationship("PalabraReto", back_populates="palabra")

class DefinicionEs(Base):
    __tablename__ = "definiciones_es"

    id = Column(Integer, primary_key=True, index=True)
    palabra_id = Column(Integer, ForeignKey("palabras.id"))
    definicion = Column(String(1000), nullable=False)

    palabra = relationship("Palabra", back_populates="definiciones_es")

class DefinicionEn(Base):
    __tablename__ = "definiciones_en"

    id = Column(Integer, primary_key=True, index=True)
    palabra_id = Column(Integer, ForeignKey("palabras.id"))
    definicion = Column(String(1000), nullable=False)

    palabra = relationship("Palabra", back_populates="definiciones_en")

class TraduccionEs(Base):
    __tablename__ = "traducciones_es"

    id = Column(Integer, primary_key=True, index=True)
    palabra_id = Column(Integer, ForeignKey("palabras.id"))
    traduccion = Column(String(255), nullable=False)

    palabra = relationship("Palabra", back_populates="traducciones_es")

class TraduccionEn(Base):
    __tablename__ = "traducciones_en"

    id = Column(Integer, primary_key=True, index=True)
    palabra_id = Column(Integer, ForeignKey("palabras.id"))
    traduccion = Column(String(255), nullable=False)

    palabra = relationship("Palabra", back_populates="traducciones_en")

class Imagen(Base):
    __tablename__ = "imagenes"

    id = Column(Integer, primary_key=True, index=True)
    nombre_archivo = Column(String(255), nullable=False)
    ruta_archivo = Column(String(1000), nullable=False)

    palabras = relationship("Palabra", secondary="palabras_imagenes", back_populates="imagenes")

class PalabraImagen(Base):
    __tablename__ = "palabras_imagenes"
    palabra_id = Column(Integer, ForeignKey("palabras.id"), primary_key=True)
    imagen_id = Column(Integer, ForeignKey("imagenes.id"), primary_key=True)

class Audio(Base):
    __tablename__ = "audios"

    id = Column(Integer, primary_key=True, index=True)
    nombre_archivo = Column(String(255), nullable=False)
    ruta_archivo = Column(String(1000), nullable=False)

    palabras = relationship("Palabra", secondary="palabras_audios", back_populates="audios")

class PalabraAudio(Base):
    __tablename__ = "palabras_audios"
    palabra_id = Column(Integer, ForeignKey("palabras.id"), primary_key=True)
    audio_id = Column(Integer, ForeignKey("audios.id"), primary_key=True)

class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    nombre_curso = Column(String(255), nullable=False, unique=True)

    palabras = relationship("Palabra", back_populates="curso")
    asignaturas = relationship("Asignatura", back_populates="curso")

class Asignatura(Base):
    __tablename__ = "asignaturas"

    id = Column(Integer, primary_key=True, index=True)
    nombre_asignatura = Column(String(255), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id"))

    palabras = relationship("Palabra", back_populates="asignatura")
    curso = relationship("Curso", back_populates="asignaturas")