from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

app = FastAPI()

# Database setup
DATABASE_URL = "sqlite:///./cybersecurity.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    Base.metadata.create_all(bind=engine)

# Models
class Threat(Base):
    __tablename__ = "threats"
    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, index=True)
    severity = Column(String)
    description = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class UserActivityLog(Base):
    __tablename__ = "user_activity_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    activity = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

class NetworkTraffic(Base):
    __tablename__ = "network_traffic"
    id = Column(Integer, primary_key=True, index=True)
    source_ip = Column(String)
    destination_ip = Column(String)
    data_transferred = Column(Integer)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

# Initialize database
init_db()

# Seed data
with SessionLocal() as session:
    if not session.query(Threat).first():
        session.add_all([
            Threat(type="Malware", severity="High", description="Detected malware activity."),
            Threat(type="Phishing", severity="Medium", description="Phishing attempt detected.")
        ])
        session.commit()

# Static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Routes
@app.get("/", response_class=HTMLResponse)
async def read_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/threats", response_class=HTMLResponse)
async def read_threats(request: Request):
    with SessionLocal() as session:
        threats = session.query(Threat).all()
    return templates.TemplateResponse("threats.html", {"request": request, "threats": threats})

@app.get("/logs", response_class=HTMLResponse)
async def read_logs(request: Request):
    with SessionLocal() as session:
        logs = session.query(UserActivityLog).all()
    return templates.TemplateResponse("logs.html", {"request": request, "logs": logs})

@app.get("/network", response_class=HTMLResponse)
async def read_network(request: Request):
    with SessionLocal() as session:
        network_traffic = session.query(NetworkTraffic).all()
    return templates.TemplateResponse("network.html", {"request": request, "network_traffic": network_traffic})

@app.get("/settings", response_class=HTMLResponse)
async def read_settings(request: Request):
    return templates.TemplateResponse("settings.html", {"request": request})

# API Endpoints
@app.get("/api/threats")
async def get_threats():
    with SessionLocal() as session:
        threats = session.query(Threat).all()
    return threats

@app.get("/api/logs")
async def get_logs():
    with SessionLocal() as session:
        logs = session.query(UserActivityLog).all()
    return logs

@app.get("/api/network")
async def get_network():
    with SessionLocal() as session:
        network_traffic = session.query(NetworkTraffic).all()
    return network_traffic

@app.post("/api/settings")
async def update_settings(settings: dict):
    # Update settings logic
    return {"status": "Settings updated"}

@app.get("/api/system-health")
async def get_system_health():
    # System health logic
    return {"status": "Healthy"}
