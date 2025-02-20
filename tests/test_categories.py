def test_create_category(client):
    response = client.post(
        "/categories/",
        json={"name": "Roman", "description": "Roman kategorisi"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Roman"
    assert data["description"] == "Roman kategorisi"
    assert "id" in data

def test_read_categories(client, test_category):
    response = client.get("/categories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == test_category.name
    assert data[0]["description"] == test_category.description

def test_create_category_invalid(client):
    # Name olmadan kategori oluşturma denemesi
    response = client.post(
        "/categories/",
        json={"description": "Geçersiz kategori"}
    )
    assert response.status_code == 422  # Validation Error 