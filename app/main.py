from fastapi import FastAPI
from .routers import reports, incidents, crews, dispatches,ai_pipeline
from . import models
from . import incident_models
from . import crew_models
from . import dispatch_models

app = FastAPI(
    title="CivicPulse API",
    description="Backend API for CivicPulse water incident intelligence",
    version="1.0.0"
)
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reports.router)
app.include_router(ai_pipeline.router)
app.include_router(incidents.router)
app.include_router(crews.router)
app.include_router(dispatches.router)

@app.get("/")
def root():
    return {"message": "CivicPulse API is running"}
