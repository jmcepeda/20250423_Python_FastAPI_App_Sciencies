from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum, Boolean, Float
from sqlalchemy.orm import relationship
from database.database import Base
from database.models.ejercicio import TipoEjercicio  # Importa TipoEjercicio
from datetime import datetime
import enum


class EstadoReto(enum.Enum):
    SIN_INICIAR = "sin_iniciar"
    EMPEZADO = "empezado"
    TERMINADO = "terminado"


class Reto(Base):
    __tablename__ = "retos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), default="Reto sin nombre")
    usuario_remitente_id = Column(Integer, ForeignKey("usuario.id"))
    usuario_destinatario_id = Column(Integer, ForeignKey("usuario.id"))
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    estado = Column(Enum(EstadoReto), default=EstadoReto.SIN_INICIAR)

    # remitente = relationship("Usuario", foreign_keys=[
    #                          usuario_remitente_id], back_populates="retos_enviados")
    # destinatario = relationship("Usuario", foreign_keys=[
    #                             usuario_destinatario_id], back_populates="retos_recibidos")
    # words_reto = relationship("WordReto", back_populates="reto")
    # resultados_reto = relationship("ResultadoReto", back_populates="reto")


# class WordReto(Base):
#     __tablename__ = "words_reto"

#     id = Column(Integer, primary_key=True, index=True)
#     reto_id = Column(Integer, ForeignKey("retos.id"))
#     word_id = Column(Integer, ForeignKey("words.id"))
#     # Especifica el tipo de ejercicio para esta palabra en el reto
#     # tipo_ejercicio = Column(Enum(TipoEjercicio), nullable=False)

#     # reto = relationship("Reto", back_populates="words_reto")
#     # word = relationship("Word", back_populates="words_reto")


# class ResultadoReto(Base):
#     __tablename__ = "resultados_reto"

#     id = Column(Integer, primary_key=True, index=True)
#     reto_id = Column(Integer, ForeignKey("retos.id"))
#     usuario_id = Column(Integer, ForeignKey("usuario.id"))
#     palabra_id = Column(Integer, ForeignKey("words.id"))
#     fecha = Column(DateTime, default=datetime.utcnow)
#     # tipo_ejercicio = Column(Enum(TipoEjercicio), nullable=False)
#     acierto = Column(Boolean, nullable=False)
#     tiempo_respuesta = Column(Float)
#     tipo_fallo = Column(String(255))

#     reto = relationship("Reto", back_populates="resultados_reto")
#     usuario = relationship("Usuario", back_populates="resultados_reto")
#     palabra = relationship("Word", back_populates="resultados_reto")
