from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text

from ..database import get_db
from ..schemas import IncidentUpdate

router = APIRouter(prefix="/incidents", tags=["Incidents"])


@router.get("/")
def get_incidents(db: Session = Depends(get_db)):
    result = db.execute(
        text("""
            SELECT
                id,
                location,
                radius,
                report_count,
                first_report,
                last_report,
                leak_probability,
                classification,
                severity,
                priority,
                status,
                recommended_action,
                created_at
            FROM incidents
            ORDER BY created_at DESC
        """)
    )

    incidents = []

    for row in result:
        incident = dict(row._mapping)

        # Convert PostGIS location into latitude/longitude
        location_result = db.execute(
            text("""
                SELECT
                    ST_Y(location) AS latitude,
                    ST_X(location) AS longitude
                FROM incidents
                WHERE id = :incident_id
            """),
            {"incident_id": incident["id"]}
        ).fetchone()

        if location_result:
            incident["latitude"] = location_result.latitude
            incident["longitude"] = location_result.longitude

        # Remove raw PostGIS geometry from JSON response
        incident.pop("location", None)

        incidents.append(incident)

    return incidents


@router.get("/{incident_id}")
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            SELECT
                id,
                radius,
                report_count,
                first_report,
                last_report,
                leak_probability,
                classification,
                severity,
                priority,
                status,
                recommended_action,
                created_at,
                ST_Y(location) AS latitude,
                ST_X(location) AS longitude
            FROM incidents
            WHERE id = :incident_id
        """),
        {"incident_id": incident_id}
    )

    row = result.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return dict(row._mapping)
@router.post("/")
def create_incident(
    latitude: float,
    longitude: float,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            INSERT INTO incidents (
                location,
                radius,
                report_count,
                status,
                created_at
            )
            VALUES (
                ST_SetSRID(
                    ST_MakePoint(:longitude, :latitude),
                    4326
                ),
                100,
                0,
                'new',
                CURRENT_TIMESTAMP
            )
            RETURNING id
        """),
        {
            "latitude": latitude,
            "longitude": longitude
        }
    )

    incident_id = result.scalar()

    db.commit()

    return {
        "message": "Incident created successfully",
        "incident_id": incident_id
    }
@router.patch("/{incident_id}")
def update_incident(
    incident_id: int,
    incident_update: IncidentUpdate,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            UPDATE incidents
            SET
                radius = COALESCE(:radius, radius),
                leak_probability = COALESCE(:leak_probability, leak_probability),
                classification = COALESCE(:classification, classification),
                severity = COALESCE(:severity, severity),
                priority = COALESCE(:priority, priority),
                status = COALESCE(:status, status),
                recommended_action = COALESCE(
                    :recommended_action,
                    recommended_action
                )
            WHERE id = :incident_id
            RETURNING id
        """),
        {
            "incident_id": incident_id,
            "radius": incident_update.radius,
            "leak_probability": incident_update.leak_probability,
            "classification": incident_update.classification,
            "severity": incident_update.severity,
            "priority": incident_update.priority,
            "status": incident_update.status,
            "recommended_action": incident_update.recommended_action
        }
    )

    row = result.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    db.commit()

    return {
        "message": "Incident updated successfully",
        "incident_id": row.id
    }
