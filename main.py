from fastapi import FastAPI
# from api import auth_router, translate_router
from api.endpoints.auth import router as auth_router
from api.endpoints.translate import router as translate_router
from database.models.word import Word
from database.models.word import DefinitionsEs
from database.models.word import DefinitionsEn
from database.models.word import TranslationEs
from database.models.word import TranslationEn
from database.models.word import Imagen
from database.models.word import Audio
from database.models.word import Curso
from database.models.word import Asignatura
# from database.models.word import WordModification
from database.models.usuario import Usuario
# from database.models.ejercicio import ResultadoEjercicio, TipoEjercicio
from database.models.ejercicio import TipoEjercicio
# from database.models.reto import Reto, WordReto, ResultadoReto, EstadoReto
# from database.models.reto import Reto, WordReto, EstadoReto
# Removed unused imports Reto and EstadoReto
from database.models.reto import Reto

# from api.endpoints import auth_router, translate_router
# from api import auth_router, translate_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(translate_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
