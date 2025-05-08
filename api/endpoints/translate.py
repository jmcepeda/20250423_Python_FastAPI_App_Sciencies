from utils.schemas import WordCreateRequest, WordResponse
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from nltk.corpus import wordnet
from nltk.corpus import words
import nltk
from nltk.corpus import wordnet
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
from utils.gemini_api import async_generate_improved_definition, async_generate_improved_translate, async_generate_frase_ejemplo
from utils.calculo_curso import get_curso_and_asignatura_id

from datetime import datetime

# from PyDictionary import PyDictionary


router = APIRouter()
age: Optional[int] = 15


# Descarga de recursos NLTK
try:
    nltk.data.find('corpora/words')
    print("Recurso NLTK 'corpora/words' encontrado.")
except LookupError:  # CAMBIO AQUÍ: de nltk.downloader.DownloadError a LookupError
    print("Recurso NLTK 'corpora/words' no encontrado. Intentando descargar...")
    nltk.download('words')

try:
    nltk.data.find('corpora/omw-1.4')  # Open Multilingual Wordnet
    print("Recurso NLTK 'corpora/omw-1.4' encontrado.")
except LookupError:  # CAMBIO AQUÍ: de nltk.downloader.DownloadError a LookupError
    print("Recurso NLTK 'corpora/omw-1.4' no encontrado. Intentando descargar...")
    nltk.download('omw-1.4')

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


@router.get("/translate", dependencies=[Depends(get_current_user_test)])
async def translate_api(
    word_data: WordCreateRequest,
    # word: str = Query(..., description="Palabra a traducir"),
    # lang: str = Query(..., description="Idioma de la palabra ('es' o 'en')"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(
        get_current_user_test)
):
    """
    Traduce una palabra y devuelve su información, verificando primero si existe en la base de datos.
    """
    word = word_data.word_en.lower()
    lang = word_data.lang.lower()
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
        print("Palabra existente en DB:",
              word_existente_db["palabra_existente_db"])
        print(word_existente_db)
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
        translated_word_arr = []

        if (lang == 'es' and idioma_correcto) or (lang == 'en' and not idioma_correcto):
            translated_word = await async_translate_word(word, source='es', target='en')
            pronunciation_lang = 'es'
            spanish_word = word.lower()
            english_improved_translated = await async_generate_improved_translate(word, "en", age)
            # english_word = translated_word
            english_word = english_improved_translated.lower()
            translated_word_arr = [
                english_improved_translated.lower(), translated_word.lower()]
            print("Palabra Traducida:", translated_word)
            print("Palabra Traducida Mejorada:", english_word)

        # else:  # lang == 'en'
        elif (lang == 'en' and idioma_correcto) or (lang == 'es' and not idioma_correcto):
            translated_word = await async_translate_word(word, source='en', target='es')
            pronunciation_lang = 'en'
            spanish_improved_translated = await async_generate_improved_translate(word, "es", age)
            spanish_word = spanish_improved_translated.lower()
            english_word = word.lower()
            translated_word_arr = [
                spanish_improved_translated.lower(), translated_word.lower()]
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
        try:
            images = await async_get_images_unsplash(spanish_word + " - " + english_word)
        except Exception as e:
            print("Error al obtener imágenes de Unsplash:", e)
            raise HTTPException(
                status_code=500, detail="Error al obtener imágenes de Unsplash."
            ) from e

        # Archivo de Pronunciación
        pronunciation_file = await async_get_pronunciation(english_word, lang='en')
        pronunciation_url = f'/00_audios/temporales/{os.path.basename(pronunciation_file)}' if pronunciation_file and os.path.exists(
            pronunciation_file) else None

        # Vamos a definir una lista con frases de ejemplo en inglés las que se usa la palabra
        try:
            sentence_example = await async_generate_frase_ejemplo(
                english_word, "en", age)
        except Exception as e:
            print("Error al generar la frase de ejemplo:", e)
            raise HTTPException(
                status_code=500, detail="Error al generar la frase de ejemplo."
            ) from e

        # sentences_example_english = set()  # 1. Se inicializa un conjunto vacío

        # # 2. Se itera sobre todos los significados (synsets) de la 'palabra'
        # for synset in wordnet.synsets(english_word, lang='eng'):
        #     # 3. Para cada significado, se obtienen sus frases de ejemplo
        #     for ejemplo in synset.examples():
        #         # 4. Cada frase de ejemplo se añade al conjunto
        #         sentences_example_english.add(ejemplo)

        # # 5. Se devuelve el conjunto convertido a lista
        # list_sentences_example_english = list(sentences_example_english)

     # Almacenamos la palabra en la base de datos
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
        try:
            response_curso_asignatura = await get_curso_and_asignatura_id(
                year_nacimiento, 0, word_data.asignatura, db)
        except Exception as e:
            print("Error al obtener el curso y asignatura:", e)
            raise HTTPException(
                status_code=500, detail="Error al obtener el curso y asignatura."
            ) from e
        # curso_id = response_curso_asignatura.get("curso_id")
        # curso_id = response_curso_asignatura["curso_id"]
        # asignatura_id = response_curso_asignatura.get("asignatura_id")

        curso_id = response_curso_asignatura["curso_id"]
        asignatura_id = response_curso_asignatura["asignatura_id"]

        # Fíjate también en await
        print("Desde Función POST API Word: Vamos a comprobar si la palabra ya existe en la base de datos.")
        try:
            word_existente = await existe_word(db, word_data.word_en, word_data.lang)
        except Exception as e:
            print("Error al comprobar si la palabra existe en la base de datos:", e)
            raise HTTPException(
                status_code=500, detail="Error al comprobar si la palabra existe en la base de datos."
            ) from e

        if word_existente['palabra_existente_db']:
            raise HTTPException(
                status_code=400, detail="Esta palabra ya existe en la base de datos. Que no te enteras contreras.")

        print("Desde Función POST API Translate: Curso ID:", curso_id)
        print("Desde Función POST API Translate: Asignatura ID:", asignatura_id)
        # new_word = guardar_word_db(db, created_by=current_user.id, word_es=word_data.word_en.lower(
        # ), word_en=word_data.word_en.lower(), curso_id=word_data.curso_id, asignatura_id=word_data.asignatura_id)
        try:
            # new_word_sqlalchemy_obj = await guardar_word_db(db, created_by=current_user.id, word_es=word_data.word_es.lower(
            # ), word_en=word_data.word_en.lower(), curso_id=curso_id, asignatura_id=asignatura_id, temporal=False)
            new_word_sqlalchemy_obj = await guardar_word_db(db, created_by=current_user.id, word_es=spanish_word.lower(
            ), word_en=english_word.lower(), curso_id=curso_id, asignatura_id=asignatura_id, temporal=False)
        except Exception as e:
            print("Error al guardar la palabra en la base de datos:", e)
            raise HTTPException(
                status_code=500, detail="Error al guardar la palabra en la base de datos."
            ) from e
        # Ahora hay que guardar las definiciones y traducciones en la base de datos

        # También hay que guardar las imagenes en la base de datos

        # Por Último hay que guardar el audio en la base de datos

    # print(new_word_sqlalchemy_obj)
    response_data = WordResponse.model_validate(new_word_sqlalchemy_obj)

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
        'sentences_example_english': sentence_example,
        'pronunciation_url': pronunciation_url,
        'image_urls': images,
        'word_existente_db': False,
        'word_insertada_db': True,
        'usuario_existente_db': current_user.usuario_existente_db,
        'user_id': current_user.id,
        'user_username': current_user.username,
        'user_firstname': current_user.firstname,
        'user_lastname': current_user.lastname,
        'user_email': current_user.email,
        'user_wordpress_id': current_user.wordpress_id,
        'curso_id': curso_id,
        'asignatura_id': asignatura_id
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
    try:
        response_curso_asignatura = await get_curso_and_asignatura_id(
            year_nacimiento, 0, word_data.asignatura, db)
    except Exception as e:
        print("Error al obtener el curso y asignatura:", e)
        raise HTTPException(
            status_code=500, detail="Error al obtener el curso y asignatura."
        ) from e
    # curso_id = response_curso_asignatura.get("curso_id")
    # curso_id = response_curso_asignatura["curso_id"]
    # asignatura_id = response_curso_asignatura.get("asignatura_id")

    curso_id = response_curso_asignatura["curso_id"]
    asignatura_id = response_curso_asignatura["asignatura_id"]

    # Fíjate también en await
    print("Desde Función POST API Word: Vamos a comprobar si la palabra ya existe en la base de datos.")
    try:
        word_existente = await existe_word(db, word_data.word_en, word_data.lang)
    except Exception as e:
        print("Error al comprobar si la palabra existe en la base de datos:", e)
        raise HTTPException(
            status_code=500, detail="Error al comprobar si la palabra existe en la base de datos."
        ) from e

    if word_existente['palabra_existente_db']:
        raise HTTPException(
            status_code=400, detail="Esta palabra ya existe en la base de datos. Que no te enteras contreras.")

    print("Desde Función POST API Translate: Curso ID:", curso_id)
    print("Desde Función POST API Translate: Asignatura ID:", asignatura_id)
    # new_word = guardar_word_db(db, created_by=current_user.id, word_es=word_data.word_en.lower(
    # ), word_en=word_data.word_en.lower(), curso_id=word_data.curso_id, asignatura_id=word_data.asignatura_id)
    try:
        new_word_sqlalchemy_obj = await guardar_word_db(db, created_by=current_user.id, word_es=word_data.word_es.lower(
        ), word_en=word_data.word_en.lower(), curso_id=curso_id, asignatura_id=asignatura_id, temporal=True)
    except Exception as e:
        print("Error al guardar la palabra en la base de datos:", e)
        raise HTTPException(
            status_code=500, detail="Error al guardar la palabra en la base de datos."
        ) from e

    # print(new_word_sqlalchemy_obj)
    response_data = WordResponse.model_validate(new_word_sqlalchemy_obj)
    print(response_data)
    # return JSONResponse(content=new_word)
    return response_data
