from app.db.collections import device_document, document_to_device
from app.models import DeviceResponse


def test_legacy_device_document_defaults_location_and_hides_mongo_id() -> None:
    device = document_to_device(
        {
            "_id": "internal-id",
            "device_id": "RTR-OLD-001",
            "name": "Legacy Router",
            "device_type": "router",
            "ip_address": "192.168.10.1",
            "status": "online",
        }
    )

    assert device.location is None
    assert device.device_id == "RTR-OLD-001"
    assert "_id" not in device.model_dump()


def test_device_document_serializes_ip_address_and_location() -> None:
    device = DeviceResponse(
        device_id="RTR-102",
        name="Branch Router",
        device_type="router",
        ip_address="192.168.10.2",
        status="online",
        location="Branch Office",
    )

    document = device_document(device)

    assert document["ip_address"] == "192.168.10.2"
    assert document["location"] == "Branch Office"