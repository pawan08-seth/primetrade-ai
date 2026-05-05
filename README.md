# Primetrade_AI 🔐

A **production-ready FastAPI backend** implementing JWT authentication, Role-Based Access Control (RBAC), and secure CRUD operations using SQLAlchemy and SQLite. Designed to demonstrate real-world backend engineering concepts including authentication, authorization, dependency injection, database modeling, and secure API design.

---

## ✨ Features

- **JWT Authentication** — Secure token-based login with access token generation and validation
- **Role-Based Access Control (RBAC)** — Fine-grained route protection based on user roles (e.g., `Admin`, `User`,`Analyst`)
- **CRUD Operations** — Full Create, Read, Update, Delete support with SQLAlchemy ORM
- **SQLite Database** — Lightweight, zero-config database setup via SQLAlchemy
- **Dependency Injection** — Clean, modular FastAPI dependency structure for auth and DB sessions
- **Modular Architecture** — Organized into separate modules for Auth, API routes, Models, and Database
- **Interactive API Docs** — Auto-generated Swagger UI at `/docs` and ReDoc at `/redoc`

---

## 🗂️ Project Structure

```
Primetrade_AI/
├── main.py           # FastAPI app entry point, router registration
├── Auth/
│   └── Auth_routes.py    # Authentication routes (register, login, token)
├── api/
│   └── api.py            # Protected CRUD API routes
├── Models/               # SQLAlchemy ORM models & Pydantic schemas
├── Database/             # Database session, engine, and base setup
└── requirements.txt      # Python dependencies
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- `pip`

### Installation

```bash
# Clone the repository
git clone https://github.com/adarshbaghel612/Primetrade_AI.git
cd Primetrade_AI

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # macOS/Linux
# venv\Scripts\activate         # Windows

# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
uvicorn main:app --reload or python -m uvicorn main:app --reload
```


The API will be live at **http://127.0.0.1:8000**

---

## 📖 API Documentation

Once the server is running, visit:

| Interface | URL |
|-----------|-----|
| Swagger UI | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |
| ReDoc | [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) |

---

## 🔑 Authentication Flow

1. **Register** — Create a new user account with a role (`Admin`,`Analyst` or `User`),you can select more than one role for your account like["User","Analyst"].By this you can perform operation that both user and analyst can do.
2. **Login** — Receive a signed JWT access token
3. **Access Protected Routes** — Pass the token as a Bearer header

```http
Authorization: Bearer <your_token>
```

---

## 🛡️ Role-Based Access Control

Routes are protected using FastAPI dependency injection. Role checks happen automatically before the handler executes.

| Role    | Permissions                          |
|---------|--------------------------------------|
| `Admin` | Full access — all CRUD operations    |
| `User`  | Read access — view own resources     |
|`Analyst`| Moderate Access — less than Admin    |

---

## 🧰 Tech Stack

| Technology | Purpose |
|------------|---------|
| [FastAPI](https://fastapi.tiangolo.com/) | Web framework & API routing |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM & database modeling |
| [SQLite](https://www.sqlite.org/) | Lightweight relational database |
| [PyJWT](https://pyjwt.readthedocs.io/) | JWT token generation & validation |
| [Passlib / bcrypt](https://passlib.readthedocs.io/) | Password hashing |
| [Pydantic](https://docs.pydantic.dev/) | Request/response data validation |

---

## 🧑‍💻 Key Concepts Demonstrated

- **Authentication vs Authorization** — JWT handles who you are; RBAC handles what you can do
- **Dependency Injection** — Database sessions and current-user resolution via `Depends()`
- **ORM Modeling** — SQLAlchemy declarative models with relationships
- **Secure API Design** — Hashed passwords, token expiry, and role-gated endpoints
- **Modular FastAPI** — Clean router separation with `include_router()`

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m 'Add my feature'`
4. Push to the branch: `git push origin feature/my-feature`
5. Open a Pull Request

---

## 📄 License

This project is open-source. See the [LICENSE](LICENSE) file for details.

---

> Built with ❤️ to demonstrate production-grade backend patterns using FastAPI.
