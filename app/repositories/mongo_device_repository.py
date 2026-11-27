from pymongo import ReturnDocument
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from app.config import ALERTS_COLLECTION, DEVICES_COLLECTION
from app.db.collections import (
    alert_document,
    device_document,
    document_to_alert,
    document_to_device,
)
from app.models import AlertResponse, DeviceResponse, DeviceStatus
from app.services.errors import DeviceAlreadyExistsError


class MongoDeviceRepository:
    def __init__(self, db: Database) -> None:
        self.devices = db[DEVICES_COLLECTION]
        self.alerts = db[ALERTS_COLLECTION]

    def add_device(self, device: DeviceResponse) -> DeviceResponse:
        try:
            self.devices.insert_one(device_document(device))
        except DuplicateKeyError as error:
            raise DeviceAlreadyExistsError(
                f"Device '{device.device_id}' already exists."
            ) from error
        document = self.devices.find_one({"device_id": device.device_id})
        if document is None:
            raise RuntimeError("Inserted device could not be read back from MongoDB.")
        return document_to_device(document)

    def list_devices(self) -> list[DeviceResponse]:
        return [
            document_to_device(document)
            for document in self.devices.find().sort("device_id", 1)
        ]

    def get_device(self, device_id: str) -> DeviceResponse | None:
        document = self.devices.find_one({"device_id": device_id})
        return document_to_device(document) if document is not None else None

    def update_status(
        self, device_id: str, new_status: DeviceStatus
    ) -> DeviceResponse | None:
        document = self.devices.find_one_and_update(
            {"device_id": device_id},
            {"$set": {"status": new_status}},
            return_document=ReturnDocument.AFTER,
        )
        return document_to_device(document) if document is not None else None

    def save_alert(self, alert: AlertResponse) -> None:
        self.alerts.insert_one(alert_document(alert))

    def list_alerts(self) -> list[AlertResponse]:
        return [
            document_to_alert(document)
            for document in self.alerts.find().sort(
                [("timestamp", 1), ("_id", 1)]
            )
        ]