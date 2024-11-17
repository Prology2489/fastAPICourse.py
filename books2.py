from typing import Optional
from fastapi import FastAPI # Framework to build APIs Quickly
from pydantic import BaseModel, Field # used for data validation and modeling

app = FastAPI() #initializes a FastAPI application instance

class Book:    #Represents a book with attributes 
    id: int
    title: str 
    author: str
    description: str
    rating: int
    
    def __init__(self, id, title, author, description, rating): #Initialization
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating

class BookRequest(BaseModel): #allows validation and converts data that can be stored
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str =Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=11)

    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "author of the book",
                "author": "Dune the chosen one",
                "description": "A new description of a book",
                "rating": 9
            }
        }
        }
    


BOOKS = [        # A list of Book objects to simulate a database
    Book(1, "Lord Of The rings", "jrr tolkien", "a grand adventure", 10),
    Book(2, "Star Wars", "georgre lucas", "epic space opera", 9),
    Book(3, "Harry Potter", "jk rowling", "magical world", 7),
    Book(4, "twilight", "stephenie meyer", "romance fantasy", 8),
    Book(5, "Pacific Rim", "del toro", "war against monsters", 1),
    Book(6, "Blade Runner", "denis villeneuve", "neo noir science fiction", 3)    
]

@app.get("/books") #Fetch all books from the BOOKS list
async def read_all_books():
    return BOOKS



@app.post("/create-book") #Add a new book to the BOOKS list.
async def create_book(book_request: BookRequest):    #BookRequest: Ensures API input validation.
    new_book = Book(**book_request.model_dump()) 
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):  #The function assigns an id dynamically based on the existing BOOKS list to ensure that each new book has a unique id
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1 #checks whether there are any books in the list to get the next ID or assigns 1 if empty
                                                            # BOOKS[-1] refers to the last item in the list, and BOOKS must not be empty for this to work.
    return book


