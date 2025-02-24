from fastapi.testclient import TestClient
from main import app, Book, User, Borrowing

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Library Management System"}

def test_create_book():
    book_data = {"id": 1, "title": "Test Book", "author": "Test Author", "publisher": "Test Publisher", "isbn": "1234567890", "stock": 5}
    response = client.post("/books/", json=book_data)
    assert response.status_code == 200
    assert response.json() == book_data

def test_read_book():
    response = client.get("/books/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "title": "Test Book", "author": "Test Author", "publisher": "Test Publisher", "isbn": "1234567890", "stock": 5}

def test_update_book():
    updated_book_data = {"id": 1, "title": "Updated Book", "author": "Updated Author", "publisher": "Updated Publisher", "isbn": "0987654321", "stock": 10}
    response = client.put("/books/1", json=updated_book_data)
    assert response.status_code == 200
    assert response.json() == updated_book_data

def test_delete_book():
    response = client.delete("/books/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Book deleted successfully"}

def test_create_user():
    user_data = {"id": 1, "name": "Test User", "email": "test@example.com"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200
    assert response.json() == user_data

def test_read_user():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test User", "email": "test@example.com"}

def test_update_user():
    updated_user_data = {"id": 1, "name": "Updated User", "email": "updated@example.com"}
    response = client.put("/users/1", json=updated_user_data)
    assert response.status_code == 200
    assert response.json() == updated_user_data

def test_delete_user():
    response = client.delete("/users/1")
    assert response.status_code == 200
    assert response.json() == {"message": "User deleted successfully"}

def test_borrow_book():
    # First create a book and a user
    book_data = {"id": 2, "title": "Borrowable Book", "author": "Test Author", "publisher": "Test Publisher", "isbn": "1122334455", "stock": 1}
    client.post("/books/", json=book_data)
    user_data = {"id": 2, "name": "Borrower", "email": "borrower@example.com"}
    client.post("/users/", json=user_data)

    borrow_data = {"user_id": 2, "book_id": 2, "borrow_date": "2024-01-01"}
    response = client.post("/borrow/", json=borrow_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Book borrowed successfully"}

def test_return_book():
    return_data = {"user_id": 2, "book_id": 2, "borrow_date": "2024-01-01"}
    response = client.post("/return/", json=return_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Book returned successfully"}

def test_read_books():
    response = client.get("/books/")
    assert response.status_code == 200

def test_read_users():
    response = client.get("/users/")
    assert response.status_code == 200

def test_read_borrowed_books():
    response = client.get("/borrowed/")
    assert response.status_code == 200

def test_read_borrowed_books_by_user():
    response = client.get("/borrowed/2")
    assert response.status_code == 200