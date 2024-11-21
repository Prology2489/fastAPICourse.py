from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

class Users(Base):
   __tablename__ = "users"
   
   id = Column(Integer, primary_key=True, index=True)
   email = Column(String, unique=True)
   username = Column(String, unique=True)
   first_name = Column(String)
   last_name = Column(String)
   hashed_password = Column(String)
   is_active = Column(Boolean, default=True) # will show if a user is active
   role = Column(String)

   

class Todos(Base): # new table in database called todos
    __tablename__ = "todos"  # a way for sql to what to name the table inside the database

    # will contain all these columns
    id = Column(Integer, primary_key=True, index=True) # this id will be a new colum and will be a integar, index is a way to increase performance, this will be unique
    title = Column(String)
    description = Column(String)
    Priority = Column(Integer)
    complete = Column(Boolean, default=False)
    owner_id = Column(Integer, ForeignKey("users.id")) # primary key of the user, so when a user signs ID we can match to primary key and find there to do list