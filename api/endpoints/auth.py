from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm, HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
from pydantic import BaseModel
# from core.config import settings # Si usas un fichero de configuración
# from ...core.config import settings
from fastapi import Depends, FastAPI, HTTPException, APIRouter
# from core.config import settings # Si usas un fichero de configuración
from models.token import Token
from models.user import User
from database.models.usuario import Usuario  # <--- IMPORTACIÓN CORRECTA

from sqlalchemy.orm import Session
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from utils.schemas import WordCreateRequest
from utils.schemas import CurrentUserResponse, CreateUser  # importa tu modelo

from fastapi import Body

router = APIRouter()


@router.post("/login", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


def authenticate_user(username: str, frontend_key: str) -> Optional[User]:
    if frontend_key == settings.FRONTEND_APP_KEY:
        return User(username=username)
    return None


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


# Ejemplo de cómo podrías definir get_current_user aquí o en core/security.py
# Usa OAuth2PasswordBearer para /login
bearer_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(token: str = Depends(bearer_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="No se pudieron validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY,
                             algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        # Aquí podrías buscar al usuario en tu base de datos si fuera necesario
        return User(username=username)
    except JWTError:
        raise credentials_exception
    return None


async def get_current_user_test(
    # credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    # username: str = None  # <--- Este parámetro se llenará desde el "username" del body
    # <-- así recibes el body completo
    word_data: WordCreateRequest = Body(...),
    db: AsyncSession = Depends(get_db),
):
    """
    Función simplificada para obtener o crear un usuario basado en el username
    enviado en el cuerpo de la petición.
    """

    username = word_data.username  # <-- extraes el username del objeto
    print(
        f"Username recibido en la función -get_current_user_test-: {username}")

    response_data = CurrentUserResponse(
        username=word_data.username,
        firstname=word_data.firstname,
        lastname=word_data.lastname,
        email=word_data.email,
        wordpress_id=word_data.wordpress_id,
        usuario_existente_db=False
    )
    # response_data = {
    #     "username": username,
    #     "firstname": word_data.firstname,
    #     "lastname": word_data.lastname,
    #     "email": word_data.email,
    #     "wordpress_id": word_data.wordpress_id,
    #     "usuario_existente_db": False  # Nuevo campo con valor predeterminado False
    # }

    if username is None:
        raise HTTPException(
            status_code=400, detail="Se debe proporcionar un 'username' en el cuerpo de la petición.")

    # user = await db.query(User).filter(User.username == username).first()
    # user = await db.execute(select(User).where(User.username == username))

     # Corrección aquí
    result = await db.execute(select(Usuario).where(Usuario.username == username))
    user = result.scalar_one_or_none()

    if user:
        # Si el usuario existe, cambiar a True

        response_data.usuario_existente_db = True
        response_data.id = user.id

        print(
            f"El usuario {username} SI EXISTE en la base de datos. Estos son los datos del usuario existente:")
        print(user)
    else:
        # Si el usuario no existe, crear uno nuevo
        print(
            f"El usuario {username} NO Existe en la base de datos. Creando un nuevo usuario. Estos son los datos que se pasan a la función create_new_user_test:")
        # print(response_data)

        response_data = await create_new_user_test(db, response_data)
        # response_data["usuario_existente_db"] = True
        response_data.usuario_existente_db = True
        # nuevo_usuario = Usuario(
        #     username=word_data.username,
        #     firstname=word_data.firstname,
        #     lastname=word_data.lastname,
        #     email=word_data.email,
        #     wordpress_id=word_data.wordpress_id
        # )
        # db.add(nuevo_usuario)
        # await db.commit()
        # await db.refresh(nuevo_usuario)

    return response_data


async def create_new_user_test(db: AsyncSession, user_data: CreateUser, ):
    """
    Función para crear un usuario basado en el username
    enviado en el cuerpo de la petición.
    """

    username = user_data.username  # <-- extraes el username del objeto
    print(
        f"Username recibido en la función -create_new_user_test-: {username}")

    """Crea un nuevo usuario en la base de datos."""
    nuevo_usuario = Usuario(
        username=user_data.username,
        firstname=user_data.firstname,
        lastname=user_data.lastname,
        email=user_data.email,
        wordpress_id=user_data.wordpress_id
    )
    db.add(nuevo_usuario)
    await db.commit()
    await db.refresh(nuevo_usuario)
    return nuevo_usuario
