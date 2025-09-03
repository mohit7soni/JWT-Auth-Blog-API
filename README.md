JWT-Auth-Blog-API

A FastAPI-based backend project that demonstrates secure user authentication and CRUD operations with MySQL.
This project is designed as a mini blog system where users can register, log in, and create or view posts using JWT authentication.

✨ Features

🔑 JWT Authentication – Secure login with token-based auth

🔒 Password Hashing – User credentials stored securely with bcrypt

👤 User Management – Register new users & fetch user details

📝 Post Management – Create and read posts linked to users

🗄️ MySQL + SQLAlchemy ORM – Relational database integration

⚡ FastAPI Router – Modular and scalable API design

🛠️ Tech Stack

Python 3.10+

FastAPI (Backend Framework)

SQLAlchemy (ORM)

MySQL (Database)

JWT (JOSE) for Authentication

Passlib (bcrypt) for Password Hashing

🚀 Setup Instructions

Clone the repo

git clone https://github.com/mohit7soni/JWT-Auth-Blog-API.git
cd JWT-Auth-Blog-API


Create and activate virtual environment

python -m venv env
source env/Scripts/activate   # Windows
source env/bin/activate       # Linux/Mac


Install dependencies

pip install -r requirements.txt


Configure MySQL Database in database.py

Run the FastAPI server

uvicorn main:app --reload


Open API Docs in your browser

Swagger UI → http://127.0.0.1:8000/docs

Redoc → http://127.0.0.1:8000/redoc

📌 API Endpoints
Auth Routes

POST /auth/ → Register user

POST /auth/token → Login & get JWT

User Routes

POST /users/ → Create user

GET /users/{id} → Get user by ID

Post Routes

POST /posts/ → Create a post

GET /posts/{id} → Get post by ID

🔮 Future Improvements

✅ Role-based access (Admin/User)

✅ Update & delete endpoints for posts/users

✅ Refresh tokens for long sessions

✅ Docker setup for deployment
