from datetime import timedelta,datetime           #Token kitne time ke liye valid hoga aur kab expire hoga ye handle karne ke liye.
from typing import Annotated                      #FastAPI me dependencies ko type hint ke sath easily inject karne ka shortcut.
from fastapi import APIRouter, Depends, HTTPException      #APIRouter → Alag-alag routes (like auth, users, products) ko group karke organize karne ke liye.
                                                           #Depends → Functions/classes ko dependency injection ke liye use karte hain (jaise DB session ya auth check).
                                                           #HTTPException → Error aane pe user ko proper HTTP error response dene ke liye (jaise 401 Unauthorized).
from pydantic import BaseModel                   #Pydantic ka model, request/response data validate aur structure karne ke liye.
from sqlalchemy.orm import Session                #SQLAlchemy ka session object, jo DB me query karne ke kaam aata hai.
from starlette import status
from jose import JWTError, jwt                    #JWT token banane, decode karne aur verify karne ke liye.
from passlib.context import CryptContext          #Password ko securely hash aur verify karne ke liye (
from database import SessionLocal                 #Database session create karne ke liye ready-made function.
from models import User
from fastapi.security import OAuth2PasswordRequestForm,OAuth2AuthorizationCodeBearer,OAuth2PasswordBearer                     #Ye mostly 3rd party login (Google, GitHub) ke liye hota hai, JWT simple auth me use nahi hota.


router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY='3fT9kLz8sD1QeXvYzW9gJmKpR7tUoVbXcYzQwErT1GhI'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    access_token: str
    token_type: str
class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db= SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

class CreateUserRequest(BaseModel):
    username: str
    password: str

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_user(db: db_dependency, created_user_request: CreateUserRequest):
    create_user_model = User(
        username=created_user_request.username,
        hashed_password=bcrypt_context.hash(created_user_request.password),
    )
    db.add(create_user_model)
    db.commit()
    db.refresh(create_user_model)
    return {"message": "User created successfully", "username": create_user_model.username}

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    

    user=authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",)
    token=create_access_user(user.username, user.Id, timedelta(minutes=20))

def authenticate_user(username: str, password: str, db: Session):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_user(username: str, user_id: int, expires_delta: timedelta = None):
    encode = {"sub": username, "id": user_id}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode.update({"exp": expire})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)