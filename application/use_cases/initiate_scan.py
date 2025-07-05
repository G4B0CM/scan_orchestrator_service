import uuid
from domain.entities.scan import Scan
from domain.repositories.scan_repository import IScanRepository
from domain.repositories.messaging_producer import IMessagingProducer

class InitiateScanUseCase:
    def __init__(
        self,
        scan_repository: IScanRepository,
        messaging_producer: IMessagingProducer
    ):
        self.scan_repository = scan_repository
        self.messaging_producer = messaging_producer

    def execute(self, domain_name: str, user_id: uuid.UUID, acceptable_loss: float) -> Scan:
        # Create the scan entity
        new_scan = Scan(
            domain_name=domain_name,
            user_id=user_id,
            acceptable_loss=acceptable_loss
        )
        
        # 1. Persist the initial state
        saved_scan = self.scan_repository.save(new_scan)

        # 2. Publish the event to trigger the pipeline
        self.messaging_producer.publish_scan_started(saved_scan)
        
        return saved_scan