import asyncio
import os
import aiohttp
import json

# No hay alternativas asíncronas directas para googletrans o deep_translator conocidas
from googletrans import Translator as GoogleTranslatorSync
from deep_translator import GoogleTranslator as DeepTranslatorSync

# No hay una alternativa asíncrona directa para gTTS conocida
from gtts import gTTS as gTTSSync


async def async_translate_word(word, source, target):
    try:
        # Ejecutar la función síncrona en un hilo para no bloquear
        translation = await asyncio.to_thread(translate_word_sync, word, source, target)
        return translation
    except Exception as e:
        print(f"Error al traducir asíncronamente: {e}")
        return None


def translate_word_sync(word, source='en', target='es'):
    """Función síncrona para ser ejecutada en un hilo."""
    try:
        translator = DeepTranslatorSync(source=source, target=target)
        translator.engine = 'google'
        translation = translator.translate(word)
        return translation
    except Exception as e:
        print(f"Error al traducir (síncrono): {e}")
        return None


async def async_translate_definitions(definitions, source, target='es'):
    translations = await asyncio.gather(
        *(asyncio.to_thread(translate_definition_sync, definition, source, target) for definition in definitions)
    )
    return translations


def translate_definition_sync(definition, source, target):
    """Función síncrona para traducir una definición."""
    try:
        translator = DeepTranslatorSync(source=source, target=target)
        translator.engine = 'google'
        translation = translator.translate(definition)
        return translation
    except Exception as e:
        print(f"Error al traducir definición (síncrono): {e}")
        return None


async def async_get_english_definitions(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and 'meanings' in data[0]:
                        definitions = [meaning['definitions'][0]['definition']
                                       for meaning in data[0]['meanings']]
                        return definitions
                else:
                    print(f"Error {response.status}: {await response.text()}")
                    return ["No encontrada ninguna definición."]
        except aiohttp.ClientError as e:
            print(f"Error de cliente HTTP: {e}")
            return "No encontrada ninguna definición."


async def async_get_spanish_definitions(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/es/{word}"
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data and 'meanings' in data[0]:
                        definitions = [meaning['definitions'][0]['definition']
                                       for meaning in data[0]['meanings']]
                        return definitions
                else:
                    print(f"Error {response.status}: {await response.text()}")
                    return ["No encontrada ninguna definición ."]
        except aiohttp.ClientError as e:
            print(f"Error de cliente HTTP: {e}")
            return "No encontrada ninguna definición."


async def async_get_pronunciation(word, lang='en'):
    try:
        file_name = await asyncio.to_thread(get_pronunciation_sync, word, lang)
        return file_name
    except Exception as e:
        print(f"Error al obtener pronunciación asíncrona: {e}")
        return None


def get_pronunciation_sync(word, lang='en'):
    """Función síncrona para generar la pronunciación."""
    tts = gTTSSync(text=word, lang=lang)
    os.makedirs("./audios", exist_ok=True)
    file_name = f"./audios/{word}.mp3"
    tts.save(file_name)
    print(
        f"El archivo de pronunciación {file_name} se ha guardado correctamente.")
    return file_name


async def async_get_images_unsplash(query):
    access_key = "mA3-OSHmrABENGeRSnjBQKJK6lDyNT-ISlroW23TzzA"
    url = f"https://api.unsplash.com/search/photos"
    params = {
        'query': query,
        'page': 1,
        'per_page': 12
    }
    headers = {
        'Authorization': f'Client-ID {access_key}'
    }
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    results = data['results']
                    image_urls = [result['urls']['regular']
                                  for result in results]
                    return image_urls
                else:
                    print(f"Error {response.status}: {await response.text()}")
                    return []
        except aiohttp.ClientError as e:
            print(f"Error de cliente HTTP: {e}")
            return []


async def async_download_image(url, folder, file_name):
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    os.makedirs(folder, exist_ok=True)
                    file_path = os.path.join(folder, file_name)
                    with open(file_path, 'wb') as file:
                        async for chunk in response.content.iter_chunked(1024):
                            file.write(chunk)
                    print(f"Imagen descargada: {file_path}")
                else:
                    print(f"Error al descargar la imagen: {response.status}")
        except aiohttp.ClientError as e:
            print(f"Excepción al descargar la imagen: {e}")

# Ejemplo de cómo ejecutar las funciones asíncronas


async def main():
    word = "book"
    spanish_translation = await async_translate_word(word)
    print(f"Traducción de '{word}': {spanish_translation}")

    definitions = await async_get_english_definitions(word)
    if definitions:
        spanish_definitions = await async_translate_definitions(definitions)
        print(f"Definiciones en inglés: {definitions}")
        print(f"Definiciones en español: {spanish_definitions}")

    pronunciation_file = await async_get_pronunciation(word)
    if pronunciation_file:
        print(f"Archivo de pronunciación guardado en: {pronunciation_file}")

    image_urls = await async_get_images_unsplash(word)
    print(f"URLs de imágenes de '{word}': {image_urls}")
    if image_urls:
        await async_download_image(image_urls[0], "images", f"{word}_1.jpg")

if __name__ == "__main__":
    asyncio.run(main())
