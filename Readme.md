````markdown
# 📘 FastAPI Book Catalog

A simple Book Catalog API built using **FastAPI**, **SQLAlchemy**, and **SQLite**.

## 🚀 Features

- Add a new book with validation
- Get all books or a single book by ID
- Update book details
- Delete a book by ID
- Validation for `published_year` (between 1450 and current year)
- Asynchronous support for fetching all books

## 🛠️ Tech Stack

- Python 3.10+
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic

## 📦 Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/fastapi-book-catalog.git
   cd fastapi-book-catalog
````

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**

   ```bash
   uvicorn main:app --reload
   ```

## 📌 API Endpoints

### ➕ Add Book

**POST** `/books/`

#### ✅ Payload without summary:

```json
{
  "title": "Test Book",
  "author": "Zain",
  "published_year": 2023
}
```

#### ✅ Payload with summary:

```json
{
  "title": "Learn FastAPI Part 2",
  "author": "Sebastián Ramírez",
  "published_year": 2016,
  "summary": "Intro to FastAPI"
}
```

---

### 📚 Get All Books

**GET** `/books/`

---

### 🔍 Get Book by ID

**GET** `/books/{book_id}`

---

### ✏️ Update Book

**PUT** `/books/{book_id}`

Payload format is the same as POST.

---

### ❌ Delete Book

**DELETE** `/books/{book_id}`

---

## ✅ Validations

* `published_year` must be between 1450 and current year (2024).
* Optional summary field.
* Example validation logic:

```python
@validator('published_year')
def validate_published_year(cls, v):
    if v < 1450 or v > CURRENT_YEAR:
        raise ValueError('Published year must be between 1450 and current year')
    return v
```

---

## 📁 Project Structure

```
.
├── crud.py             # FastAPI application
├── models.py           # SQLAlchemy models
├── db.py               # Database setup
├── test_main.py        # Unit tests (pytest)
├── requirements.txt    # Project dependencies
└── README.md           # Project documentation
```

---

## 🧪 Run Tests

```bash
pytest test_main.py
```

---

## 👤 Author

**Zain Kiyani**

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
Free to use for learning or production.
