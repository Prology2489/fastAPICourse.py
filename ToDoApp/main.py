from typing import Annotated
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
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

@app.get("/")
async def read_all(db: db_dependency):
    return db.query(Todos).all()   #return all of the todos from our database



   #in programming, allow us to do code behind scenes