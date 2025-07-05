import uuid
from sqlalchemy import Column, String, Float, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from infrastructure.database.connection import Base
from domain.enums.scan_status import ScanStatus

class ScanDB(Base):
    __tablename__ = "scans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    domain_name = Column(String, nullable=False, index=True)
    acceptable_loss = Column(Float, nullable=False)
    status = Column(Enum(ScanStatus), nullable=False, default=ScanStatus.PENDING)
    requested_at = Column(DateTime, nullable=False)