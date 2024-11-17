from fastapi import FastAPI

app = FastAPI()

class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating): 
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


BOOKS = [
    Book(1, "Lord Of The rings", "jrr tolkien", "a grand adventure", 10),
    Book(2, "Star Wars", "georgre lucas", "epic space opera", 9),
    Book(3, "Harry Potter", "jk rowling", "magical world", 7),
    Book(4, "twilight", "stephenie meyer", "romance fantasy", 8),
    Book(5, "Pacific Rim", "del toro", "war against monsters", 1),
    Book(6, "Blade Runner", "denis villeneuve", "neo noir science fiction", 3)    
]

@app.get("/books")
async def read_all_books():
    return BOOKS

