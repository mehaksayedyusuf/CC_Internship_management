import datetime
import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, Integer, String, create_engine, or_
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./students.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI(title="Student Service", version="2.0.0")

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
    skills = Column(String, default="")

Base.metadata.create_all(engine)

class StudentInput(BaseModel):
    name: str
    email: EmailStr
    department: str | None = None
    year: int | None = None
    skills: str | None = ""

def out(s):
    return {
        "id": s.id,
        "name": s.name,
        "email": s.email,
        "department": s.department,
        "year": s.year,
        "skills": s.skills or ""
    }

@app.get("/")
def home():
    return {
        "service": "student-service",
        "status": "running",
        "version": "2.0.0",
        "endpoints": ["/health", "/students", "/students/stats", "/students/{id}"]
    }

@app.get("/health")
def health():
    db = Session()
    try:
        count = db.query(Student).count()
        return {
            "status": "healthy",
            "service": "student-service",
            "database": "connected",
            "total_students": count,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    finally:
        db.close()

@app.get("/students/stats")
def stats():
    db = Session()
    try:
        students = db.query(Student).all()
        by_dept = {}
        for s in students:
            d = s.department or "Unknown"
            by_dept[d] = by_dept.get(d, 0) + 1
        return {
            "total_students": len(students),
            "by_department": by_dept
        }
    finally:
        db.close()

@app.post("/students")
def create(data: StudentInput):
    db = Session()
    try:
        if db.query(Student).filter_by(email=data.email).first():
            raise HTTPException(409, "Student email already exists")
        s = Student(**data.model_dump())
        db.add(s)
        db.commit()
        db.refresh(s)
        return out(s)
    finally:
        db.close()

@app.get("/students")
def list_all(
    department: str | None = Query(None, description="Filter by department"),
    year: int | None = Query(None, description="Filter by academic year"),
    search: str | None = Query(None, description="Search by name or email")
):
    db = Session()
    try:
        q = db.query(Student)
        if department:
            q = q.filter(Student.department.ilike(department))
        if year is not None:
            q = q.filter(Student.year == year)
        if search:
            p = f"%{search}%"
            q = q.filter(or_(Student.name.ilike(p), Student.email.ilike(p)))
        return [out(s) for s in q.order_by(Student.id).all()]
    finally:
        db.close()

@app.get("/students/{student_id}")
def get_one(student_id: int):
    db = Session()
    try:
        s = db.query(Student).filter_by(id=student_id).first()
        if not s:
            raise HTTPException(404, "Student not found")
        return out(s)
    finally:
        db.close()

@app.put("/students/{student_id}")
def update(student_id: int, data: StudentInput):
    db = Session()
    try:
        s = db.query(Student).filter_by(id=student_id).first()
        if not s:
            raise HTTPException(404, "Student not found")
        for k, v in data.model_dump().items():
            setattr(s, k, v)
        db.commit()
        db.refresh(s)
        return out(s)
    finally:
        db.close()

@app.delete("/students/{student_id}")
def delete(student_id: int):
    db = Session()
    try:
        s = db.query(Student).filter_by(id=student_id).first()
        if not s:
            raise HTTPException(404, "Student not found")
        db.delete(s)
        db.commit()
        return {"message": "Student deleted", "id": student_id}
    finally:
        db.close()
