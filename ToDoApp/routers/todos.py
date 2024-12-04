from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path
from models import Todos
from database import SessionLocal
from .auth import get_current_user

router = APIRouter()


def get_db():
    db = SessionLocal() # we can now contact the database
    try:
        yield db 
    finally:
        db.close() #return all the information back

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel): #adding validation to todo requests
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    Priority: int = Field(gt=0, lt=6)
    complete: bool 

@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()  #return all of the todos from our database



@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):    #added validation, needs to be greater then 0
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    
      
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()   #adding a query that will look at our todos table and turn all todos that have the same ID as the path parameter.
    if todo_model is not None: # making sure it has valid data, return data or raise a HTTP exception
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not Found.")


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    
    
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    
    db.add(todo_model) #getting the database ready
    db.commit() #actually doing the transaction to the database


@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)    #update request based on authentication
async def Update_todo(user: user_dependency, db: db_dependency,
                      todo_request: TodoRequest,
                      todo_id: int  = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail="Todo not found.")
    
    todo_model.title = todo_request.title
    todo_model.description = todo_request.description
    todo_model.Priority = todo_request.Priority
    todo_model.complete = todo_request.complete

    db.add(todo_model)
    db.commit()

@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependency, todo_id: int =Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    
    todo_model = db.query(Todos).filter(Todos.id == todo_id)\
        .filter(Todos.owner_id == user.get('id')).first()
    if todo_model is None:    #validating that todo is a real record by the id getting passed in and user that is authenticated
        raise HTTPException(status_code=404, detail="Todo not Found.")
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()

    db.commit()
