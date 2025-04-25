#!/bin/bash

# Desactiva todos los entornos Conda activos
# conda init 

# conda deactivate
# conda deactivate
# conda deactivate

# Reinstala las bibliotecas del sistema
# brew reinstall enchant
# brew reinstall hunspell
# brew reinstall aspell

# Desactiva todos los entornos Conda activos (PowerShell)
conda deactivate

# Activa tu entorno Conda (PowerShell)
conda activate new_env

# Instala nltk y sus dependencias (PowerShell)
conda install -c conda-forge nltk -y

# Descarga los recursos necesarios de nltk (inglés words corpus)
python -c "import nltk; nltk.download('words')"

# Descarga el Spanish grammar package (might contain vocabulary)
python -c "import nltk; nltk.download('spanish_grammars')"

Write-Host "Entorno, nltk y recursos instalados y configurados."