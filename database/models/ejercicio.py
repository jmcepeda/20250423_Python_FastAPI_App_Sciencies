from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, Enum, Float, String
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime
import enum


class TipoEjercicio(enum.Enum):
    UNIR_PALABRAS = "unir_palabras"
    ESCRIBIR_INGLES = "escribir_ingles"
    SELECCIONAR_AUDIO_ES = "seleccionar_audio_es"
    SELECCIONAR_COLUMNAS = "seleccionar_columnas"


# class ResultadoEjercicio(Base):
#     __tablename__ = "resultados_ejercicio"

#     id = Column(Integer, primary_key=True, index=True)
#     usuario_id = Column(Integer, ForeignKey("usuario.id"))
#     word_id = Column(Integer, ForeignKey("words.id"))
#     fecha = Column(DateTime, default=datetime.utcnow)
#     tipo_ejercicio = Column(Enum(TipoEjercicio), nullable=False)
#     acierto = Column(Boolean, nullable=False)
#     tiempo_respuesta = Column(Float)  # Tiempo en segundos
#     tipo_fallo = Column(String(255))  # Detalles del fallo (opcional)

#     usuario = relationship("Usuario", back_populates="resultados")
#     palabra = relationship("Word", back_populates="resultados")
