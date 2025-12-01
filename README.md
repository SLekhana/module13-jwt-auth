# Module 13: JWT Authentication with Playwright E2E Testing

[![CI/CD Pipeline](https://github.com/SLekhana/module13-jwt-auth/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/SLekhana/module13-jwt-auth/actions)

## Overview
This project implements JWT-based authentication with user registration and login functionality, including client-side validation, comprehensive Playwright E2E tests, and a fully automated CI/CD pipeline.

## Features
- ✅ JWT-based authentication (python-jose)
- ✅ Secure password hashing (bcrypt)
- ✅ User registration with duplicate email prevention
- ✅ User login with credential verification
- ✅ Client-side form validation (JavaScript)
- ✅ Server-side validation (Pydantic)
- ✅ Responsive frontend (HTML/CSS/JavaScript)
- ✅ Playwright E2E tests (7 test cases)
- ✅ CI/CD pipeline (GitHub Actions)
- ✅ Automated Docker Hub deployment

## Tech Stack
- **Backend**: FastAPI, SQLAlchemy, PostgreSQL
- **Authentication**: JWT (python-jose), bcrypt (passlib)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Testing**: Playwright, pytest, pytest-asyncio
- **DevOps**: Docker, Docker Compose, GitHub Actions

## Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/SLekhana/module13-jwt-auth.git
cd module13-jwt-auth
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
playwright install chromium
```

4. **Start PostgreSQL**
```bash
docker-compose up -d db
```

5. **Run the application**
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

6. **Access the application**
- Home: http://localhost:8000
- Register: http://localhost:8000/register-page
- Login: http://localhost:8000/login-page
- API Docs: http://localhost:8000/docs

## Running Tests

**Run all E2E tests:**
```bash
pytest tests/e2e/test_auth.py -v
```

**Run with detailed output:**
```bash
pytest tests/e2e/test_auth.py -v -s
```

**Expected output:**
```
tests/e2e/test_auth.py::test_register_with_valid_data PASSED           [ 14%]
tests/e2e/test_auth.py::test_register_with_short_password PASSED       [ 28%]
tests/e2e/test_auth.py::test_register_with_invalid_email PASSED        [ 42%]
tests/e2e/test_auth.py::test_register_with_mismatched_passwords PASSED [ 57%]
tests/e2e/test_auth.py::test_login_with_correct_credentials PASSED     [ 71%]
tests/e2e/test_auth.py::test_login_with_wrong_password PASSED          [ 85%]
tests/e2e/test_auth.py::test_login_with_invalid_email_format PASSED    [100%]

========================= 7 passed in 20.66s =========================
```

## API Endpoints

### POST /register
Register a new user

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Response (400 Bad Request):**
```json
{
  "detail": "Email already registered"
}
```

---

### POST /login
Authenticate user and receive JWT token

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Incorrect email or password"
}
```

---

### GET /health
Health check endpoint

**Response (200 OK):**
```json
{
  "status": "healthy"
}
```

## Client-Side Validation

### Registration Form
- ✅ Valid email format (RFC 5322 compliant)
- ✅ Password minimum 8 characters
- ✅ Password confirmation must match
- ✅ Real-time error messages
- ✅ Visual feedback for invalid inputs

### Login Form
- ✅ Valid email format
- ✅ Password required
- ✅ Clear error messages
- ✅ User-friendly UI feedback

## E2E Test Coverage

All tests use Playwright for browser automation and cover both positive and negative scenarios:

### Positive Test Cases
1. ✅ **test_register_with_valid_data** - Successful user registration with valid email and password
2. ✅ **test_login_with_correct_credentials** - Successful login with correct credentials

### Negative Test Cases
3. ✅ **test_register_with_short_password** - Registration fails with password < 8 characters
4. ✅ **test_register_with_invalid_email** - Registration fails with invalid email format
5. ✅ **test_register_with_mismatched_passwords** - Registration fails when passwords don't match
6. ✅ **test_login_with_wrong_password** - Login fails with incorrect password
7. ✅ **test_login_with_invalid_email_format** - Login fails with invalid email format

## Docker Deployment

### Using Docker Compose

**Build and run:**
```bash
docker-compose up --build
```

**Access:** http://localhost:8000

**Stop services:**
```bash
docker-compose down
```

**Clean up (including volumes):**
```bash
docker-compose down -v
```

### Using Docker Hub Image

**Pull image:**
```bash
docker pull lekhanasandra/module13-jwt-auth:latest
```

**Run container:**
```bash
docker run -p 8000:8000 \
  -e DATABASE_URL=postgresql://testuser:testpass@host.docker.internal:5432/testdb \
  -e SECRET_KEY=your-secret-key \
  lekhanasandra/module13-jwt-auth:latest
```

## CI/CD Pipeline

The GitHub Actions workflow automatically executes on every push to `main` branch:

### Pipeline Steps:
1. ✅ **Checkout code** - Retrieves latest code from repository
2. ✅ **Set up Python 3.11** - Configures Python environment
3. ✅ **Install dependencies** - Installs all required packages
4. ✅ **Start PostgreSQL** - Spins up database service
5. ✅ **Install Playwright** - Sets up browser automation
6. ✅ **Start FastAPI application** - Launches the web server
7. ✅ **Run Playwright E2E tests** - Executes all 7 test cases
8. ✅ **Build Docker image** - Creates container image
9. ✅ **Push to Docker Hub** - Deploys image to registry (on success)

**Workflow file:** `.github/workflows/ci-cd.yml`

**View workflow runs:** https://github.com/SLekhana/module13-jwt-auth/actions

## Docker Hub

**Repository:** https://hub.docker.com/r/lekhanasandra/module13-jwt-auth

**Latest tag:** `lekhanasandra/module13-jwt-auth:latest`

## Environment Variables

Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://testuser:testpass@localhost:5432/testdb
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Important:** Never commit `.env` to version control!

## Security Features

- 🔒 **Password Hashing**: bcrypt with cost factor 12
- 🔒 **JWT Tokens**: HS256 algorithm with expiration
- 🔒 **Token Expiration**: 30-minute validity period
- 🔒 **Secure Storage**: No plaintext passwords in database
- 🔒 **Email Uniqueness**: Prevents duplicate accounts
- 🔒 **SQL Injection Prevention**: SQLAlchemy ORM parameterization
- 🔒 **Input Validation**: Client-side and server-side validation
- 🔒 **HTTPS Ready**: Production-ready security configuration

## Project Structure
```
module13-jwt-auth/
├── app/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # FastAPI application & routes
│   ├── auth.py              # JWT & password hashing logic
│   ├── models.py            # SQLAlchemy database models
│   ├── schemas.py           # Pydantic validation schemas
│   └── database.py          # Database configuration
├── templates/
│   ├── register.html        # User registration page
│   └── login.html           # User login page
├── static/
│   ├── styles.css           # Shared CSS styles
│   ├── register.js          # Registration form logic
│   └── login.js             # Login form logic
├── tests/
│   ├── conftest.py          # Pytest fixtures & configuration
│   └── e2e/
│       └── test_auth.py     # Playwright E2E test suite
├── .github/
│   └── workflows/
│       └── ci-cd.yml        # GitHub Actions CI/CD pipeline
├── screenshots/             # Screenshots for submission
├── Dockerfile               # Container image definition
├── docker-compose.yml       # Multi-service orchestration
├── requirements.txt         # Python dependencies
├── pytest.ini               # Pytest configuration
├── .env                     # Environment variables (not in git)
├── .gitignore              # Git ignore patterns
├── README.md               # This file
└── REFLECTION.md           # Project reflection document
```

## Troubleshooting

### Database Connection Issues
```bash
# Restart PostgreSQL container
docker-compose down -v
docker-compose up -d db

# Check database is running
docker-compose ps
```

### Port Already in Use
```bash
# macOS/Linux: Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Windows: Find and kill process
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

### Playwright Browser Issues
```bash
# Reinstall Chromium browser
playwright install chromium --force

# Install system dependencies
playwright install-deps
```

### bcrypt Compatibility Issues
```bash
# If you encounter bcrypt errors with Python 3.13
pip uninstall bcrypt -y
pip install bcrypt==4.0.1
```

## Development Workflow

1. **Create feature branch**
```bash
git checkout -b feature/your-feature-name
```

2. **Make changes and test locally**
```bash
pytest tests/e2e/test_auth.py -v
```

3. **Commit and push**
```bash
git add .
git commit -m "Add your feature description"
git push origin feature/your-feature-name
```

4. **Create Pull Request** on GitHub

5. **CI/CD runs automatically** - Tests must pass before merge

## Screenshots

See `screenshots/` directory for:
- ✅ GitHub Actions workflow passing
- ✅ All 7 Playwright tests passing
- ✅ Registration page UI
- ✅ Login page UI  
- ✅ Successful registration with token
- ✅ Successful login with token

## Author

**Lekhana Sandra**  
Master's in Data Science  
New Jersey Institute of Technology (NJIT)

## Course Information

- **Course**: IS 601 - Python for Web API Development
- **Module**: 13 - JWT Authentication & Playwright E2E Testing
- **Semester**: Fall 2024

## License

MIT License - See LICENSE file for details

## Acknowledgments

- FastAPI documentation and community
- Playwright testing framework
- SQLAlchemy ORM
- JWT.io for token visualization
- Docker and Docker Hub
- GitHub Actions for CI/CD

## Links

- **GitHub Repository**: https://github.com/SLekhana/module13-jwt-auth
- **Docker Hub**: https://hub.docker.com/r/lekhanasandra/module13-jwt-auth
- **FastAPI Docs**: https://fastapi.tiangolo.com/
- **Playwright Docs**: https://playwright.dev/python/
