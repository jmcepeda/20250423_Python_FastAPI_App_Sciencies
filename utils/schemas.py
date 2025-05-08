# Importa ConfigDict para Pydantic V2
from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date


class WordCreateRequest(BaseModel):
    word_en: str
    word_es: Optional[str] = None  # Campo word_es ahora es opcional
    lang: str
    username: str
    firstname: str
    lastname: str
    email: str
    wordpress_id: int
    birthdate: date
    asignatura: str


class CurrentUserResponse(BaseModel):
    id: Optional[int] = None
    username: str
    firstname: str
    lastname: str
    email: str
    wordpress_id: int
    usuario_existente_db: bool


class CreateUser(BaseModel):
    id: Optional[int] = None
    username: str
    firstname: str
    lastname: str
    email: str
    wordpress_id: int
    usuario_existente_db: bool


class WordResponse(BaseModel):
    id: int
    word_en: str
    word_es: str
    curso_id: Optional[int] = None  # Usa Optional si pueden ser NULL en la BD
    # Usa Optional si pueden ser NULL en la BD
    asignatura_id: Optional[int] = None
    created_by: int  # O podrías anidar un UserResponse aquí si quieres

    # --- Configuración importante ---
    # Para Pydantic V2:
    model_config = ConfigDict(from_attributes=True)
    # Para Pydantic V1 (si usas una versión anterior):
    # class Config:
    #     orm_mode = True
