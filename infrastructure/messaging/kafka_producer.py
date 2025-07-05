import json
import logging
from kafka import KafkaProducer

from core.config import settings
from domain.entities.scan import Scan
from domain.repositories.messaging_producer import IMessagingProducer

logger = logging.getLogger(__name__)

class KafkaMessagingProducer(IMessagingProducer):
    def __init__(self):
        try:
            self.producer = KafkaProducer(
                bootstrap_servers=settings.KAFKA_BOOTSTRAP_SERVERS,
                value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8'),
                api_version=(0, 10, 1) # Explicitly set for compatibility
            )
            logger.info("Kafka producer connected successfully.")
        except Exception as e:
            logger.error(f"Failed to connect to Kafka: {e}")
            self.producer = None

    def publish_scan_started(self, scan: Scan) -> None:
        if not self.producer:
            logger.error("Kafka producer is not available. Cannot publish message.")
            # In a real system, you might add this to a fallback queue
            return
            
        message = {
            "scan_id": str(scan.id),
            "domain_name": scan.domain_name,
            "user_id": str(scan.user_id),
            "requested_at": scan.requested_at.isoformat()
        }
        
        try:
            self.producer.send(settings.KAFKA_SCAN_TOPIC, value=message)
            self.producer.flush()
            logger.info(f"Published 'scan.started' event for scan_id: {scan.id}")
        except Exception as e:
            logger.error(f"Failed to publish message to Kafka for scan_id {scan.id}: {e}")