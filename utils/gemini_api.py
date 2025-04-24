import google.generativeai as genai
import os

# Asegúrate de tener configurada tu clave de API de Gemini
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)
# model = genai.GenerativeModel('gemini-pro')
# model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
model = genai.GenerativeModel('models/gemini-2.0-flash')


# async def async_generate_improved_definition(word_palabra, original_definition_definicion_original, target_language, age):
#     """
#     Genera una definición adaptada usando la API de Gemini de forma asíncrona.

#     Args:
#         original_definition (str): La definición original.
#         target_language (str): El idioma objetivo ('es' o 'en').
#         age (int): La edad del niño.

#     Returns:
#         str: La definición mejorada o None si hay un error.
#     """
#     if target_language == 'es':
#         prompt = f"""Necesito que adaptes la siguiente definición de la palabra {word_palabra} para una persona española de {age} años con un nivel medio/bajo de inglés para su edad. La definición debe ser adaptada a su edad y nivel: "{original_definition_definicion_original}". Debería tener 25 palabras como máximo"""
#     elif target_language == 'en':
#         prompt = f"""Please remake the following definition of the {word_palabra} for a Spanish person of {age} years old with an average level of English for his age. The definition should be adapted to his age and level: "{original_definition_definicion_original}". Should be a maximum of 25 words."""
#     else:
#         return "Idioma objetivo no válido."

#     try:
#         print(f"API_Key: {GOOGLE_API_KEY}")
#         models = genai.list_models()
#         print("Modelos disponibles:")
#         for available_model in models:
#             print(f"  Nombre: {available_model.name}")
#             print(f"  Descripción: {available_model.description}")
#             print(
#                 f"  Métodos de generación soportados: {available_model.supported_generation_methods}")
#             print("-" * 30)
#         response = await model.generate_content_async(prompt)
#         # response = await model.generate_content(prompt)
#         if response.parts and hasattr(response.parts[0], 'text'):
#             return response.parts[0].text.strip()
#         else:
#             print(f"Respuesta de Gemini inesperada: {response}")
#             return None
#     except Exception as e:
#         print(f"Error al comunicarse con la API de Gemini: {e}")
#         return None
    
async def async_generate_improved_definition(word_palabra, target_language, age):
    """
    Genera una definición adaptada usando la API de Gemini de forma asíncrona.

    Args:
        original_definition (str): La definición original.
        target_language (str): El idioma objetivo ('es' o 'en').
        age (int): La edad del niño.

    Returns:
        str: La definición mejorada o None si hay un error.
    """
    if target_language == 'es':
        prompt = f"""Necesito que me des una definición en español de la palabra {word_palabra} para una persona española de {age} años con un nivel medio/bajo de inglés para su edad. La definición debe ser adaptada a su edad y nivel:". Debería tener 25 palabras como máximo. Necesito que en la respuesta solo venga la definición"""
    elif target_language == 'en':
        prompt = f"""Please giveme a definition in english of the {word_palabra} for a Spanish person of {age} years old with an average level of English. The definition should be adapted to his age and level. Should be a maximum of 25 words. I need only the definition in the response."""
    else:
        return "Idioma objetivo no válido."

    try:
        print(f"API_Key: {GOOGLE_API_KEY}")
        models = genai.list_models()
        # print("Modelos disponibles:")
        # for available_model in models:
        #     print(f"  Nombre: {available_model.name}")
        #     print(f"  Descripción: {available_model.description}")
        #     print(
        #         f"  Métodos de generación soportados: {available_model.supported_generation_methods}")
        #     print("-" * 30)
        response = await model.generate_content_async(prompt)
        # response = await model.generate_content(prompt)
        if response.parts and hasattr(response.parts[0], 'text'):
            return response.parts[0].text.strip()
        else:
            print(f"Respuesta de Gemini inesperada: {response}")
            return None
    except Exception as e:
        print(f"Error al comunicarse con la API de Gemini: {e}")
        return None

async def async_generate_improved_translate(word_palabra, target_language, age):
    """
    Genera la traducción adaptada usando la API de Gemini de forma asíncrona.

    Args:
        target_language (str): El idioma objetivo ('es' o 'en').
        age (int): La edad del niño.

    Returns:
        str: La traducción mejorada o None si hay un error.
    """
    if target_language == 'es':
        prompt = f"""Necesito que me des una traducción a español de la palabra {word_palabra} para una persona española de {age} años con un nivel medio/bajo de inglés para su edad. Necesito una traducción y no una definición. Necesito que en la respuesta solo venga la traducción"."""
    elif target_language == 'en':
        prompt = f"""Please giveme a translation in english of the {word_palabra} for a Spanish person of {age} years old with an average level of English. I need a translation not a definition. I only need the translation in the response."""
    else:
        return "Idioma objetivo no válido."

    try:
        print(f"API_Key: {GOOGLE_API_KEY}")
        models = genai.list_models()
        # print("Modelos disponibles:")
        # for available_model in models:
        #     print(f"  Nombre: {available_model.name}")
        #     print(f"  Descripción: {available_model.description}")
        #     print(
        #         f"  Métodos de generación soportados: {available_model.supported_generation_methods}")
        #     print("-" * 30)
        response = await model.generate_content_async(prompt)
        # response = await model.generate_content(prompt)
        if response.parts and hasattr(response.parts[0], 'text'):
            return response.parts[0].text.strip()
        else:
            print(f"Respuesta de Gemini inesperada: {response}")
            return None
    except Exception as e:
        print(f"Error al comunicarse con la API de Gemini: {e}")
        return None


if __name__ == '__main__':
    # Ejemplo de uso (necesitarás tener la variable de entorno configurada)
    original = "The process by which green plants and some other organisms use sunlight to synthesize foods with the help of chlorophyll."
    word_palabra = "green plants"
    improved_es = generate_improved_definition(word_palabra, original, 'es', 8)
    print(f"Definición original: {original}")
    print(f"Definición mejorada (ES): {improved_es}")

    improved_en = generate_improved_definition(word_palabra, original, 'en', 8)
    print(f"Definición mejorada (EN): {improved_en}")
