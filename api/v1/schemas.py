import uuid
from pydantic import BaseModel, Field

from domain.enums.scan_status import ScanStatus

# --- Request ---
class ScanCreateRequest(BaseModel):
    domain_name: str = Field(..., example="example.com")
    acceptable_loss: float = Field(..., gt=0, example=50000.0)

# --- Response ---
class ScanCreateResponse(BaseModel):
    scan_id: uuid.UUID
    domain_name: str
    status: ScanStatus
    message: str