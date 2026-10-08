import datetime
import os
import requests
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, UniqueConstraint, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

STUDENT_SERVICE_URL = os.getenv("STUDENT_SERVICE_URL", "http://localhost:8002")
INTERNSHIP_SERVICE_URL = os.getenv("INTERNSHIP_SERVICE_URL", "http://localhost:8003")
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./applications.db")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
Session = sessionmaker(bind=engine)
Base = declarative_base()

app = FastAPI(title="Application Service", version="2.0.0")

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
    applied_at = Column(String, default=lambda: datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S"))
    notes = Column(String, default="")

Base.metadata.create_all(engine)

class ApplyInput(BaseModel):
    student_id: int
    internship_id: int
    notes: str | None = ""

class StatusInput(BaseModel):
    status: str

def out(x):
    return {
        "id": x.id,
        "student_id": x.student_id,
        "internship_id": x.internship_id,
        "status": x.status,
        "applied_at": x.applied_at or "",
        "notes": x.notes or ""
    }

@app.get("/")
def home():
    return {
        "service": "application-service",
        "status": "running",
        "version": "2.0.0",
        "student_service_target": STUDENT_SERVICE_URL,
        "internship_service_target": INTERNSHIP_SERVICE_URL,
        "endpoints": ["/health", "/applications", "/applications/stats", "/applications/enriched"]
    }

@app.get("/health")
def health():
    db = Session()
    try:
        total = db.query(Application).count()
        return {
            "status": "healthy",
            "service": "application-service",
            "database": "connected",
            "total_applications": total,
            "connected_services": {
                "student_service": STUDENT_SERVICE_URL,
                "internship_service": INTERNSHIP_SERVICE_URL
            },
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    finally:
        db.close()

@app.get("/applications/stats")
def stats():
    db = Session()
    try:
        total = db.query(Application).count()
        pending = db.query(Application).filter_by(status="pending").count()
        accepted = db.query(Application).filter_by(status="accepted").count()
        rejected = db.query(Application).filter_by(status="rejected").count()
        return {
            "total_applications": total,
            "pending": pending,
            "accepted": accepted,
            "rejected": rejected
        }
    finally:
        db.close()

def verify_student_exists(student_id: int):
    try:
        resp = requests.get(f"{STUDENT_SERVICE_URL}/students/{student_id}", timeout=5)
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Student {student_id} not found in Student Service")
        elif resp.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Student service error: {resp.status_code}")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Unable to reach Student service: {str(e)}")

def verify_internship_exists(internship_id: int):
    try:
        resp = requests.get(f"{INTERNSHIP_SERVICE_URL}/internships/{internship_id}", timeout=5)
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Internship {internship_id} not found in Internship Service")
        elif resp.status_code != 200:
            raise HTTPException(status_code=502, detail=f"Internship service error: {resp.status_code}")
    except requests.RequestException as e:
        raise HTTPException(status_code=503, detail=f"Unable to reach Internship service: {str(e)}")

@app.post("/applications")
def apply(data: ApplyInput):
    # Inter-Service Communication Validation (Checkpoint 3 Core Requirement)
    verify_student_exists(data.student_id)
    verify_internship_exists(data.internship_id)

    db = Session()
    try:
        existing = db.query(Application).filter_by(
            student_id=data.student_id, internship_id=data.internship_id
        ).first()
        if existing:
            raise HTTPException(409, "Already applied to this internship")
        x = Application(
            student_id=data.student_id,
            internship_id=data.internship_id,
            notes=data.notes or ""
        )
        db.add(x)
        db.commit()
        db.refresh(x)
        return out(x)
    finally:
        db.close()

@app.get("/applications")
def list_all(
    student_id: int | None = Query(None, description="Filter by student ID"),
    internship_id: int | None = Query(None, description="Filter by internship ID"),
    status: str | None = Query(None, description="Filter by status (pending, accepted, rejected)")
):
    db = Session()
    try:
        q = db.query(Application)
        if student_id is not None:
            q = q.filter_by(student_id=student_id)
        if internship_id is not None:
            q = q.filter_by(internship_id=internship_id)
        if status:
            q = q.filter_by(status=status.lower())
        return [out(x) for x in q.order_by(Application.id).all()]
    finally:
        db.close()

@app.get("/applications/enriched")
def list_enriched():
    """Fetch applications and enrich with student names and internship titles over internal network."""
    db = Session()
    try:
        apps = db.query(Application).order_by(Application.id.desc()).all()
        enriched = []
        for a in apps:
            student_name = f"Student #{a.student_id}"
            internship_title = f"Internship #{a.internship_id}"
            company_name = "N/A"
            try:
                s_res = requests.get(f"{STUDENT_SERVICE_URL}/students/{a.student_id}", timeout=2)
                if s_res.ok:
                    student_name = s_res.json().get("name", student_name)
            except Exception:
                pass

            try:
                i_res = requests.get(f"{INTERNSHIP_SERVICE_URL}/internships/{a.internship_id}", timeout=2)
                if i_res.ok:
                    i_data = i_res.json()
                    internship_title = i_data.get("title", internship_title)
                    company_name = i_data.get("company", company_name)
            except Exception:
                pass

            record = out(a)
            record["student_name"] = student_name
            record["internship_title"] = internship_title
            record["company"] = company_name
            enriched.append(record)
        return enriched
    finally:
        db.close()

@app.get("/applications/{application_id}")
def get_one(application_id: int):
    db = Session()
    try:
        x = db.query(Application).filter_by(id=application_id).first()
        if not x:
            raise HTTPException(404, "Application not found")
        return out(x)
    finally:
        db.close()

@app.patch("/applications/{application_id}/status")
def update_status(application_id: int, data: StatusInput):
    clean_status = data.status.lower().strip()
    if clean_status not in {"pending", "accepted", "rejected"}:
        raise HTTPException(400, "Status must be pending, accepted, or rejected")
    db = Session()
    try:
        x = db.query(Application).filter_by(id=application_id).first()
        if not x:
            raise HTTPException(404, "Application not found")
        x.status = clean_status
        db.commit()
        db.refresh(x)
        return out(x)
    finally:
        db.close()

@app.delete("/applications/{application_id}")
def delete(application_id: int):
    db = Session()
    try:
        x = db.query(Application).filter_by(id=application_id).first()
        if not x:
            raise HTTPException(404, "Application not found")
        db.delete(x)
        db.commit()
        return {"message": "Application deleted", "id": application_id}
    finally:
        db.close()
