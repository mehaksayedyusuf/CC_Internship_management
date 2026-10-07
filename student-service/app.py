
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker
import os

engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///./students.db"),
                       connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()
app = FastAPI(title="Student Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Student(Base):
    __tablename__ = "students"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    department = Column(String)
    year = Column(Integer)

Base.metadata.create_all(engine)

class StudentInput(BaseModel):
    name: str
    email: EmailStr
    department: str | None = None
    year: int | None = None

def out(s):
    return {"id": s.id, "name": s.name, "email": s.email,
            "department": s.department, "year": s.year}

@app.get("/")
def home():
    return {"service": "student", "message": "running"}

@app.post("/students")
def create(data: StudentInput):
    db = Session()
    try:
        if db.query(Student).filter_by(email=data.email).first():
            raise HTTPException(409, "Student email already exists")
        s = Student(**data.model_dump()); db.add(s); db.commit(); db.refresh(s)
        return out(s)
    finally:
        db.close()

@app.get("/students")
def list_all():
    db = Session()
    try:
        return [out(s) for s in db.query(Student).order_by(Student.id).all()]
    finally:
        db.close()

@app.get("/students/{student_id}")
def get_one(student_id: int):
    db = Session()
    try:
        s = db.query(Student).filter_by(id=student_id).first()
        if not s: raise HTTPException(404, "Student not found")
        return out(s)
    finally:
        db.close()

@app.put("/students/{student_id}")
def update(student_id: int, data: StudentInput):
    db = Session()
    try:
        s = db.query(Student).filter_by(id=student_id).first()
        if not s: raise HTTPException(404, "Student not found")
        for k, v in data.model_dump().items(): setattr(s, k, v)
        db.commit(); db.refresh(s); return out(s)
    finally:
        db.close()

@app.delete("/students/{student_id}")
def delete(student_id: int):
    db = Session()
    try:
        s = db.query(Student).filter_by(id=student_id).first()
        if not s: raise HTTPException(404, "Student not found")
        db.delete(s); db.commit()
        return {"message": "Student deleted"}
    finally:
        db.close()
