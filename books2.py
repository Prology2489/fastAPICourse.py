from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException # Framework to build APIs Quickly
from pydantic import BaseModel, Field # used for data validation and modeling
from starlette import status

app = FastAPI() #initializes a FastAPI application instance

class Book:    #Represents a book with attributes 
    id: int
    title: str 
    author: str
    description: str
    rating: int
    published_date: int
    
    def __init__(self, id, title, author, description, rating, published_date): #Initialization
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date

class BookRequest(BaseModel): #allows validation and converts data that can be stored
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str =Field(min_length=1, max_length=100)
    rating: int = Field(gt=-1, lt=11)
    published_date: int = Field(gt=1980, lt=2025)

    model_config = {   #this gives an outlay for people adding a new book
        "json_schema_extra":{
            "example":{
                "title": "author of the book",
                "author": "Dune the chosen one",
                "description": "A new description of a book",
                "rating": 9,
                "published_date": 2012,
            }
        }
        }
    


BOOKS = [        # A list of Book objects to simulate a database
    Book(1, "Lord Of The rings", "jrr tolkien", "a grand adventure", 10, 2002),
    Book(2, "Star Wars", "georgre lucas", "epic space opera", 9, 1998),
    Book(3, "Harry Potter", "jk rowling", "magical world", 7, 2003),
    Book(4, "twilight", "stephenie meyer", "romance fantasy", 8, 2010),
    Book(5, "Pacific Rim", "del toro", "war against monsters", 1, 2008),
    Book(6, "Blade Runner", "denis villeneuve", "neo noir science fiction", 3, 2022)    
]

@app.get("/books", status_code=status.HTTP_200_OK) #Fetch all books from the BOOKS list + after success of retunring all book we want to return 200 code
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK) #Fetch a specific book from a list of books
async def read_book(book_id: int = Path(gt=0)):  #needs to be greater then 0 or error will occur
    for  book in BOOKS: #looping throuhg books
        if book.id == book_id:  # when book matches book ID we pass then we return the book
            return book
    raise HTTPException(status_code=404, detail="Item not found")  #this will raise HTTP Exception and show an error 

@app.get("/books/", status_code=status.HTTP_200_OK)   #filter books by rating in FastAPI
async def read_book_by_rating(book_rating: int = Query(gt=0, lt=11)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
            return books_to_return

@app.get("/books/publish/", status_code=status.HTTP_200_OK)   #filter books by published date + 200 code means everything is ok and here is the data
async def read_book_by_published_date(published_date: int = Query(gt=1980, lt=2025)): #ensured query parameter is protected
    books_to_return = []
    for book in BOOKS:
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return

@app.post("/create-book", status_code=status.HTTP_201_CREATED) #Add a new book to the BOOKS list.
async def create_book(book_request: BookRequest):    #BookRequest: Ensures API input validation.
    new_book = Book(**book_request.model_dump()) 
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):  #The function assigns an id dynamically based on the existing BOOKS list to ensure that each new book has a unique id
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1 #checks whether there are any books in the list to get the next ID or assigns 1 if empty
                                                            # BOOKS[-1] refers to the last item in the list, and BOOKS must not be empty for this to work.
    return book

@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)   # this function will allow us to update a book.
async def Update_book(book: BookRequest): #loop through the books to update the book i want
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id: #when we find ID of the ID we pass in, we swap new book with that books ID
            BOOKS[i] = book
            book_changed = True #successfully change book will be true
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found")



@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT) #204 code is just enhancing or changing with returning any data
async def delete_book(book_id: int = Path(gt=0)): #delete book function + added path validation 
    book_changed = False
    for i in range(len(BOOKS)): #loop through all books that match the ID then we can delete that item.
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not found") #catching unusal like ID that doesnt exist then returning HTTP exception back to the user
  
        



