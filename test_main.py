import pytest
from fastapi.testclient import TestClient
from main import app, init_db
client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_database():
    init_db()
    yield
    # После каждого теста база данных будет пересоздана

def test_create_note():
    response = client.post(
        "/notes/",
        json={"title": "Test Note", "content": "Test Content"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "Test Content"
    assert "id" in data
    assert "created_at" in data
    return data["id"]
def test_get_notes():
    response = client.get("/notes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
def test_get_note():
    # Сначала создаем заметку
    note_id = test_create_note()
    
    # Получаем созданную заметку
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Note"
    assert data["content"] == "Test Content"
def test_update_note():
    # Сначала создаем заметку
    note_id = test_create_note()
    
    # Обновляем заметку
    response = client.put(
        f"/notes/{note_id}",
        json={"title": "Updated Note", "content": "Updated Content"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Note"
    assert data["content"] == "Updated Content"
def test_delete_note():
    # Сначала создаем заметку
    note_id = test_create_note()
    
    # Удаляем заметку
    response = client.delete(f"/notes/{note_id}")
    assert response.status_code == 200
    
    # Проверяем, что заметка действительно удалена
    response = client.get(f"/notes/{note_id}")
    assert response.status_code == 404
def test_get_nonexistent_note():
    response = client.get("/notes/99999")
    assert response.status_code == 404
def test_update_nonexistent_note():
    response = client.put(
        "/notes/99999",
        json={"title": "Updated Note", "content": "Updated Content"}
    )
    assert response.status_code == 404
def test_delete_nonexistent_note():
    response = client.delete("/notes/99999")
    assert response.status_code == 404
