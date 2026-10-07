import os
import requests

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, UniqueConstraint, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

STUDENT_SERVICE_URL = os.getenv("STUDENT_SERVICE_URL", "http://localhost:8002")
INTERNSHIP_SERVICE_URL = os.getenv("INTERNSHIP_SERVICE_URL", "http://localhost:8003")

engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///./applications.db"),
                       connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()
app = FastAPI(title="Application Service")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("student_id", "internship_id"),)
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, nullable=False)
    internship_id = Column(Integer, nullable=False)
    status = Column(String, nullable=False, default="pending")

Base.metadata.create_all(engine)

class ApplyInput(BaseModel):
    student_id: int
    internship_id: int

class StatusInput(BaseModel):
    status: str

def out(x):
    return {"id": x.id, "student_id": x.student_id,
            "internship_id": x.internship_id, "status": x.status}

@app.get("/")
def home():
    return {"service": "application", "message": "running"}

def verify_student_exists(student_id: int):
    try:
        resp = requests.get(f"{STUDENT_SERVICE_URL}/students/{student_id}", timeout=5)
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Student {student_id} not found")
        elif resp.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Student service error: {resp.status_code}")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Unable to reach Student service: {str(e)}")

def verify_internship_exists(internship_id: int):
    try:
        resp = requests.get(f"{INTERNSHIP_SERVICE_URL}/internships/{internship_id}", timeout=5)
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Internship {internship_id} not found")
        elif resp.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Internship service error: {resp.status_code}")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Unable to reach Internship service: {str(e)}")

@app.post("/applications")
def apply(data: ApplyInput):
    # Inter-Service Communication: Validate student and internship existence
    verify_student_exists(data.student_id)
    verify_internship_exists(data.internship_id)

    db = Session()
    try:
        existing = db.query(Application).filter_by(
            student_id=data.student_id, internship_id=data.internship_id).first()
        if existing: raise HTTPException(409, "Already applied to this internship")
        x = Application(student_id=data.student_id, internship_id=data.internship_id)
        db.add(x); db.commit(); db.refresh(x); return out(x)
    finally:
        db.close()

@app.get("/applications")
def list_all(student_id: int | None = None):
    db = Session()
    try:
        q = db.query(Application)
        if student_id is not None: q = q.filter_by(student_id=student_id)
        return [out(x) for x in q.order_by(Application.id).all()]
    finally:
        db.close()

@app.patch("/applications/{application_id}/status")
def update_status(application_id: int, data: StatusInput):
    if data.status not in {"pending", "accepted", "rejected"}:
        raise HTTPException(400, "Status must be pending, accepted, or rejected")
    db = Session()
    try:
        x = db.query(Application).filter_by(id=application_id).first()
        if not x: raise HTTPException(404, "Application not found")
        x.status = data.status; db.commit(); db.refresh(x); return out(x)
    finally:
        db.close()

@app.delete("/applications/{application_id}")
def delete(application_id: int):
    db = Session()
    try:
        x = db.query(Application).filter_by(id=application_id).first()
        if not x: raise HTTPException(404, "Application not found")
        db.delete(x); db.commit()
        return {"message": "Application deleted"}
    finally:
        db.close()
