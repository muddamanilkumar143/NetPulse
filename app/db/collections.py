from pymongo.database import Database

from app.config import ALERTS_COLLECTION, DEVICES_COLLECTION
from app.models import AlertResponse, DeviceResponse


def ensure_indexes(db: Database) -> None:
    db[DEVICES_COLLECTION].create_index("device_id", unique=True, name="device_id_1")
    db[ALERTS_COLLECTION].create_index("device_id", name="alert_device_id_1")
    db[ALERTS_COLLECTION].create_index("timestamp", name="alert_timestamp_1")


def device_document(device: DeviceResponse) -> dict:
    data = device.model_dump()
    data["ip_address"] = str(data["ip_address"])
    return data


def document_to_device(document: dict) -> DeviceResponse:
    data = dict(document)
    data.pop("_id", None)
    data.setdefault("location", None)
    return DeviceResponse(**data)


def alert_document(alert: AlertResponse) -> dict:
    return alert.model_dump()


def document_to_alert(document: dict) -> AlertResponse:
    data = dict(document)
    data.pop("_id", None)
    return AlertResponse(**data)