
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from datetime import timedelta, datetime, timezone




router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

SECRET_KEY = 'f1301773c620d411ebe3824330a5cc187d04344f24d49f9b48c21fe7fb07e24f'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class CreateUserRequest(BaseModel):
    username : str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal() # we can now contact the database
    try:
        yield db 
    finally:
        db.close() #return all the information back

db_dependency = Annotated[Session, Depends(get_db)]


def authenticate_user(username: str, password: str, db):  # new function that takes in username, password and database session
    user = db.query(Users).filter(Users.username == username).first() # we query the username, qunique value
    if not user:    # if nothing from database we rreturn false
        return False
    if not bcrypt_context.verify(password, user.hashed_password): # if we run and it takes in password and checks hash password and see if it macthes, tell us if user password is correct
        return False # return false if no user matches
    return user # return True if matches


def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):

    encode = {'sub': username, 'id': user_id, 'role': role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: int = payload.get('id')
        user_role: str = payload.get('role')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='could not validate user.')
        return {'username': username, 'id': user_id, 'user_role': user_role}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='could not validate user.')

@router.post("/", status_code=status.HTTP_201_CREATED)  #created new users and saved it to our database
async def create_user(db: db_dependency,
                      create_user_request: CreateUserRequest):
    create_user_model = Users(
        email=create_user_request.email,
        username=create_user_request.username,
        first_name=create_user_request.first_name,
        last_name=create_user_request.last_name,
        role=create_user_request.role,
        hashed_password=bcrypt_context.hash(create_user_request.password),   #bcrypt will be equal to what create_user_request.password returns  
        is_active=True
    )

    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token) #token return to user and contains all information inside

async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],   # this function will validate the password and username and match to the database.
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail='could not validate user.') # this will fail if user does not work
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))


    return {'access_token': token, 'token_type': 'bearer'} # we pass in correct username and password              




  

