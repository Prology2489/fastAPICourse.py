from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Corrected database URL
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

# Create a session local
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define the base class for models
Base = declarative_base()  # Base is the object used for model declarations
