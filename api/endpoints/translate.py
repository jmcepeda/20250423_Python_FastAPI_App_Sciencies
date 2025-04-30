from utils.schemas import WordCreateRequest, WordResponse
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from nltk.corpus import wordnet
from nltk.corpus import words
import nltk
from fastapi import APIRouter, Query, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from typing import Optional, List
import os
# from utils import (
from utils.utils import (
    async_translate_word,
    async_get_english_definitions,
    async_get_spanish_definitions,
    async_translate_definitions,
    async_get_pronunciation,
    async_get_images_unsplash,
)
from .auth import get_current_user, get_current_user_test
from models.user import User
from utils.lectura_escritura import existe_word, guardar_word_db
import os
# import enchant
import asyncio
from utils.gemini_api import async_generate_improved_definition, async_generate_improved_translate
from utils.calculo_curso import get_curso_and_asignatura_id

from datetime import datetime

# from PyDictionary import PyDictionary


router = APIRouter()
age: Optional[int] = 15


try:
    nltk.data.find('corpora/words')
except nltk.downloader.DownloadError:
    nltk.download('words')

english_words = set(words.words('en'))
# There isn't a direct 'es' argument that guarantees a comprehensive Spanish list.
# The default 'words' might contain some Spanish.
# all_words = set(words.words()) # Load all words and check if present (less efficient)


def es_palabra_ingles(word: str):
    return word.lower() in english_words

# def es_palabra_espanol(word:str):
#     try:
#         spanish_words_corpus = set(words.words('es'))
#         return word.lower() in spanish_words_corpus
#     except LookupError:
#         print("Spanish words corpus not found. You might need to download it.")
#         return False

# print(f"'hello' is English: {es_palabra_ingles('hello')}")
# print(f"'Hola' is Spanish: {es_palabra_espanol('Hola')}")
# print(f"'blorf' is English: {es_palabra_ingles('blorf')}")
# print(f"'zutano' is Spanish: {es_palabra_espanol('zutano')}")


# def es_palabra_espanol(word: str) -> bool:
#     diccionario_es = enchant.Dict("es")
#     return diccionario_es.check(word)

# def es_palabra_ingles(word: str) -> bool:
#     diccionario_en = enchant.Dict("en")
#     return diccionario_en.check(word)


def validate_language(word: str, lang: str) -> bool:
    if lang == 'es':
        return True
    elif lang == 'en':
        return es_palabra_ingles(word)
    return False

# Ruta de Prueba CON Verificación de usuario
# @router.get("/translate", dependencies=[Depends(get_current_user)]) # Ejemplo de ruta protegida

# Ruta de Prueba SIN Verificación de usuario


@router.get("/translate")
async def translate_api(
    word: str = Query(..., description="Palabra a traducir"),
    lang: str = Query(..., description="Idioma de la palabra ('es' o 'en')"),
    db: AsyncSession = Depends(get_db)
):
    """
    Traduce una palabra y devuelve su información, verificando primero si existe en la base de datos.
    """

    if not lang in ['es', 'en']:
        raise HTTPException(
            status_code=400, detail="Las Palabras deben ser en alguno de estos dos idiomas: 'es' (Español) o 'en' (Inglés).")

    idioma_correcto: bool = validate_language(word, lang)

    print("Palabra Original a Traducir:", word, ". Idioma Original:", lang)
    print("Idioma Correcto:", idioma_correcto)

    # <--- ¡VERIFICA ESTA LÍNEA!
    word_existente_db = await existe_word(db, word=word, lang=lang)

    print(word_existente_db)
    # word_existente_db = await existe_word(db, word=word, lang=lang)

    print(word_existente_db)
    print("Palabra existente en DB:",
          word_existente_db["palabra_existente_db"])
    print("Palabra WORD:", word_existente_db["word_en"])
    print("Palabra WORD:", word_existente_db["lang"])

    if word_existente_db["palabra_existente_db"] == True:
        respuesta = {
            # 'original_word': word,
            # 'original_language': lang,
            # 'translated_word': translated_word_arr,
            # 'pronunciation_lang': 'en',
            # 'translated_language': translated_language,
            # 'definitions': {
            #     'en': english_definitions_def,
            #     'es': spanish_definitions_def,
            # },
            # 'definitions_improved': {
            #     'en': english_improved_definitions,
            #     'es': spanish_improved_definitions,
            # },

            # 'pronunciation_url': word_existente_dbpronunciation_url,
            # 'image_urls': images,
            'word_existente_db': word_existente_db["palabra_existente_db"],
            # "existe_en_db": True,
            "word_es": word_existente_db["word_es"],
            "word_en": word_existente_db["word_en"],
            # "definitions_es": [d.definicion for d in word_existente_db.definiciones_es],
            # "definitions_en": [d.definicion for d in word_existente_db.definiciones_en],
            # "images_url": [img.ruta_archivo for img in word_existente_db.imagenes],
            # "audios": [audio.ruta_archivo for audio in word_existente_db.audios],
            # "edad_minima": palabra_existente_db.edad_minima,
            # "edad_maxima": palabra_existente_db.edad_maxima,
            "curso_id": word_existente_db["curso_id"],
            "asignatura_id": word_existente_db["asignatura_id"],
        }
        return respuesta
    else:

        print("Empezando la traducción...")

        # if not validate_language(word, lang):
        if not idioma_correcto:
            idioma = 'Español' if lang == 'es' else 'Inglés'
            raise HTTPException(
                status_code=400, detail=f"La palabra introducida '{word}' no parece ser una palabra válida para el idioma '{lang}' ({idioma}). Recuerda que las palabras deben ser en inglés.")

        translated_word: str = ''
        spannish_word: str = ''
        english_word: str = ''

        if (lang == 'es' and idioma_correcto) or (lang == 'en' and not idioma_correcto):
            translated_word = await async_translate_word(word, source='es', target='en')
            pronunciation_lang = 'es'
            spanish_word = word
            english_improved_translated = await async_generate_improved_translate(word, "en", age)
            # english_word = translated_word
            english_word = english_improved_translated
            translated_word_arr = [
                english_improved_translated, translated_word]
            print("Palabra Traducida:", translated_word)
            print("Palabra Traducida Mejorada:", english_word)

        # else:  # lang == 'en'
        elif (lang == 'en' and idioma_correcto) or (lang == 'es' and not idioma_correcto):
            translated_word = await async_translate_word(word, source='en', target='es')
            pronunciation_lang = 'en'
            spanish_improved_translated = await async_generate_improved_translate(word, "es", age)
            spanish_word = spanish_improved_translated
            english_word = word
            translated_word_arr = [
                spanish_improved_translated, translated_word]
            print("Palabra Traducida:", translated_word)
            print("Palabra Traducida Mejorada:", spanish_improved_translated)

        if (lang == 'es' and idioma_correcto) or (lang == 'en' and not idioma_correcto):
            # spanish_definitions = await async_get_spanish_definitions(spanish_word)
            # english_definitions = await async_translate_definitions(spanish_definitions, source='es', target='en') if spanish_definitions else []

            # dictionary = PyDictionary()
            # dictionary = PyDictionary.PyDictionary()
            # english_definitions = dictionary.meaning(english_word)

            synsets_english = wordnet.synsets(
                english_word, pos='n')  # Obtener solo los sustantivos

            english_definitions = []  # Inicializamos una lista vacía para guardar las definiciones

            for synset in synsets_english:
                definicion = synset.definition()  # Obtenemos la definición del synset
                # Añadimos la definición al array
                english_definitions.append(definicion)

            # print(definiciones_array)

            spanish_definitions = await async_translate_definitions(english_definitions, source='en', target='es') if english_definitions else []
            # spanish_definitions = await async_translate_definitions(english_definitions, 'es')
            # pronunciation_lang = 'en'
            translated_language = 'en'
        elif (lang == 'es' and not idioma_correcto) or (lang == 'en' and idioma_correcto):  # lang == 'en'
            # english_definitions = await async_get_english_definitions(english_word)
            # dictionary = PyDictionary()
            # english_definitions = dictionary.me∫aning(english_word)

            synsets_english = wordnet.synsets(
                english_word, pos='n')  # Obtener solo los sustantivos

            english_definitions = []  # Inicializamos una lista vacía para guardar las definiciones

            for synset in synsets_english:
                definicion = synset.definition()  # Obtenemos la definición del synset
                # Añadimos la definición al array
                english_definitions.append(definicion)

            # print(definiciones_array)

            # english_definitions = wordnet.synsets(english_word)
            spanish_definitions = await async_translate_definitions(english_definitions, source='en', target='es') if english_definitions else []
            # pronunciation_lang = 'en'
            translated_language = 'es'
            # spanish_definitions = []
        else:
            spanish_definitions = []
            english_definitions = []
            pronunciation_lang = ''
            translated_language = ''
            spanish_word = ''
            english_word = ''

        # english_definitions = await async_get_english_definitions(word)
        # spanish_definitions = await async_translate_definitions(
        #     english_definitions, target='es') if english_definitions else []

    spanish_improved_definitions: list[str] = []
    if spanish_definitions:
        tasks = [async_generate_improved_definition(
            spanish_word, "es", age) for definition in spanish_definitions]
        spanish_improved_definitions = await asyncio.gather(*tasks)

    print("Definiciones originales en español:", spanish_definitions)
    print("Definiciones mejoradas:", spanish_improved_definitions)
    spanish_definitions_def = spanish_improved_definitions+spanish_definitions
    print("Definiciones totales en español:", spanish_definitions)

    english_improved_definitions: list[str] = []
    if english_definitions:
        tasks = [async_generate_improved_definition(
            english_word, "en", age) for definition in english_definitions]
        english_improved_definitions = await asyncio.gather(*tasks)

    print("Definiciones originales en ingles:", english_definitions)
    print("Definiciones mejoradas:", english_improved_definitions)
    english_definitions_def = english_improved_definitions+english_definitions
    print("Definiciones totales en ingles:", english_definitions)

    # images = await async_get_images_unsplash(word if lang == 'en' else translated_word)
    images = await async_get_images_unsplash(spanish_word + " - " + english_word)

    # Archivo de Pronunciación
    pronunciation_file = await async_get_pronunciation(english_word, lang='en')
    pronunciation_url = f'/audio/{os.path.basename(pronunciation_file)}' if pronunciation_file and os.path.exists(
        pronunciation_file) else None

    return JSONResponse(content={
        'original_word': word,
        'original_language': lang,
        'translated_word': translated_word_arr,
        'pronunciation_lang': 'en',
        'translated_language': translated_language,
        'definitions': {
            'en': english_definitions_def,
            'es': spanish_definitions_def,
        },
        'definitions_improved': {
            'en': english_improved_definitions,
            'es': spanish_improved_definitions,
        },
        'pronunciation_url': pronunciation_url,
        'image_urls': images,
        'palabra_existente_db': True
    })
    # else:


# Endpoint para servir archivos de audio


@router.get("/audio/{filename}")
async def serve_audio(filename: str):
    audio_dir = os.path.join(os.getcwd(), 'audios')
    filename = filename + ".mp3"
    file_path = os.path.join(audio_dir, filename)
    print("File Path:", file_path)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio no encontrado")
    # return FileResponse(file_path)
    return FileResponse(file_path, media_type="audio/mpeg")


@router.post("/words", dependencies=[Depends(get_current_user_test)])
async def add_new_word(
    # word_es: str,
    # word_en: str,
    # username: str,  # Espera el username en el cuerpo de la petición
    word_data: WordCreateRequest,  # <- Recibes todo en un objeto
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user_test),  # Usa la nueva función
):
    # print(
    # f"Token recibido (no validado): {credentials.credentials if (credentials := Depends(bearer_scheme)) else None}")
    print(current_user)
    # print(
    # f"Usuario (Username: {current_user['username']} Existente en DB: {current_user['usuario_existente_db']})")
    print(
        f"Usuario (Username: {current_user.username} Existente en DB: {current_user.usuario_existente_db})")

    # formato = "%Y-%m-%d"  # Código de formato para YYYY-MM-DD
    date = word_data.birthdate
    try:
        # .date() si solo quieres la fecha
        # objeto_fecha = datetime.strptime(date_str, formato).date()
        # year_nacimiento = objeto_fecha.year
        year_nacimiento = date.year
        # print(f"Fecha como objeto date: {objeto_fecha}")
        print(f"El año es: {year_nacimiento}")  # Salida: El año es: 2024
    except ValueError:
        print("El formato de la fecha no coincide.")
    # word_existente = existe_word(db, word_es=word_es, word_en=word_en)
    # {curso_id, asignatura_id} = word_data.curso_id, word_data.asignatura_id
    # {curso_id, asignatura_id} = get_curso_and_asignatura_id(year_nacimiento, 0, "Sciencies", db)
    # response_curso_asignatura = await get_curso_and_asignatura_id(
    #     year_nacimiento, 0, "Sciencies", db)
    response_curso_asignatura = await get_curso_and_asignatura_id(
        year_nacimiento, 0, word_data.asignatura, db)

    # curso_id = response_curso_asignatura.get("curso_id")
    # curso_id = response_curso_asignatura["curso_id"]
    # asignatura_id = response_curso_asignatura.get("asignatura_id")

    curso_id = response_curso_asignatura["curso_id"]
    asignatura_id = response_curso_asignatura["asignatura_id"]

    # Fíjate también en await
    word_existente = await existe_word(db, word_data.word_en, word_data.lang)

    if word_existente['palabra_existente_db']:
        raise HTTPException(
            status_code=400, detail="Esta palabra ya existe en la base de datos.")

    print("Desde Función POST API Translate: Curso ID:", curso_id)
    print("Desde Función POST API Translate: Asignatura ID:", asignatura_id)
    # new_word = guardar_word_db(db, created_by=current_user.id, word_es=word_data.word_en.lower(
    # ), word_en=word_data.word_en.lower(), curso_id=word_data.curso_id, asignatura_id=word_data.asignatura_id)
    new_word_sqlalchemy_obj = await guardar_word_db(db, created_by=current_user.id, word_es=word_data.word_es.lower(
    ), word_en=word_data.word_en.lower(), curso_id=curso_id, asignatura_id=asignatura_id)
    # print(new_word_sqlalchemy_obj)
    response_data = WordResponse.model_validate(new_word_sqlalchemy_obj)
    print(response_data)
    # return JSONResponse(content=new_word)
    return response_data
