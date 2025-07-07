import uuid
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from api.v1 import schemas
from api.v1.security import get_current_user_id
from application.use_cases.initiate_scan import InitiateScanUseCase
from infrastructure.database.connection import get_db
from infrastructure.repositories.postgres_scan_repository import PostgresScanRepository
from infrastructure.messaging.kafka_producer import KafkaMessagingProducer

router = APIRouter()

@router.post("/scan", response_model=schemas.ScanCreateResponse, status_code=status.HTTP_202_ACCEPTED)
def create_scan(
    scan_request: schemas.ScanCreateRequest,
    db: Session = Depends(get_db),
    current_user_id: uuid.UUID = Depends(get_current_user_id)
):
    """
    Initiates a new cybersecurity scan for the given domain.
    This endpoint is asynchronous. It accepts the request and returns immediately,
    while the scan processing is started in the background.
    """
    # Instantiate infrastructure components
    scan_repo = PostgresScanRepository(db)
    producer = KafkaMessagingProducer()
    
    # Instantiate and execute the use case
    use_case = InitiateScanUseCase(scan_repo, producer)
    created_scan = use_case.execute(
        domain_name=scan_request.domain_name,
        user_id=current_user_id,
        acceptable_loss=scan_request.acceptable_loss
    )

    return {
        "scan_id": created_scan.id,
        "domain_name": created_scan.domain_name,
        "status": created_scan.status,
        "message": "Scan initiated successfully. Processing has started."
    }