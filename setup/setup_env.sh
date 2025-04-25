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

# Activa tu entorno Conda

# conda activate new_env

# echo "Entorno y bibliotecas configurados."

# Desactiva todos los entornos Conda activos
conda deactivate

# Activa tu entorno Conda
conda activate new_env

# Instala nltk y sus dependencias
conda install -c conda-forge nltk

# Descarga los recursos necesarios de nltk (inglés y español)
python -c "import nltk; nltk.download('words')"

echo "nltk y sus dependencias instaladas y configuradas."