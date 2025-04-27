import nltk

try:
    nltk.download('wordnet')
    print("Datos de WordNet descargados correctamente.")
except Exception as e:
    print(f"Error al descargar los datos de WordNet: {e}")
    exit(1)  # Salir con código de error si falla
