from typing import Optional
import uuid
from sqlalchemy.orm import Session

from domain.entities.scan import Scan
from domain.repositories.scan_repository import IScanRepository
from infrastructure.database.models import ScanDB

class PostgresScanRepository(IScanRepository):
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def save(self, scan: Scan) -> Scan:
        scan_db = ScanDB(
            id=scan.id,
            user_id=scan.user_id,
            domain_name=scan.domain_name,
            acceptable_loss=scan.acceptable_loss,
            status=scan.status,
            requested_at=scan.requested_at
        )
        self.db.add(scan_db)
        self.db.commit()
        self.db.refresh(scan_db)
        return Scan.from_orm(scan_db)

    def find_by_id(self, scan_id: uuid.UUID) -> Optional[Scan]:
        scan_db = self.db.query(ScanDB).filter(ScanDB.id == scan_id).first()
        return Scan.from_orm(scan_db) if scan_db else None