from pydantic import BaseModel


class WordCreateRequest(BaseModel):
    word_en: str
    word_es: str
    username: str
