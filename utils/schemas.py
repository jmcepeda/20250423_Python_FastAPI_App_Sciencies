from pydantic import BaseModel


class WordCreateRequest(BaseModel):
    word_en: str
    lang: str
    username: str
    firstname: str∫
    lastname: str
    email: str
    wordpress_id: int
