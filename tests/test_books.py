def test_create_book(client, test_category):
    response = client.post(
        "/books/",
        json={
            "title": "Yeni Kitap",
            "author": "Test Yazar",
            "isbn": "9876543210",
            "publication_year": 2023,
            "category_id": test_category.id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Yeni Kitap"
    assert data["author"] == "Test Yazar"
    assert data["isbn"] == "9876543210"
    assert data["available"] == True

def test_read_books(client, test_book):
    response = client.get("/books/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == test_book.title
    assert data[0]["author"] == test_book.author

def test_read_book_by_id(client, test_book):
    response = client.get(f"/books/{test_book.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == test_book.title
    assert data["author"] == test_book.author

def test_read_book_not_found(client):
    response = client.get("/books/999")
    assert response.status_code == 404

def test_update_book(client, test_book):
    response = client.put(
        f"/books/{test_book.id}",
        json={
            "title": "Güncellenmiş Kitap",
            "author": test_book.author,
            "isbn": test_book.isbn,
            "publication_year": test_book.publication_year,
            "category_id": test_book.category_id
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Güncellenmiş Kitap"

def test_delete_book(client, test_book):
    response = client.delete(f"/books/{test_book.id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Kitap başarıyla silindi"
    
    # Kitabın silindiğini kontrol et
    response = client.get(f"/books/{test_book.id}")
    assert response.status_code == 404

def test_filter_books_by_category(client, test_book, test_category):
    response = client.get(f"/books/?category_id={test_category.id}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == test_book.title 