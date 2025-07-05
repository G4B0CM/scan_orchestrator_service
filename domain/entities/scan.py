import uuid
from datetime import datetime
from pydantic import BaseModel, Field

from domain.enums.scan_status import ScanStatus

class Scan(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    domain_name: str
    user_id: uuid.UUID
    acceptable_loss: float = Field(gt=0)
    status: ScanStatus = ScanStatus.PENDING
    requested_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True