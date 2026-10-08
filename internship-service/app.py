import datetime
import os
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, create_engine, or_
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./internships.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI(title="Internship Service", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Internship(Base):
    __tablename__ = "internships"
    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    company = Column(String, nullable=False)
    location = Column(String)
    description = Column(Text)
    stipend = Column(String, default="Paid")
    status = Column(String, default="open")  # open / closed
    deadline = Column(String, default="Rolling")

Base.metadata.create_all(engine)

class InternshipInput(BaseModel):
    title: str
    company: str
    location: str | None = None
    description: str | None = None
    stipend: str | None = "Paid"
    status: str | None = "open"
    deadline: str | None = "Rolling"

def out(x):
    return {
        "id": x.id,
        "title": x.title,
        "company": x.company,
        "location": x.location,
        "description": x.description,
        "stipend": x.stipend or "Paid",
        "status": x.status or "open",
        "deadline": x.deadline or "Rolling"
    }

@app.get("/")
def home():
    return {
        "service": "internship-service",
        "status": "running",
        "version": "2.0.0",
        "endpoints": ["/health", "/internships", "/internships/stats", "/internships/{id}"]
    }

@app.get("/health")
def health():
    db = Session()
    try:
        total = db.query(Internship).count()
        open_count = db.query(Internship).filter_by(status="open").count()
        return {
            "status": "healthy",
            "service": "internship-service",
            "database": "connected",
            "total_internships": total,
            "open_internships": open_count,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    finally:
        db.close()

@app.get("/internships/stats")
def stats():
    db = Session()
    try:
        total = db.query(Internship).count()
        open_count = db.query(Internship).filter_by(status="open").count()
        closed_count = total - open_count
        return {
            "total_internships": total,
            "open_internships": open_count,
            "closed_internships": closed_count
        }
    finally:
        db.close()

@app.post("/internships")
def create(data: InternshipInput):
    db = Session()
    try:
        x = Internship(**data.model_dump())
        db.add(x)
        db.commit()
        db.refresh(x)
        return out(x)
    finally:
        db.close()

@app.get("/internships")
def list_all(
    search: str | None = Query(None, description="Search across title, company, or description"),
    status: str | None = Query(None, description="Filter by status (open/closed)"),
    location: str | None = Query(None, description="Filter by location (e.g. Remote)"),
    company: str | None = Query(None, description="Filter by company name")
):
    db = Session()
    try:
        q = db.query(Internship)
        if status:
            q = q.filter(Internship.status.ilike(status))
        if location:
            q = q.filter(Internship.location.ilike(f"%{location}%"))
        if company:
            q = q.filter(Internship.company.ilike(f"%{company}%"))
        if search:
            p = f"%{search}%"
            q = q.filter(or_(
                Internship.title.ilike(p),
                Internship.company.ilike(p),
                Internship.location.ilike(p),
                Internship.description.ilike(p)
            ))
        return [out(x) for x in q.order_by(Internship.id).all()]
    finally:
        db.close()

@app.get("/internships/{internship_id}")
def get_one(internship_id: int):
    db = Session()
    try:
        x = db.query(Internship).filter_by(id=internship_id).first()
        if not x:
            raise HTTPException(404, "Internship not found")
        return out(x)
    finally:
        db.close()

@app.put("/internships/{internship_id}")
def update(internship_id: int, data: InternshipInput):
    db = Session()
    try:
        x = db.query(Internship).filter_by(id=internship_id).first()
        if not x:
            raise HTTPException(404, "Internship not found")
        for k, v in data.model_dump().items():
            setattr(x, k, v)
        db.commit()
        db.refresh(x)
        return out(x)
    finally:
        db.close()

@app.delete("/internships/{internship_id}")
def delete(internship_id: int):
    db = Session()
    try:
        x = db.query(Internship).filter_by(id=internship_id).first()
        if not x:
            raise HTTPException(404, "Internship not found")
        db.delete(x)
        db.commit()
        return {"message": "Internship deleted", "id": internship_id}
    finally:
        db.close()
