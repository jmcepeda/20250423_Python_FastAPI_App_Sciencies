from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
from datetime import datetime

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    wordpress_id = Column(Integer, unique=True, index=True, nullable=False)  # ID del usuario en WordPress
    fecha_registro = Column(DateTime, default=datetime.utcnow)

    sesiones = relationship("SesionUsuario", back_populates="usuario")
    resultados = relationship("ResultadoEjercicio", back_populates="usuario")
    retos_enviados = relationship("Reto", foreign_keys="[Reto.usuario_remitente_id]", back_populates="remitente")
    retos_recibidos = relationship("Reto", foreign_keys="[Reto.usuario_destinatario_id]", back_populates="destinatario")
    resultados_reto = relationship("ResultadoReto", back_populates="usuario")

class SesionUsuario(Base):
    __tablename__ = "sesiones_usuario"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id"))
    fecha_inicio = Column(DateTime, default=datetime.utcnow)
    fecha_fin = Column(DateTime)

    usuario = relationship("Usuario", back_populates="sesiones")