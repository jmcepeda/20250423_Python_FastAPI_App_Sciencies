from fastapi import FastAPI
# from api import auth_router, translate_router
from api.endpoints.auth import router as auth_router
from api.endpoints.translate import router as translate_router

# from api.endpoints import auth_router, translate_router
# from api import auth_router, translate_router

app = FastAPI()

app.include_router(auth_router)
app.include_router(translate_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)