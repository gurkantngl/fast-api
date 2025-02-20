def test_create_loan(client, test_book):
    response = client.post(
        "/loans/",
        json={
            "book_id": test_book.id,
            "borrower_name": "Test Kullanıcı"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["book_id"] == test_book.id
    assert data["borrower_name"] == "Test Kullanıcı"
    assert data["is_returned"] == False

def test_create_loan_book_not_found(client):
    response = client.post(
        "/loans/",
        json={
            "book_id": 999,
            "borrower_name": "Test Kullanıcı"
        }
    )
    assert response.status_code == 404

def test_create_loan_book_not_available(client, test_book, db_session):
    # İlk ödünç alma
    response = client.post(
        "/loans/",
        json={
            "book_id": test_book.id,
            "borrower_name": "İlk Kullanıcı"
        }
    )
    assert response.status_code == 200

    # Aynı kitabı tekrar ödünç alma denemesi
    response = client.post(
        "/loans/",
        json={
            "book_id": test_book.id,
            "borrower_name": "İkinci Kullanıcı"
        }
    )
    assert response.status_code == 400

def test_return_book(client, test_book):
    # Önce kitabı ödünç al
    loan_response = client.post(
        "/loans/",
        json={
            "book_id": test_book.id,
            "borrower_name": "Test Kullanıcı"
        }
    )
    loan_id = loan_response.json()["id"]

    # Şimdi kitabı iade et
    return_response = client.put(f"/loans/{loan_id}/return")
    assert return_response.status_code == 200
    assert return_response.json()["message"] == "Kitap başarıyla iade edildi"

def test_return_book_not_found(client):
    response = client.put("/loans/999/return")
    assert response.status_code == 404

def test_return_book_already_returned(client, test_book):
    # Önce kitabı ödünç al
    loan_response = client.post(
        "/loans/",
        json={
            "book_id": test_book.id,
            "borrower_name": "Test Kullanıcı"
        }
    )
    loan_id = loan_response.json()["id"]

    # İlk iade
    client.put(f"/loans/{loan_id}/return")

    # İkinci iade denemesi
    response = client.put(f"/loans/{loan_id}/return")
    assert response.status_code == 400

def test_read_loans(client, test_book):
    # Önce bir ödünç kaydı oluştur
    client.post(
        "/loans/",
        json={
            "book_id": test_book.id,
            "borrower_name": "Test Kullanıcı"
        }
    )

    # Ödünç kayıtlarını listele
    response = client.get("/loans/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["book_id"] == test_book.id
    assert data[0]["borrower_name"] == "Test Kullanıcı" 