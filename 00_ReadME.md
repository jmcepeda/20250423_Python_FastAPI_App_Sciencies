# Configuración del Entorno Virtual y Dependencias del Proyecto

Este documento describe los pasos necesarios para configurar correctamente el entorno virtual de este proyecto, instalar las dependencias y solucionar los problemas relacionados con la biblioteca `enchant` y sus diccionarios para la verificación de palabras en español.

## 0000. Preparación Previa de dependecias con el script

    ```
    ./setup_env.sh
    ```

## 000. Activar Entorno Virtual con el script

    ```
    conda activate new_env
    ```

## 00. Instalar dependencias en el entorno virtual

    ```
    pip install -r setup/requirements.txt
    ```

## 0. Lanzar la Aplicación (Esta opción funciona mejor que la tradicional 'python main.py')

    ```
    uvicorn main:app --reload
    ```

## 0. Lanzar la Aplicación

    ```
    <!-- python main.py (Parece que esto ya no debo usarlo) -->
    ```

## 1. Asegurarse de que el Entorno Virtual esté Activado

**¡Importante!** Antes de ejecutar el script `main.py`, es crucial activar el entorno virtual. De lo contrario, Python utilizará las bibliotecas instaladas globalmente en tu sistema, lo que puede llevar a errores y a un comportamiento inesperado.

**¿Cómo activar el entorno virtual?**

1.  Abre tu terminal y navega hasta el directorio raíz de tu proyecto (`01_API_Translate`).
2.  Ejecuta el siguiente comando para activar el entorno virtual llamado `.venv`:

Si no existe el entorno virtual, debes crearlo

    ```
    python3 -m venv .venv
    ```

Seguimos con más código para activar el entorno virtual

    ```
    source .venv/bin/activate
    ```

    Después de ejecutar este comando, deberías ver `(.venv)` al principio de la línea de tu terminal, indicando que el entorno virtual está activo.

**¡No ejecutes `python main.py` antes de ver `(.venv)` en tu terminal!**

## 2. Instalación de las Dependencias del Proyecto

Todas las bibliotecas necesarias para este proyecto están listadas en el archivo `requirements.txt`. Para instalarlas, sigue estos pasos:

1.  **Asegúrate de que tu entorno virtual esté activado** (como se describe en la sección anterior).
2.  Navega hasta el directorio raíz de tu proyecto (donde se encuentra el archivo `requirements.txt`).
3.  Ejecuta el siguiente comando para instalar todas las dependencias:

    ```
    pip install -r requirements.txt
    ```

    Este comando leerá el archivo `requirements.txt` e instalará automáticamente todas las bibliotecas especificadas, incluyendo `fastapi`, `pyenchant`, `gTTS`, `googletrans`, `deep-translator`, `google-generativeai`, `aiohttp`, `gemini-api`, `pydantic` y `typing-extensions`. **Este comando se ejecuta dentro del entorno virtual activado (`(.venv)` en tu terminal).**

## 3. Enlazando Correctamente los Diccionarios con `enchant` y `pyenchant`

Uno de los problemas recurrentes puede ser que `pyenchant` no encuentre los diccionarios de español necesarios. Aquí se describe el proceso para asegurar que estén correctamente enlazados:

1.  **Instalar la biblioteca `enchant` a nivel del sistema:** `pyenchant` depende de una biblioteca de C llamada `enchant`. Si no está instalada en tu sistema, `pyenchant` no funcionará correctamente. En macOS, puedes instalarla usando Homebrew (**ejecuta este comando fuera del entorno virtual**):

    ```
    brew install enchant
    ```

2.  **Verificar la instalación de `hunspell` (backend de `enchant`):** `enchant` suele utilizar `hunspell` como corrector ortográfico. Asegúrate de que `hunspell` esté instalado (**ejecuta este comando fuera del entorno virtual**):

    ```
    brew install hunspell
    ```

3.  **Instalar los diccionarios de español para `hunspell`:** El paquete principal de `hunspell` puede no incluir todos los diccionarios de idiomas. Busca e instala el paquete de diccionario de español (**ejecuta estos comandos fuera del entorno virtual**):

    ```
    brew search hunspell spanish
    # Si encuentras un paquete como hunspell-es, instálalo:
    brew install hunspell-es
    ```

    Si la búsqueda no da resultados directos, intenta buscar "spanish dictionary" en Homebrew en general:

    ```
    brew search spanish dictionary
    ```

    ```
    export PYENCHANT_DICT_PATH="/opt/homebrew/Cellar/aspell/0.60.8.1_1/lib/aspell-0.60"

    ```

    E instala cualquier paquete relevante que encuentres con `brew install nombre_del_paquete` (**fuera del entorno virtual**).

4.  **Activa tu entorno virtual:** Si aún no está activo, ejecútalo ahora:

    ```
    source .venv/bin/activate
    ```

5.  **Reinstalar `pyenchant` dentro del entorno virtual:** Después de asegurarte de que `enchant` y los diccionarios de español están instalados a nivel del sistema, reinstala `pyenchant` dentro de tu entorno virtual (asegúrate de que esté activo):

    ```
    pip uninstall pyenchant
    pip install pyenchant
    ```

    **Estos comandos `pip` se ejecutan dentro del entorno virtual activado (`(.venv)` en tu terminal).**

6.  **Probar la carga del diccionario de español en Python:** Ejecuta una sesión de Python dentro de tu entorno virtual y prueba cargar el diccionario de español:

    ```
    python
    import enchant
    print(enchant.list_languages())
    diccionario_es = enchant.Dict("es_ES")
    print(diccionario_es.check("Arbol"))
    print(diccionario_es.check("tree"))
    ```

    La salida de `enchant.list_languages()` debería incluir códigos de idioma como `es` o `es_ES`. La comprobación de "Arbol" debería dar `True` y la de "tree" debería dar `False`. **Estos comandos `python` se ejecutan dentro del entorno virtual activado.**

**Si persisten los problemas con los diccionarios:**

- **Verifica las variables de entorno:** En algunos casos, puede ser necesario configurar variables de entorno como `DYLD_LIBRARY_PATH` para que Python encuentre las bibliotecas compartidas de `enchant`. Intenta esto **después de activar tu entorno virtual**:

  ```bash
  export DYLD_LIBRARY_PATH="/opt/homebrew/Cellar/enchant/*/lib:$DYLD_LIBRARY_PATH"
  ```

  (Reemplaza `*` con la versión correcta de `enchant`).

- **Reconstruye el entorno virtual:** Si todo lo demás falla, elimina el directorio `.venv` y vuelve a crear el entorno e instalar las dependencias desde cero. **Recuerda activar el entorno antes de usar `pip install`.**

  ```bash
  deactivate
  rm -rf .venv
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

Siguiendo estos pasos y asegurándote de activar siempre tu entorno virtual antes de ejecutar tu script, deberías poder mantener una configuración estable y evitar tener que reinstalar todo repetidamente.
