
from typing import Annotated
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from models import Users
from passlib.context import CryptContext
from database import SessionLocal
from sqlalchemy.orm import Session
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm





router = APIRouter()


bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class CreateUserRequest(BaseModel):
    username : str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

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
    return True # return True if matches


@router.post("/auth", status_code=status.HTTP_201_CREATED)  #created new users and saved it to our database
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


@router.post("/token") #token return to user and contains all information inside

async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],   # this function will validate the password and username and match to the database.
                                 db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return 'Failed Authentication' # this will fail if user does not work
    return 'Successful Authentication' # we pass in correct username and password              




  
