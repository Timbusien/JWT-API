'''Авторизация позволяет определить, имеют ли пользователи
или клиенты право на доступ к определённым ресурсам,
выполнение определнных действий или получение данных от
сервера'''


'''JWT (JSON Wev Tokens) - это один из видов авторизации с 
использованием уникальных токенов, которые могут быть
ипользованы для авторизации.'''

'''JWT содержит закодированны данные о пользователе и метку
 времени, и они могут быть проверены без обращения к базе
 данных'''


from fastapi import FastAPI
from passlib.context import CryptContext
from jwtservice import create_access_token
from models import RegisterModel, LoginModel
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwtservice import verify_token
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    return payload


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(docs_url='/')


@app.get('/home')
async def home():
    return {'message': 'Hello world'}


@app.post('/register')
async def register(user: RegisterModel):
    pass


@app.post('/login')
async def login(user: LoginModel):
    # Проверка авторизации
    result = create_access_token(user.model_dump(), 20)

    return {'jwt': result}


@app.get("/secure-data")
async def secure_data(current_user: dict = Depends(get_current_user)):
    return {"message": "This data is secure", "user": current_user}

