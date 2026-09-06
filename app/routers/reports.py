from fastapi import APIRouter, Depends,HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from ..database import get_db
from ..schemas import ReportCreate, ReportStatusUpdate, ReportIncidentUpdate


router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get("/")
def get_reports(db: Session = Depends(get_db)):
    result = db.execute(
        text("""
            SELECT
                id,
                description,
                classification,
                leak_probability,
                incident_id,
                status,
                created_at
            FROM reports
            ORDER BY created_at DESC
        """)
    )

    reports = []

    for row in result:
        reports.append(dict(row._mapping))

    return reports


@router.post("/")
def create_report(
    report: ReportCreate,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            INSERT INTO reports (
                timestamp,
                location,
                description,
                status,
                created_at
            )
            VALUES (
                CURRENT_TIMESTAMP,
                ST_SetSRID(
                    ST_MakePoint(:longitude, :latitude),
                    4326
                ),
                :description,
                'new',
                CURRENT_TIMESTAMP
            )
            RETURNING id
        """),
        {
            "latitude": report.latitude,
            "longitude": report.longitude,
            "description": report.description
        }
    )

    new_id = result.scalar()

    db.commit()

    return {
        "message": "Report created successfully",
        "report_id": new_id
    }
@router.get("/nearby")
def get_nearby_reports(
    latitude: float,
    longitude: float,
    radius: float = 100,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            SELECT
                id,
                description,
                classification,
                leak_probability,
                incident_id,
                status,
                created_at,
                ST_Distance(
                    location::geography,
                    ST_SetSRID(
                        ST_MakePoint(:longitude, :latitude),
                        4326
                    )::geography
                ) AS distance_meters
            FROM reports
            WHERE ST_DWithin(
                location::geography,
                ST_SetSRID(
                    ST_MakePoint(:longitude, :latitude),
                    4326
                )::geography,
                :radius
            )
            ORDER BY distance_meters
        """),
        {
            "latitude": latitude,
            "longitude": longitude,
            "radius": radius
        }
    )

    reports = []

    for row in result:
        reports.append(dict(row._mapping))

    return reports
@router.get("/{report_id}")
def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            SELECT
                id,
                description,
                classification,
                leak_probability,
                incident_id,
                status,
                created_at
            FROM reports
            WHERE id = :report_id
        """),
        {
            "report_id": report_id
        }
    )

    row = result.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return dict(row._mapping)
@router.patch("/{report_id}/status")
def update_report_status(
    report_id: int,
    status_update: ReportStatusUpdate,
    db: Session = Depends(get_db)
):
    result = db.execute(
        text("""
            UPDATE reports
            SET status = :status
            WHERE id = :report_id
            RETURNING id, status
        """),
        {
            "report_id": report_id,
            "status": status_update.status
        }
    )

    row = result.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    db.commit()

    return {
        "message": "Report status updated successfully",
        "report_id": row.id,
        "status": row.status
    }
@router.patch("/{report_id}/incident")
def assign_report_to_incident(
    report_id: int,
    incident_update: ReportIncidentUpdate,
    db: Session = Depends(get_db)
):
    # First check that the report exists
    report_check = db.execute(
        text("""
            SELECT id
            FROM reports
            WHERE id = :report_id
        """),
        {"report_id": report_id}
    ).fetchone()

    if report_check is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    # Check that the incident exists
    incident_check = db.execute(
        text("""
            SELECT id
            FROM incidents
            WHERE id = :incident_id
        """),
        {"incident_id": incident_update.incident_id}
    ).fetchone()

    if incident_check is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    # Connect the report to the incident
    result = db.execute(
        text("""
            UPDATE reports
            SET incident_id = :incident_id
            WHERE id = :report_id
            RETURNING id, incident_id
        """),
        {
            "report_id": report_id,
            "incident_id": incident_update.incident_id
        }
    )

    row = result.fetchone()

    db.commit()

    return {
        "message": "Report assigned to incident successfully",
        "report_id": row.id,
        "incident_id": row.incident_id
    }
@router.post("/{report_id}/match-incident")
def match_report_to_incident(
    report_id: int,
    db: Session = Depends(get_db)
):
    # 1. Check that the report exists
    report = db.execute(
        text("""
            SELECT
                id,
                location,
                timestamp,
                description,
                classification,
                leak_probability
            FROM reports
            WHERE id = :report_id
        """),
        {"report_id": report_id}
    ).fetchone()

    if report is None:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    # 2. Find the nearest existing incident within 100 meters
    incident = db.execute(
        text("""
            SELECT
                id,
                ST_Distance(
                    location::geography,
                    (SELECT location
                     FROM reports
                     WHERE id = :report_id)::geography
                ) AS distance_meters
            FROM incidents
            WHERE ST_DWithin(
                location::geography,
                (SELECT location
                 FROM reports
                 WHERE id = :report_id)::geography,
                100
            )
            ORDER BY distance_meters
            LIMIT 1
        """),
        {"report_id": report_id}
    ).fetchone()

    # 3. Existing incident found
    if incident is not None:

        db.execute(
            text("""
                UPDATE reports
                SET incident_id = :incident_id
                WHERE id = :report_id
            """),
            {
                "incident_id": incident.id,
                "report_id": report_id
            }
        )

        db.execute(
            text("""
                UPDATE incidents
                SET
                    report_count = COALESCE(report_count, 0) + 1,
                    last_report = CURRENT_TIMESTAMP
                WHERE id = :incident_id
            """),
            {"incident_id": incident.id}
        )

        db.commit()

        return {
            "matched": True,
            "created": False,
            "report_id": report_id,
            "incident_id": incident.id,
            "distance_meters": round(
                float(incident.distance_meters), 2
            ),
            "message": "Report matched to existing incident"
        }

    # 4. No nearby incident → create a new incident
    new_incident = db.execute(
        text("""
            INSERT INTO incidents (
                location,
                radius,
                report_count,
                first_report,
                last_report,
                leak_probability,
                classification,
                status,
                created_at
            )
            VALUES (
                (SELECT location
                 FROM reports
                 WHERE id = :report_id),
                100,
                1,
                COALESCE(
                    (SELECT timestamp
                     FROM reports
                     WHERE id = :report_id),
                    CURRENT_TIMESTAMP
                ),
                COALESCE(
                    (SELECT timestamp
                     FROM reports
                     WHERE id = :report_id),
                    CURRENT_TIMESTAMP
                ),
                :leak_probability,
                :classification,
                'new',
                CURRENT_TIMESTAMP
            )
            RETURNING id
        """),
        {
            "report_id": report_id,
            "leak_probability": report.leak_probability,
            "classification": report.classification
        }
    )

    new_incident_id = new_incident.scalar()

    # 5. Attach the report to the new incident
    db.execute(
        text("""
            UPDATE reports
            SET incident_id = :incident_id
            WHERE id = :report_id
        """),
        {
            "incident_id": new_incident_id,
            "report_id": report_id
        }
    )

    db.commit()

    return {
        "matched": False,
        "created": True,
        "report_id": report_id,
        "incident_id": new_incident_id,
        "message": "No nearby incident found. New incident created."
    }