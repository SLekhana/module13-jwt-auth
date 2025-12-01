from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from sqlalchemy.orm import Session
from datetime import timedelta
from app.database import engine, get_db, Base
from app.schemas import UserRegister, UserLogin, Token, UserResponse
from app import auth
import os

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="JWT Auth API")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <body>
            <h1>JWT Authentication API</h1>
            <ul>
                <li><a href="/register-page">Register</a></li>
                <li><a href="/login-page">Login</a></li>
            </ul>
        </body>
    </html>
    """

@app.get("/register-page", response_class=HTMLResponse)
async def register_page():
    return FileResponse("templates/register.html")

@app.get("/login-page", response_class=HTMLResponse)
async def login_page():
    return FileResponse("templates/login.html")

@app.post("/register", response_model=Token, status_code=status.HTTP_201_CREATED)
async def register(user: UserRegister, db: Session = Depends(get_db)):
    # Check if user already exists
    db_user = auth.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    new_user = auth.create_user(db, user)
    
    # Create access token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": new_user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/login", response_model=Token)
async def login(user: UserLogin, db: Session = Depends(get_db)):
    # Authenticate user
    authenticated_user = auth.authenticate_user(db, user.email, user.password)
    if not authenticated_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create access token
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": authenticated_user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
