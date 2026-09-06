from sqlalchemy import Column, Integer, Text, DateTime
from .database import Base


class Dispatch(Base):
    __tablename__ = "dispatches"

    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer)
    crew_id = Column(Integer)
    dispatched_at = Column(DateTime)
    status = Column(Text)
    eta = Column(Integer)