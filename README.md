# Django Auth API with JWT and Kafka Logging

This is a Django REST API project that supports user registration, login/logout using JWT tokens (SimpleJWT), secure profile view/update, and logs API usage events to Kafka. The project also includes Swagger UI for API documentation.

---

##  Features

- JWT Authentication (SimpleJWT)
- Registration, Login, Logout
- Profile view and update (via access token)
- Kafka event logging
- Swagger & ReDoc API documentation
- Change Password
---

## Requirements

- Python 3.8+
- Docker & Docker Compose
- Kafka & Zookeeper (via Docker)
- Python dependencies in `requirements.txt`

---

## Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/S-Mukherjee98/assignment.git
cd assignment
Create and activate a virtual environment
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python consumer.py(start the zookeeper and kafka server beforehand)


🔐 API Endpoints
Auth
POST /api/register/ – Register a new user

POST /api/login/ – Login and receive JWT tokens

POST /api/logout/ – Logout and blacklist the refresh token

POST /api/profile/ – To get the profile

POST /api/secure-data/ – simulation of kafka 

POST /api/rest-password/ – To reset the password

POST /api/test/ – Test API which returns a message only

Profile
GET /api/profile/ – View logged-in user's profile

PUT /api/profile/ – Update name and age

