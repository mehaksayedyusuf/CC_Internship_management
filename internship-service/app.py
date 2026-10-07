from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, or_
from sqlalchemy.orm import declarative_base, sessionmaker
import os

engine = create_engine(os.getenv("DATABASE_URL", "sqlite:///./internships.db"),
                       connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()
app = FastAPI(title="Internship Service")

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

Base.metadata.create_all(engine)

class InternshipInput(BaseModel):
    title: str
    company: str
    location: str | None = None
    description: str | None = None

def out(x):
    return {"id": x.id, "title": x.title, "company": x.company,
            "location": x.location, "description": x.description}

@app.get("/")
def home():
    return {"service": "internship", "message": "running"}

@app.post("/internships")
def create(data: InternshipInput):
    db = Session()
    try:
        x = Internship(**data.model_dump()); db.add(x); db.commit(); db.refresh(x)
        return out(x)
    finally:
        db.close()

@app.get("/internships")
def list_all(search: str | None = None):
    db = Session()
    try:
        q = db.query(Internship)
        if search:
            p = f"%{search}%"
            q = q.filter(or_(Internship.title.ilike(p), Internship.company.ilike(p),
                             Internship.location.ilike(p)))
        return [out(x) for x in q.order_by(Internship.id).all()]
    finally:
        db.close()

@app.get("/internships/{internship_id}")
def get_one(internship_id: int):
    db = Session()
    try:
        x = db.query(Internship).filter_by(id=internship_id).first()
        if not x: raise HTTPException(404, "Internship not found")
        return out(x)
    finally:
        db.close()

@app.put("/internships/{internship_id}")
def update(internship_id: int, data: InternshipInput):
    db = Session()
    try:
        x = db.query(Internship).filter_by(id=internship_id).first()
        if not x: raise HTTPException(404, "Internship not found")
        for k, v in data.model_dump().items(): setattr(x, k, v)
        db.commit(); db.refresh(x); return out(x)
    finally:
        db.close()

@app.delete("/internships/{internship_id}")
def delete(internship_id: int):
    db = Session()
    try:
        x = db.query(Internship).filter_by(id=internship_id).first()
        if not x: raise HTTPException(404, "Internship not found")
        db.delete(x); db.commit()
        return {"message": "Internship deleted"}
    finally:
        db.close()

