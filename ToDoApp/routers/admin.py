from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path
from models import Todos
from database import SessionLocal
from .auth import get_current_user



#new admin router file, which has the ability to authenticate a user, check if that users is a admin

router = APIRouter(prefix='/admin',
    tags=['admin'])


def get_db():
    db = SessionLocal() # we can now contact the database
    try:
        yield db 
    finally:
        db.close() #return all the information back

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/todo", status_code=status.HTTP_200_OK)    #allows admin to view all users
async def read_all(user: user_dependency, db: db_dependency):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Todos).all()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)      #allows admin to delete a user
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None or user.get('user_role') != 'admin':
        raise HTTPException(status_code=401, detail='Authentication Failed')
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    db.query(Todos).filter(Todos.id == todo_id).delete()
    db.commit()

