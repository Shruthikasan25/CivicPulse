import json, os, subprocess
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/incidents", tags=["AI Pipeline"])

AI_MODULE_DIR = Path(os.getenv("AI_MODULE_DIR", "../AI")).resolve()
AI_PYTHON = os.getenv("AI_PYTHON_PATH", "python")
INCIDENTS_JSON = AI_MODULE_DIR / "data" / "processed" / "incidents.json"

@router.post("/run-pipeline")
def run_ai_pipeline():
    try:
        result = subprocess.run(
            [AI_PYTHON, "pipeline.py"],
            cwd=str(AI_MODULE_DIR),
            capture_output=True, text=True, timeout=120,
        )
    except FileNotFoundError:
        raise HTTPException(500, f"Python interpreter not found: '{AI_PYTHON}'")
    except subprocess.TimeoutExpired:
        raise HTTPException(504, "AI pipeline timed out")

    if result.returncode != 0:
        raise HTTPException(500, f"AI pipeline failed:\n{result.stderr}")
    if not INCIDENTS_JSON.exists():
        raise HTTPException(500, "Pipeline ran but incidents.json was not produced")

    with open(INCIDENTS_JSON) as f:
        return json.load(f)

@router.get("/live")
def get_live_incidents():
    if not INCIDENTS_JSON.exists():
        raise HTTPException(404, "No incidents yet — call POST /incidents/run-pipeline first")
    with open(INCIDENTS_JSON) as f:
        return json.load(f)