from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Book(BaseModel):
    id: int
    title: str
    author: str
    publisher: str
    isbn: str
    stock: int

books = []

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Library Management System"}

@app.post("/books/", response_model=Book)
async def create_book(book: Book):
    books.append(book)
    return book

@app.get("/books/", response_model=List[Book])
async def read_books():
    return books

@app.get("/books/{book_id}", response_model=Book)
async def read_book(book_id: int):
    for book in books:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.put("/books/{book_id}", response_model=Book)
async def update_book(book_id: int, updated_book: Book):
    for index, book in enumerate(books):
        if book.id == book_id:
            books[index] = updated_book
            return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}")
async def delete_book(book_id: int):
    for index, book in enumerate(books):
        if book.id == book_id:
            del books[index]
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=404, detail="Book not found")

class User(BaseModel):
    id: int
    name: str
    email: str

users = []

@app.post("/users/", response_model=User)
async def create_user(user: User):
    users.append(user)
    return user

@app.get("/users/", response_model=List[User])
async def read_users():
    return users

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    for user in users:
        if user.id == user_id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, updated_user: User):
    for index, user in enumerate(users):
        if user.id == user_id:
            users[index] = updated_user
            return updated_user
    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    for index, user in enumerate(users):
        if user.id == user_id:
            del users[index]
            return {"message": "User deleted successfully"}
    raise HTTPException(status_code=404, detail="User not found")

class Borrowing(BaseModel):
    user_id: int
    book_id: int
    borrow_date: str
    return_date: str = None

borrowed_books = []

@app.post("/borrow/")
async def borrow_book(borrowing: Borrowing):
    # Check if user and book exist
    user_exists = any(user.id == borrowing.user_id for user in users)
    book_exists = any(book.id == borrowing.book_id for book in books)

    if not user_exists or not book_exists:
        raise HTTPException(status_code=400, detail="Invalid user_id or book_id")

    # Check if book is in stock
    book = next((book for book in books if book.id == borrowing.book_id), None)
    if book.stock <= 0:
        raise HTTPException(status_code=400, detail="Book is out of stock")

    # Update book stock
    book.stock -= 1
    borrowed_books.append(borrowing)
    return {"message": "Book borrowed successfully"}

@app.post("/return/")
async def return_book(borrowing: Borrowing):
    # Check if borrowing record exists
    borrowing_exists = False
    for index, borrowed in enumerate(borrowed_books):
        if borrowed.user_id == borrowing.user_id and borrowed.book_id == borrowing.book_id:
            borrowing_exists = True
            del borrowed_books[index]
            break

    if not borrowing_exists:
        raise HTTPException(status_code=404, detail="Borrowing record not found")

    # Update book stock
    book = next((book for book in books if book.id == borrowing.book_id), None)
    book.stock += 1
    return {"message": "Book returned successfully"}

@app.get("/borrowed/")
async def list_borrowed_books():
    return borrowed_books

@app.get("/borrowed/{user_id}")
async def list_borrowed_books_by_user(user_id: int):
    user_borrowed = [borrowed for borrowed in borrowed_books if borrowed.user_id == user_id]
    return user_borrowed