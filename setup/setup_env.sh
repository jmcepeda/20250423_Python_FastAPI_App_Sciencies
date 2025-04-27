#!/bin/bash

# Desactiva todos los entornos Conda activos
# conda init 

# conda deactivate
# conda deactivate
# conda deactivate

# Reinstala las bibliotecas del sistema
brew reinstall enchant
brew reinstall hunspell
brew reinstall aspell

# Activa tu entorno Conda

# conda activate new_env

# echo "Entorno y bibliotecas configurados."

# Desactiva todos los entornos Conda activos
# conda deactivate

# # Activa tu entorno Conda
# conda activate new_env

# # Instala nltk y sus dependencias
# conda install -c conda-forge nltk

# # Descarga los recursos necesarios de nltk (inglés y español)
# python -c "import nltk; nltk.download('words')"

# echo "nltk y sus dependencias instaladas y configuradas."

# conda deactivate

# Activa tu entorno Conda (PowerShell)
# conda activate new_env

# Instala nltk y sus dependencias (PowerShell)
conda install -c conda-forge nltk -y

# Descarga los recursos necesarios de nltk (inglés words corpus)
python -c "import nltk; nltk.download('words')"

# Descarga el Spanish grammar package (might contain vocabulary)
python -c "import nltk; nltk.download('spanish_grammars')"

echo "Iniciando la instalación de dependencias..."

# Instalar las librerías desde el archivo
pip install -r setup/requierements.txt

# Write-Host "Entorno, nltk y recursos instalados y configurados."

if [ $? -eq 0 ]; then
    echo "Librerías instaladas correctamente."

    # Ejecutar el script de Python para descargar WordNet
    echo "Descargando los datos de WordNet..."
    python setup/descargar_wordnet.py

    if [ $? -eq 0 ]; then
        echo "Configuración completa."
    else
        echo "Error al descargar los datos de WordNet."
        exit 1
    fi
else
    echo "Error al instalar las librerías."
    exit 1
fi



exit 0

