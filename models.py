from pydantic import BaseModel


# Модели для регистрации
class RegisterModel(BaseModel):
    name: str
    password: str
    email: str


class LoginModel(BaseModel):
    name: str
    password: str


class Token(BaseModel):
    token: str
    token_type: str



