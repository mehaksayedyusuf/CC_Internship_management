from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
from passlib.context import CryptContext
import os

engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///./auth.db"),
                       connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")
app = FastAPI(title="Auth Service")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)

Base.metadata.create_all(engine)

class Register(BaseModel):
    name: str
    email: EmailStr
    password: str

class Login(BaseModel):
    email: EmailStr
    password: str

@app.get("/")
def home():
    return {"service": "auth", "message": "running"}

@app.post("/register")
def register(data: Register):
    db = Session()
    try:
        if db.query(User).filter_by(email=data.email).first():
            raise HTTPException(409, "Email already registered")
        user = User(name=data.name, email=data.email, password_hash=pwd.hash(data.password))
        db.add(user); db.commit(); db.refresh(user)
        return {"id": user.id, "name": user.name, "email": user.email}
    finally:
        db.close()

@app.post("/login")
def login(data: Login):
    db = Session()
    try:
        user = db.query(User).filter_by(email=data.email).first()
        if not user or not pwd.verify(data.password, user.password_hash):
            raise HTTPException(401, "Invalid email or password")
        return {"message": "Login successful", "user_id": user.id}
    finally:
        db.close()
