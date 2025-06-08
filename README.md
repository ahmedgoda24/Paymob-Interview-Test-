# Paymob Interview Project

This is a Django-based project that includes REST APIs, testing with pytest, and load testing with Locust.

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Virtual environment (recommended)

## Project Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd paymob-interview
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
python manage.py migrate
```

5. Create a superuser (optional):
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

The server will start at `http://127.0.0.1:8000/`

## Testing
#### Unit Tests
- Located in `task/tests/` 
- Covers:
  - Model validation
  - Serializer logic
```bash
python manage.py test
```

### Running Unit Tests with pytest

The project uses pytest for testing. To run the tests:

```bash
# Run all tests
pytest

# Run tests with coverage report
pytest --cov=.

# Run specific test file
pytest path/to/test_file.py

# Run tests with verbose output
pytest -v
```


### Load Testing with Locust

The project includes Locust for load testing. To run load tests:

1. Install Locust (if not already installed):
```bash
pip install locust
```

2. Run Locust:
```bash
# General API load testing
locust -f locustfiles/locustfile.py
# Product endpoints load testing
locust -f locustfiles/products.py
### Load Testing with Locust

```

3. Open your browser and go to `http://localhost:8089`
4. Configure the number of users and spawn rate
5. Start the load test

## Project Structure

```
paymob-interview/
├── locustfiles/        # Locust load testing files
├── task/              # Main application directory
├── task1/             # Additional task directory
├── paymob/            # Project settings
├── manage.py          # Django management script
├── requirements.txt   # Project dependencies
└── pytest.ini        # pytest configuration
```

## Features

- Django REST Framework APIs
- Unit testing with pytest
- Load testing with Locust
- SQLite database (can be configured for other databases)
- Django admin interface

## API Documentation

### Base URL: `http://127.0.0.1:8000/api/`


#### Key Functionality:
1. **Optimized Product Queries**
   - Fetches top 10 most expensive products in each category
   - Uses Django ORM annotations and subqueries
   - Implements efficient querying to avoid N+1 problems
   - Optimized for large datasets

2. **Category Analytics**
   - Annotates products with category statistics
   - Provides total product count per category
   - Efficient aggregation using Django ORM

# 🛒 DRF Product API – Optimized ORM Queries

This Django REST Framework project demonstrates advanced ORM techniques and clean API design by exposing multiple endpoints related to **Products** and **Categories** using optimized queries, subqueries, and window functions.

---

## 🚀 Features

- ✅ Paginated product listing
- ✅ Top 10 most expensive products **per category**
- ✅ Top 10 most expensive products **globally**
- ✅ Each product annotated with the **number of products in its category**
- ✅ Highly optimized with `select_related`, `Window`, and `RowNumber`
- ✅ Custom DRF `@action`s with full pagination support
- ✅ Load testing via **Locust**
- ✅ Unit testing via **pytest + factory_boy**

---

## ⚙️ Tech Stack

- Python 3.x
- Django 4.x
- Django REST Framework
- PostgreSQL (for window functions)
- Pytest + Factory Boy
- Locust (for performance testing)

---

## 📂 API Endpoints

| Method | Endpoint                                              | Description |
|--------|-------------------------------------------------------|-------------|
| GET    | `/api/v1/task1/products/`                             | List all products (paginated) |
| GET    | `/api/v1/task1/products/top_most_expensive_by_category/` | Top 10 expensive products **per category** with counts |
| GET    | `/api/v1/task1/products/top_10_most_expensive/`       | Top 10 expensive products globally (sorted) |
| GET    | `/api/v1/task1/products/products_with_category_counts/` | All products with total products per category |

---

### Task 2: User Profile Management
Located in `task/` directory

This app implements advanced DRF serializers for user profile management:

#### Features:
- **UserProfile Model** with one-to-one relationship to Django User model
- Advanced validation and serialization
- Full nested support for `UserProfile` within `User`
- Custom validation for profile fields (e.g., bio length ≥ 50)
- Atomic create and update logic using `transaction.atomic()`
- Clean update via shared utility `CoreUtils.serializer_save()`

#### Key Functionality:
1. **Unified User Management**
   - Create/update User and UserProfile in a single request
   - Nested serializer implementation
   - Comprehensive validation:
     - Website URL validation
     - Bio field minimum length (50 characters)
   - Graceful error handling with detailed validation messages

2. **Profile Management**
   - Complete user profile CRUD operations
   - Custom validation rules
   - Secure data handling

## 👤 User & UserProfile API

This module demonstrates how to manage **nested user profile data** within Django REST Framework serializers using atomic transactions and reusable validation utilities.


---

### 🔗 Data Model Overview

- `User`: Standard Django `User` model
- `UserProfile`: One-to-one with `User`, fields: `website`, `bio`

---

### 📦 Serializer Behavior

| Action   | What Happens                                                |
|----------|-------------------------------------------------------------|
| `create` | Creates both `User` and `UserProfile` atomically            |
| `update` | Updates user fields and related `UserProfile` (if provided) |

---



## 🧪 Running Tests

Install test dependencies:

```bash
pip install pytest pytest-django factory_boy
Then run the tests:

pytest
Test data is generated using factory_boy.

🧪 Running Load Tests (Locust)


pip install locust


python manage.py runserver

locust
```