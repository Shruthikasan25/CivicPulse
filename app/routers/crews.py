from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..database import get_db
from ..schemas import CrewStatusUpdate

router = APIRouter(prefix="/crews", tags=["Crews"])


@router.get("/")
def get_crews(db: Session = Depends(get_db)):
    result = db.execute(
        text("""
            SELECT
                id,
                name,
                capability,
                available,
                status,
                ST_Y(location) AS latitude,
                ST_X(location) AS longitude
            FROM crews
            ORDER BY id
        """)
    )

    crews = []

    for row in result:
        crews.append(dict(row._mapping))

    return crews


@router.get("/{crew_id}")
def get_crew(
    crew_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            SELECT
                id,
                name,
                capability,
                available,
                status,
                ST_Y(location) AS latitude,
                ST_X(location) AS longitude
            FROM crews
            WHERE id = :crew_id
        """),
        {"crew_id": crew_id}
    )

    row = result.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Crew not found"
        )

    return dict(row._mapping)
@router.patch("/{crew_id}/status")
def update_crew_status(
    crew_id: int,
    status_update: CrewStatusUpdate,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            UPDATE crews
            SET
                status = :status,
                available = COALESCE(:available, available)
            WHERE id = :crew_id
            RETURNING id, status, available
        """),
        {
            "crew_id": crew_id,
            "status": status_update.status,
            "available": status_update.available
        }
    )

    row = result.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Crew not found"
        )

    db.commit()

    return {
        "message": "Crew status updated successfully",
        "crew_id": row.id,
        "status": row.status,
        "available": row.available
    }