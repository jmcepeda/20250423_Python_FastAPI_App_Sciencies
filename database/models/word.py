from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime, timezone


class Word(Base):
    __tablename__ = "words"

    id = Column(Integer, primary_key=True, index=True)
    word_es = Column(String(255), nullable=False)
    word_en = Column(String(255), nullable=False)
    # edad_minima = Column(Integer)
    # edad_maxima = Column(Integer)
    curso_id = Column(Integer, ForeignKey("cursos.id"))
    asignatura_id = Column(Integer, ForeignKey("asignaturas.id"))
    # Nuevo campo: ID del usuario que creó la palabra
    created_by = Column(Integer, ForeignKey("usuario.id"))
    # Nuevo campo: Fecha y hora de creación
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    definitions_es = relationship("DefinitionsEs", back_populates="word")
    definitions_en = relationship("DefinitionsEn", back_populates="word")
    translations_es = relationship("TranslationEs", back_populates="word")
    translations_en = relationship("TranslationEn", back_populates="word")
    # imagenes = relationship("Imagen", secondary="words_imagenes", back_populates="words")
    # audios = relationship("Audio", secondary="words_audios", back_populates="words")
    curso = relationship("Curso", back_populates="word")
    asignatura = relationship("Asignatura", back_populates="word")
    # resultados = relationship("ResultadoEjercicio", back_populates="words")
    # words_reto = relationship("WordReto", back_populates="words")


class DefinitionsEs(Base):
    __tablename__ = "definitions_es"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))
    definicion = Column(String(1000), nullable=False)
    # Nuevo campo: ID del usuario que creó la palabra
    created_by = Column(Integer, ForeignKey("usuario.id"))
    # Nuevo campo: Fecha y hora de creación
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    word = relationship("Word", back_populates="definitions_es")


class DefinitionsEn(Base):
    __tablename__ = "definitions_en"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))
    definicion = Column(String(1000), nullable=False)
    # Nuevo campo: ID del usuario que creó la palabra
    created_by = Column(Integer, ForeignKey("usuario.id"))
    # Nuevo campo: Fecha y hora de creación
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    word = relationship("Word", back_populates="definitions_en")


class TranslationEs(Base):
    __tablename__ = "translations_es"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))
    traduccion = Column(String(255), nullable=False)
    # Nuevo campo: ID del usuario que creó la palabra
    created_by = Column(Integer, ForeignKey("usuario.id"))
    # Nuevo campo: Fecha y hora de creación
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    word = relationship("Word", back_populates="translations_es")


class TranslationEn(Base):
    __tablename__ = "translations_en"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))
    traduccion = Column(String(255), nullable=False)
    # Nuevo campo: ID del usuario que creó la palabra
    created_by = Column(Integer, ForeignKey("usuario.id"))
    # Nuevo campo: Fecha y hora de creación
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    word = relationship("Word", back_populates="translations_en")


class Imagen(Base):
    __tablename__ = "imagen"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))
    nombre_archivo = Column(String(255), nullable=False)
    ruta_archivo = Column(String(1000), nullable=False)
    # Nuevo campo: ID del usuario que creó la palabra
    created_by = Column(Integer, ForeignKey("usuario.id"))
    # Nuevo campo: Fecha y hora de creación
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # words = relationship("Word", secondary="words_imagenes", back_populates="imagen")


# class WordImagenes(Base):
#     __tablename__ = "words_imagenes"
#     word_id = Column(Integer, ForeignKey("words.id"), primary_key=True)
#     imagen_id = Column(Integer, ForeignKey("imagen.id"), primary_key=True)
#     # Nuevo campo: ID del usuario que creó la palabra
#     created_by = Column(Integer, ForeignKey("usuario.id"))
#     # Nuevo campo: Fecha y hora de creación
#     created_at = Column(DateTime, default=datetime.now(timezone.utc))


class Audio(Base):
    __tablename__ = "audios"

    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, ForeignKey("words.id"))
    nombre_archivo = Column(String(255), nullable=False)
    ruta_archivo = Column(String(1000), nullable=False)
    # Nuevo campo: ID del usuario que creó la palabra
    created_by = Column(Integer, ForeignKey("usuario.id"))
    # Nuevo campo: Fecha y hora de creación
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    # words = relationship("word", secondary="words_audios", back_populates="audios")


# class WordAudio(Base):
#     __tablename__ = "words_audios"
#     word_id = Column(Integer, ForeignKey("words.id"), primary_key=True)
#     audio_id = Column(Integer, ForeignKey("audios.id"), primary_key=True)
#     # Nuevo campo: ID del usuario que creó la palabra
#     created_by = Column(Integer, ForeignKey("usuario.id"))
#     # Nuevo campo: Fecha y hora de creación
#     created_at = Column(DateTime, default=datetime.now(timezone.utc))


class Curso(Base):
    __tablename__ = "cursos"

    id = Column(Integer, primary_key=True, index=True)
    nombre_curso = Column(String(255), nullable=False, unique=True)
    level = Column(Integer)  # Nuevo campo para el nivel del curso
    # Nuevo campo: Fecha y hora de creación
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    word = relationship("Word", back_populates="curso")
    asignatura = relationship("Asignatura", back_populates="curso")


class Asignatura(Base):
    __tablename__ = "asignaturas"

    id = Column(Integer, primary_key=True, index=True)
    nombre_asignatura = Column(String(255), nullable=False)
    curso_id = Column(Integer, ForeignKey("cursos.id"))
    # Nuevo campo: Fecha y hora de creación
    created_at = Column(DateTime, default=datetime.now(timezone.utc))

    word = relationship("Word", back_populates="asignatura")
    curso = relationship("Curso", back_populates="asignatura")


# class WordModification(Base):
#     __tablename__ = "word_modification"

#     id = Column(Integer, primary_key=True, index=True)
#     word_id = Column(Integer, ForeignKey("words.id"))  # Cambiado a "words.id"
#     modified_by = Column(Integer, ForeignKey("usuario.id"))
#     modified_at = Column(DateTime, default=datetime.now(timezone.utc))
#     word = relationship("Word", back_populates="modifications")
#     modifier = relationship("Usuario", foreign_keys=[
#                             modified_by], back_populates="modified_words")
#     # Nuevo campo: ID del usuario que creó la palabra
#     created_by = Column(Integer, ForeignKey("usuario.id"))
#     # Nuevo campo: Fecha y hora de creación
#     created_at = Column(DateTime, default=datetime.now(timezone.utc))
