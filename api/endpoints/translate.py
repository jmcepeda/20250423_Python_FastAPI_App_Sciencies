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
from .auth import get_current_user
from models.user import User
import os
import enchant
import asyncio
from utils.gemini_api import async_generate_improved_definition, async_generate_improved_translate

router = APIRouter()
age: Optional[int] = 15


def es_palabra_espanol(word: str) -> bool:
    diccionario_es = enchant.Dict("es")
    return diccionario_es.check(word)


def es_palabra_ingles(word: str) -> bool:
    diccionario_en = enchant.Dict("en")
    return diccionario_en.check(word)


def validate_language(word: str, lang: str) -> bool:
    if lang == 'es':
        return es_palabra_espanol(word)
    elif lang == 'en':
        return es_palabra_ingles(word)
    return False

# Ruta de Prueba CON Verificación de usuario
# @router.get("/translate", dependencies=[Depends(get_current_user)]) # Ejemplo de ruta protegida

# Ruta de Prueba SIN Verificación de usuario


@router.get("/translate")
async def translate_api(
    word: str = Query(..., description="Palabra a traducir"),
    lang: str = Query(..., description="Idioma de la palabra ('es' o 'en')")
):
    if not lang in ['es', 'en']:
        raise HTTPException(
            status_code=400, detail="Las Palabras deben ser en alguno de estos dos idiomas: 'es' (Español) o 'en' (Inglés).")

    idioma_correcto: bool = validate_language(word, lang)

    print("Palabra Original a Traducir:", word, ". Idioma Original:", lang)
    print("Idioma Correcto:", idioma_correcto)

    # if not validate_language(word, lang):
    if not idioma_correcto:
        idioma = 'Español' if lang == 'es' else 'Inglés'
        raise HTTPException(
            status_code=400, detail=f"La palabra introducida '{word}' no parece ser una palabra válida para el idioma '{lang}' ({idioma}).")

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
        translated_word_arr = [english_improved_translated, translated_word]
        print("Palabra Traducida:", translated_word)
        print("Palabra Traducida Mejorada:", english_word)

    # else:  # lang == 'en'
    elif (lang == 'en' and idioma_correcto) or (lang == 'es' and not idioma_correcto):
        translated_word = await async_translate_word(word, source='en', target='es')
        pronunciation_lang = 'en'
        spanish_improved_translated = await async_generate_improved_translate(word, "es", age)
        spanish_word = spanish_improved_translated
        english_word = word
        translated_word_arr = [spanish_improved_translated, translated_word]
        print("Palabra Traducida:", translated_word)
        print("Palabra Traducida Mejorada:", spanish_improved_translated)

    if (lang == 'es' and idioma_correcto) or (lang == 'en' and not idioma_correcto):
        spanish_definitions = await async_get_spanish_definitions(spanish_word)
        english_definitions = await async_translate_definitions(spanish_definitions, source='es', target='en') if spanish_definitions else []
        # spanish_definitions = await async_translate_definitions(english_definitions, 'es')
        # pronunciation_lang = 'en'
        translated_language = 'en'
    elif (lang == 'es' and not idioma_correcto) or (lang == 'en' and idioma_correcto):  # lang == 'en'
        english_definitions = await async_get_english_definitions(english_word)
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
    pronunciation_file = await async_get_pronunciation(english_word, lang=pronunciation_lang)
    pronunciation_url = f'/audio/{os.path.basename(pronunciation_file)}' if pronunciation_file and os.path.exists(
        pronunciation_file) else None

    return JSONResponse(content={
        'original_word': word,
        'original_language': lang,
        'translated_word': translated_word_arr,
        'pronunciation_lang': pronunciation_lang,
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
        'image_urls': images
    })

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
