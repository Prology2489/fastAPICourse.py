from database import Base
from sqlalchemy import Column, Integer, String, Boolean

class Todos(Base): # new table in database called todos
    __tablename__ = "todos"  #a way for sql to what to name the table inside the database

    # will contain all these columns
    id = Column(Integer, primary_key=True, index=True) #this id will be a new colum and will be a integar, index is a way to increase performance, this will be unique
    title = Column(String)
    description = Column(String)
    Priority = Column(Integer)
    complete = Column(Boolean, default=False)