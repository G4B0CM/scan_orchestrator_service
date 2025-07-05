from abc import ABC, abstractmethod
from domain.entities.scan import Scan

class IMessagingProducer(ABC):
    """Abstract interface for a messaging producer."""

    @abstractmethod
    def publish_scan_started(self, scan: Scan) -> None:
        """Publishes an event indicating a new scan has started."""
        pass