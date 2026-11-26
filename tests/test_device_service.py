import pytest

from app.models import DeviceCreate
from app.repositories.device_repository import InMemoryDeviceRepository
from app.services.device_service import (
    DeviceAlreadyExistsError,
    DeviceNotFoundError,
    DeviceService,
)


@pytest.fixture
def service() -> DeviceService:
    return DeviceService(InMemoryDeviceRepository())


def make_device(
    device_id: str = "RTR-101", status: str = "online"
) -> DeviceCreate:
    return DeviceCreate(
        device_id=device_id,
        name="Branch Router",
        device_type="router",
        ip_address="192.168.10.1",
        status=status,
    )


def test_register_device(service: DeviceService) -> None:
    device = service.register(make_device())

    assert device.device_id == "RTR-101"
    assert device.status == "online"
    assert service.list() == [device]


def test_duplicate_registration_raises_error(service: DeviceService) -> None:
    service.register(make_device())

    with pytest.raises(DeviceAlreadyExistsError):
        service.register(make_device())


def test_missing_device_raises_error(service: DeviceService) -> None:
    with pytest.raises(DeviceNotFoundError):
        service.get("missing")

    with pytest.raises(DeviceNotFoundError):
        service.update_status("missing", "offline")


def test_initial_offline_registration_does_not_create_alert(
    service: DeviceService,
) -> None:
    service.register(make_device(status="offline"))

    assert service.repository.list_alerts() == []


def test_online_to_offline_creates_one_alert(service: DeviceService) -> None:
    service.register(make_device())

    updated = service.update_status("RTR-101", "offline")

    alerts = service.repository.list_alerts()
    assert updated.status == "offline"
    assert len(alerts) == 1
    assert alerts[0].device_id == "RTR-101"
    assert "online to offline" in alerts[0].message
    assert alerts[0].timestamp.tzinfo is not None


def test_repeated_offline_update_does_not_create_another_alert(
    service: DeviceService,
) -> None:
    service.register(make_device())

    service.update_status("RTR-101", "offline")
    service.update_status("RTR-101", "offline")

    assert len(service.repository.list_alerts()) == 1