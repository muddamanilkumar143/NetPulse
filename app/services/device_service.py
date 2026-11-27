from app.events import create_offline_alert
from app.models import DeviceCreate, DeviceResponse, DeviceStatus
from app.repositories.protocols import DeviceRepository
from app.services.errors import DeviceAlreadyExistsError, DeviceNotFoundError


class DeviceService:
    def __init__(self, repository: DeviceRepository) -> None:
        self.repository = repository

    def register(self, device: DeviceCreate) -> DeviceResponse:
        if self.repository.get_device(device.device_id) is not None:
            raise DeviceAlreadyExistsError(
                f"Device '{device.device_id}' already exists."
            )
        response = DeviceResponse(**device.model_dump())
        return self.repository.add_device(response)

    def list(self) -> list[DeviceResponse]:
        return self.repository.list_devices()

    def get(self, device_id: str) -> DeviceResponse:
        device = self.repository.get_device(device_id)
        if device is None:
            raise DeviceNotFoundError(f"Device '{device_id}' was not found.")
        return device

    def update_status(
        self, device_id: str, new_status: DeviceStatus
    ) -> DeviceResponse:
        device = self.repository.get_device(device_id)
        if device is None:
            raise DeviceNotFoundError(f"Device '{device_id}' was not found.")

        changed_to_offline = device.status == "online" and new_status == "offline"
        updated_device = self.repository.update_status(device_id, new_status)
        if changed_to_offline:
            create_offline_alert(self.repository, device_id)
        return updated_device