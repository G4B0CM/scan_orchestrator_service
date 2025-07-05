from abc import ABC, abstractmethod
from typing import Optional
import uuid

from domain.entities.scan import Scan

class IScanRepository(ABC):
    """Abstract interface for scan data persistence."""

    @abstractmethod
    def save(self, scan: Scan) -> Scan:
        """Saves a scan entity."""
        pass

    @abstractmethod
    def find_by_id(self, scan_id: uuid.UUID) -> Optional[Scan]:
        """Finds a scan by its unique ID."""
        pass