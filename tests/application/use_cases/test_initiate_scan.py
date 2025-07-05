import uuid
from application.use_cases.initiate_scan import InitiateScanUseCase
from domain.entities.scan import Scan

def test_initiate_scan_success(mock_scan_repository, mock_messaging_producer):
    """Prueba que el caso de uso guarda el escaneo y luego publica el evento."""
    # Arrange
    use_case = InitiateScanUseCase(mock_scan_repository, mock_messaging_producer)
    domain_name = "example.com"
    user_id = uuid.uuid4()
    acceptable_loss = 50000.0

    # Simula que el guardado devuelve el scan con un ID
    saved_scan_instance = Scan(
        id=uuid.uuid4(),
        domain_name=domain_name,
        user_id=user_id,
        acceptable_loss=acceptable_loss
    )
    mock_scan_repository.save.return_value = saved_scan_instance

    # Act
    result = use_case.execute(domain_name, user_id, acceptable_loss)

    # Assert
    # 1. Verifica que se llamó a save
    mock_scan_repository.save.assert_called_once()
    saved_arg = mock_scan_repository.save.call_args[0][0]
    assert isinstance(saved_arg, Scan)
    assert saved_arg.domain_name == domain_name
    assert saved_arg.user_id == user_id

    # 2. Verifica que se llamó a publish con el objeto devuelto por save
    mock_messaging_producer.publish_scan_started.assert_called_once_with(saved_scan_instance)

    # 3. Verifica que el resultado es el esperado
    assert result == saved_scan_instance