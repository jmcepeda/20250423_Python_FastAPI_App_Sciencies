import os
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.database import get_db
# from database.models.word import Word, DefinitionsEs, DefinitionsEn, Imagen, WordImagenes, Audio, WordAudio, Curso, Asignatura, WordModification
# from database.models.word import Word, DefinitionsEs, DefinitionsEn, Imagen, Audio, Curso, Asignatura, WordModification
from database.models.word import Word, DefinitionsEs, DefinitionsEn, Imagen, Audio, Curso, Asignatura
from typing import List, Optional
from fastapi import HTTPException

# --- Funciones auxiliares de verificación ---


async def existe_word(db: AsyncSession, word: str, lang: str, temporal: bool = False) -> dict:
    """Verifica si una palabra ya existe en la base de datos (asíncrono)."""
    word = word.lower()

    palabra_encontrada = None
    if lang == "es":
        if temporal:
            result = await db.execute(select(Word).where(Word.word_es == word, Word.campo_temporal == True))
        else:
            result = await db.execute(select(Word).where(Word.word_es == word, Word.campo_temporal == False))
        palabra_encontrada = result.scalar_one_or_none()
    elif lang == "en":
        if temporal:
            result = await db.execute(select(Word).where(Word.word_en == word, Word.campo_temporal == True))
        else:
            result = await db.execute(select(Word).where(Word.word_en == word, Word.campo_temporal == False))
        palabra_encontrada = result.scalar_one_or_none()
    else:
        raise HTTPException(
            status_code=400, detail="Error: No has seleccionado un idioma. Tienes que seleccionar: 'en' o 'es'.")

    print(
        f"Acabamos de Comprobar si la Palabra existe en la Base de Datos: {word}")
    # print(f"{palabra_encontrada}")

    if palabra_encontrada:
        print(
            f"La palabra '{word}' ya existe en la base de datos (ID: {palabra_encontrada.id}).")
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
        print(f"La palabra '{word}' NO existe en la base de datos.")
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


async def guardar_word_db(db: AsyncSession, created_by: int, word_en: str, word_es: str, curso_id: Optional[int] = None, asignatura_id: Optional[int] = None, temporal: bool = False) -> Word:
    # async def guardar_word_db(db: AsyncSession, created_by: int, word_en: str, curso_id: Optional[int] = None, asignatura_id: Optional[int] = None, temporal: bool = False) -> Word:
    """Guarda una nueva palabra en la base de datos."""

    # Ponemos en minúscula la palabra para evitar problemas de comparación y evitar duplicados
    print("Guardando la palabra en la base de datos... Desde la función guardar_word_db")
    word_es_lower = word_es.lower()
    word_en_lower = word_en.lower()

    new_word = Word(
        created_by=created_by,
        word_es=word_es_lower,
        word_en=word_en_lower,
        curso_id=curso_id,
        asignatura_id=asignatura_id,
        campo_temporal=temporal
    )
    db.add(new_word)
    try:
        # --- AÑADIR await ---
        await db.commit()
        print(f"Commit realizado para: {word_en_lower}")
        # --- AÑADIR await ---
        await db.refresh(new_word)
        print(f"Objeto refrescado, ID obtenido: {new_word.id}")
        return new_word
    except Exception as e:
        # --- AÑADIR await ---
        await db.rollback()
        print(f"Error al guardar la palabra '{word_en_lower}' en la BD: {e}")
        # Considera relanzar el error de forma adecuada para FastAPI

        # print(new_word_sqlalchemy_obj) # Esto podría estar intentando cargar relaciones lazy-loaded síncronamente

        # return JSONResponse(status_code=201, content={"message": f"Palabra '{word_es}' añadida exitosamente con ID: {new_word_sqlalchemy_obj.id}", "word_id": new_word_sqlalchemy_obj.id})
        raise HTTPException(
            status_code=500, detail=f"Error al guardar en base de datos: {e}") from e


async def guardar_definiciones_db(db: AsyncSession, word_id: int, definitions_es: List[str], definitions_en: List[str]):
    """Guarda las definiciones en español e inglés para una palabra."""
    for def_es in definitions_es:
        new_definition_es = DefinitionsEs(word_id=word_id, definicion=def_es)
        db.add(new_definition_es)
    for def_en in definitions_en:
        new_definition_en = DefinitionsEn(word_id=word_id, definicion=def_en)
        db.add(new_definition_en)
    db.commit()


def guardar_imagenes_db(db: AsyncSession, word_id: int, url_images: List[str]):
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


def guardar_audio_db(db: AsyncSession, word_id: int, url_audio: str):
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
    db: AsyncSession,
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
            db, word_es, word_en, curso_id, asignatura_id, False)
        print(
            f"Se ha guardado la nueva palabra '{word_es}' (ID: {new_word.id}).")
        guardar_definiciones_db(
            db, new_word.id, definitions_es, definitions_en)
        guardar_imagenes_db(db, new_word.id, url_images)
        guardar_audio_db(db, new_word.id, url_audio)

        # Aquí iría la lógica para mover/descargar imágenes y audios a las carpetas definitivas

    print("Proceso de guardado de la palabra completado.")
