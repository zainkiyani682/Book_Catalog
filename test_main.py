import pytest
from fastapi.testclient import TestClient
from crud import app
from db import SessionLocal
from models import Book_Catalog
from uuid import uuid4
from datetime import datetime

client = TestClient(app)
CURRENT_YEAR = datetime.now().year

# Automatically clear the database before each test
@pytest.fixture(autouse=True)
def clear_database():
    db = SessionLocal()
    db.query(Book_Catalog).delete()
    db.commit()
    db.close()


def create_unique_payload(summary=None):
    return {
        "title": f"Test Book {uuid4()}",
        "author": "Zain",
        "published_year": CURRENT_YEAR - 1,
        "summary": summary,
    }


def test_create_book():
    payload = create_unique_payload()
    response = client.post("/books/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == payload["title"]
    assert data["author"] == payload["author"]
    assert data["published_year"] == payload["published_year"]
    assert data.get("summary") is None


def test_create_book_with_summary():
    payload = create_unique_payload(summary="A great book")
    response = client.post("/books/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["summary"] == payload["summary"]


def test_get_all_books():
    payload = create_unique_payload()
    client.post("/books/", json=payload)
    response = client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_get_single_book():
    payload = create_unique_payload()
    post_response = client.post("/books/", json=payload)
    book_id = post_response.json()["id"]

    response = client.get(f"/books/{book_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == book_id


def test_update_book():
    payload = create_unique_payload()
    post_response = client.post("/books/", json=payload)
    book_id = post_response.json()["id"]

    updated_payload = {
        "title": f"Updated Book {uuid4()}",
        "author": "Updated Author",
        "published_year": CURRENT_YEAR - 2,
        "summary": "Updated Summary",
    }

    response = client.put(f"/books/{book_id}", json=updated_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == updated_payload["title"]
    assert data["summary"] == updated_payload["summary"]


def test_delete_book():
    payload = create_unique_payload()
    post_response = client.post("/books/", json=payload)
    book_id = post_response.json()["id"]

    delete_response = client.delete(f"/books/{book_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Item Deleted Successfully"

    # Verify deletion
    get_response = client.get(f"/books/{book_id}")
    assert get_response.status_code == 404
    assert get_response.json().get("detail") == "Book not found"
