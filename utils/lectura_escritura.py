import os
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.database import get_db
# from database.models.word import Word, DefinitionsEs, DefinitionsEn, Imagen, WordImagenes, Audio, WordAudio, Curso, Asignatura, WordModification
# from database.models.word import Word, DefinitionsEs, DefinitionsEn, Imagen, Audio, Curso, Asignatura, WordModification
from database.models.word import Word, DefinitionsEs, DefinitionsEn, Imagen, Audio, Curso, Asignatura
from typing import List, Optional

# --- Funciones auxiliares de verificación ---


async def existe_word(db: AsyncSession, word: str, lang: str) -> dict:
    """Verifica si una palabra ya existe en la base de datos (asíncrono)."""
    word = word.lower()
    palabra_encontrada = None
    if lang == "es":
        result = await db.execute(select(Word).where(Word.word_es == word))
        palabra_encontrada = result.scalar_one_or_none()
    elif lang == "en":
        result = await db.execute(select(Word).where(Word.word_en == word))
        palabra_encontrada = result.scalar_one_or_none()

    if palabra_encontrada:
        return {
            "word_en": palabra_encontrada.word_en,
            "word_es": palabra_encontrada.word_es,
            "lang": lang,
            "palabra_existente_db": True,
            "curso_id": palabra_encontrada.curso_id,
            "asignatura_id": palabra_encontrada.asignatura_id,
            # "definitions_es": [d.definicion for d in palabra_encontrada.definitions_es],
            # "definitions_en": [d.definicion for d in palabra_encontrada.definitions_en],
            # "images_url": [img.ruta_archivo for img in palabra_encontrada.imagenes],
            # "audios": [audio.ruta_archivo for audio in palabra_encontrada.audios],
        }
    else:
        return {
            "word_en": word,
            "lang": lang,
            "palabra_existente_db": False
        }

# def existe_word(db: Session, word: str, lang: str) -> Optional[Word]:
#     """Verifica si una palabra ya existe en la base de datos. Para eso tengo que identificar el idioma para hacer una consulta en la base de datos u otra"""

#     # Ponemos en minúscula la palabra para evitar problemas de comparación y evitar duplicados
#     word = word.lower()

#     # Verifica si el idioma es español o inglés
#     # y realiza la consulta correspondiente
#     palabra_encontrada = None
#     if lang == "es":
#         palabra_encontrada = db.query(Word).filter(
#             Word.word_es == word).first()
#     elif lang == "en":
#         palabra_encontrada = db.query(Word).filter(
#             Word.word_en == word).first()

#     if palabra_encontrada:
#         return {
#             # "original_word": word,
#             "word_en": palabra_encontrada.word_en,
#             "word_es": palabra_encontrada.word_es,
#             "original_language": lang,
#             "palabra_existente_db": True,
#             "curso_id": palabra_encontrada.curso_id,
#             "asignatura_id": palabra_encontrada.asignatura_id
#             # "definitions_es": [d.definicion for d in palabra_encontrada.definitions_es],
#             # "definitions_en": [d.definicion for d in palabra_encontrada.definitions_en],
#             # "images_url": [img.ruta_archivo for img in palabra_encontrada.imagenes],
#             # "audios": [audio.ruta_archivo for audio in palabra_encontrada.audios],
#         }
#     else:
#         return {
#             "word_en": word,
#             "original_language": lang,
#             "palabra_existente_db": False
#         }

#     return {'Message: "Error: No has seleccionado un idioma. Tienes que seleccionar:" "en" o "es".'}
#     # def existe_word_ortografia(db: Session, word_es: str, word_en: str) -> Optional[Word]:
#     # """Verifica si una palabra con la misma ortografía en español o inglés ya existe."""
#     # return db.query(Word).filter((Word.word_es == word_es) | (Word.word_en == word_en)).first()


def guardar_word_db(db: Session, word_es: str, word_en: str, curso_id: Optional[int] = None, asignatura_id: Optional[int] = None) -> Word:
    """Guarda una nueva palabra en la base de datos."""

    # Ponemos en minúscula la palabra para evitar problemas de comparación y evitar duplicados
    word_es = word_es.lower()
    word_en = word_en.lower()

    new_word = Word(
        word_es=word_es,
        word_en=word_en,
        curso_id=curso_id,
        asignatura_id=asignatura_id
    )
    db.add(new_word)
    db.commit()
    db.refresh(new_word)
    return new_word


def guardar_definiciones_db(db: Session, word_id: int, definitions_es: List[str], definitions_en: List[str]):
    """Guarda las definiciones en español e inglés para una palabra."""
    for def_es in definitions_es:
        new_definition_es = DefinitionsEs(word_id=word_id, definicion=def_es)
        db.add(new_definition_es)
    for def_en in definitions_en:
        new_definition_en = DefinitionsEn(word_id=word_id, definicion=def_en)
        db.add(new_definition_en)
    db.commit()


def guardar_imagenes_db(db: Session, word_id: int, url_images: List[str]):
    """Guarda las URLs de las imágenes y las asocia a la palabra."""
    for url in url_images:
        imagen_existente = db.query(Imagen).filter(
            Imagen.ruta_archivo == url).first()
        if not imagen_existente:
            new_imagen = Imagen(
                ruta_archivo=url, nombre_archivo=os.path.basename(url))
            db.add(new_imagen)
            db.commit()
            db.refresh(new_imagen)
            word_imagen = WordImagenes(
                word_id=word_id, imagen_id=new_imagen.id)
            db.add(word_imagen)
        else:
            # Asociar la imagen existente si no está ya asociada
            existing_association = db.query(WordImagenes).filter(
                WordImagenes.word_id == word_id, WordImagenes.imagen_id == imagen_existente.id).first()
            if not existing_association:
                word_imagen = WordImagenes(
                    word_id=word_id, imagen_id=imagen_existente.id)
                db.add(word_imagen)
    db.commit()


def guardar_audio_db(db: Session, word_id: int, url_audio: str):
    """Guarda la URL del audio y lo asocia a la palabra."""
    audio_existente = db.query(Audio).filter(
        Audio.ruta_archivo == url_audio).first()
    if not audio_existente:
        new_audio = Audio(ruta_archivo=url_audio,
                          nombre_archivo=os.path.basename(url_audio))
        db.add(new_audio)
        db.commit()
        db.refresh(new_audio)
        word_audio = WordAudio(word_id=word_id, audio_id=new_audio.id)
        db.add(word_audio)
    else:
        # Asociar el audio existente si no está ya asociada
        existing_association = db.query(WordAudio).filter(
            WordAudio.word_id == word_id, WordAudio.audio_id == audio_existente.id).first()
        if not existing_association:
            word_audio = WordAudio(
                word_id=word_id, audio_id=audio_existente.id)
            db.add(word_audio)
    db.commit()


def gestionar_guardado_word(
    db: Session,
    word_es: str,
    word_en: str,
    definitions_es: List[str],
    definitions_en: List[str],
    url_images: List[str],
    url_audio: str,
    curso_id: Optional[int] = None,
    asignatura_id: Optional[int] = None,
    carpeta_imagenes_destino: str = "imagenes_definitivas",
    carpeta_audios_destino: str = "audios_definitivos"
):
    """
    Función principal para verificar y guardar una palabra con sus datos asociados.
    También gestiona el guardado de imágenes y audios en carpetas definitivas.
    """
    word_existente = existe_word(db, word_es, word_en)

    if word_existente:
        print(
            f"La palabra '{word_es}' o '{word_en}' ya existe en la base de datos (ID: {word_existente.id}).")
        # Aquí podrías agregar lógica para actualizar la información si es necesario
    else:
        new_word = guardar_word_db(
            db, word_es, word_en, curso_id, asignatura_id)
        print(
            f"Se ha guardado la nueva palabra '{word_es}' (ID: {new_word.id}).")
        guardar_definiciones_db(
            db, new_word.id, definitions_es, definitions_en)
        guardar_imagenes_db(db, new_word.id, url_images)
        guardar_audio_db(db, new_word.id, url_audio)

        # Aquí iría la lógica para mover/descargar imágenes y audios a las carpetas definitivas

    print("Proceso de guardado de la palabra completado.")
