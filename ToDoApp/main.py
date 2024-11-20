from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException, status, Path
import models
from models import Todos
from database import engine, SessionLocal

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal() # we can now contact the database
    try:
        yield db 
    finally:
        db.close() #return all the information back

db_dependency = Annotated[Session, Depends(get_db)]



class TodoRequest(BaseModel): #adding validation to todo requests
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    Priority: int = Field(gt=0, lt=6)
    complete: bool 

@app.get("/", status_code=status.HTTP_200_OK)
async def read_all(db: db_dependency):
    return db.query(Todos).all()   #return all of the todos from our database



@app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(db: db_dependency, todo_id: int = Path(gt=0)): #added validation, needs to be greater then 0
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()   #adding a query that will look at our todos table and turn all todos that have the same ID as the path parameter.
    if todo_model is not None: # making sure it has valid data, return data or raise a HTTP exception
        return todo_model
    raise HTTPException(status_code=404, detail="Todo not Found.")


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_tool(db: db_dependency, todo_request: TodoRequest):
    todo_model = Todos(**todo_request.model_dump())
    
    db.add(todo_model) #getting the database ready
    db.commit() #actually doing the transaction to the database