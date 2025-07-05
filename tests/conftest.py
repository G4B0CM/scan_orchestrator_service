import pytest
from unittest.mock import MagicMock
from domain.repositories.scan_repository import IScanRepository
from domain.repositories.messaging_producer import IMessagingProducer

@pytest.fixture
def mock_scan_repository(mocker):
    return mocker.MagicMock(spec=IScanRepository)

@pytest.fixture
def mock_messaging_producer(mocker):
    return mocker.MagicMock(spec=IMessagingProducer)