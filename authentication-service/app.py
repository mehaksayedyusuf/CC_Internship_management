import datetime
import os
import jwt
from fastapi import FastAPI, HTTPException, Header, Query
from fastapi.middleware.cors import CORSMiddleware
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./auth.db")
JWT_SECRET = os.getenv("JWT_SECRET", "ims-secure-jwt-secret-key-2026")
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()
pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(title="Authentication Service", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="student", nullable=False)

Base.metadata.create_all(engine)

class Register(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "student"

class Login(BaseModel):
    email: EmailStr
    password: str

def create_access_token(user_id: int, email: str, role: str) -> str:
    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.datetime.now(datetime.timezone.utc)
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

@app.get("/")
def home():
    return {
        "service": "authentication-service",
        "status": "running",
        "version": "2.0.0",
        "endpoints": ["/health", "/register", "/login", "/verify-token", "/me"]
    }

@app.get("/health")
def health():
    db = Session()
    try:
        count = db.query(User).count()
        return {
            "status": "healthy",
            "service": "authentication-service",
            "database": "connected",
            "total_users": count,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    finally:
        db.close()

@app.post("/register")
def register(data: Register):
    db = Session()
    try:
        if db.query(User).filter_by(email=data.email).first():
            raise HTTPException(409, "Email already registered")
        user = User(
            name=data.name,
            email=data.email,
            password_hash=pwd.hash(data.password),
            role=data.role
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        token = create_access_token(user.id, user.email, user.role)
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "access_token": token,
            "token_type": "bearer"
        }
    finally:
        db.close()

@app.post("/login")
def login(data: Login):
    db = Session()
    try:
        user = db.query(User).filter_by(email=data.email).first()
        if not user or not pwd.verify(data.password, user.password_hash):
            raise HTTPException(401, "Invalid email or password")
        token = create_access_token(user.id, user.email, user.role)
        return {
            "message": "Login successful",
            "user_id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "access_token": token,
            "token_type": "bearer"
        }
    finally:
        db.close()

@app.get("/verify-token")
def verify_token(token: str = Query(...)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return {"valid": True, "claims": payload}
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")

@app.get("/me")
def get_current_user(authorization: str | None = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(401, "Missing or invalid authorization header")
    token = authorization.split(" ")[1]
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        db = Session()
        try:
            user = db.query(User).filter_by(id=int(payload["sub"])).first()
            if not user:
                raise HTTPException(404, "User not found")
            return {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "role": user.role
            }
        finally:
            db.close()
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(401, "Invalid token")
