from sqlalchemy import select
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.models import AlertModel, DeviceModel
from app.models import AlertResponse, DeviceResponse, DeviceStatus
from app.services.errors import DeviceAlreadyExistsError


class MySqlDeviceRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_device(self, device: DeviceResponse) -> DeviceResponse:
        model = DeviceModel(
            device_id=device.device_id,
            name=device.name,
            device_type=device.device_type,
            ip_address=str(device.ip_address),
            status=device.status,
            location=device.location,
        )
        self.session.add(model)
        try:
            self.session.commit()
            self.session.refresh(model)
        except IntegrityError as error:
            self.session.rollback()
            raise DeviceAlreadyExistsError(
                f"Device '{device.device_id}' already exists."
            ) from error
        except SQLAlchemyError:
            self.session.rollback()
            raise
        return self._to_device_response(model)

    def list_devices(self) -> list[DeviceResponse]:
        devices = self.session.scalars(
            select(DeviceModel).order_by(DeviceModel.device_id)
        )
        return [self._to_device_response(device) for device in devices]

    def get_device(self, device_id: str) -> DeviceResponse | None:
        device = self.session.get(DeviceModel, device_id)
        return self._to_device_response(device) if device is not None else None

    def update_status(
        self, device_id: str, new_status: DeviceStatus
    ) -> DeviceResponse | None:
        device = self.session.get(DeviceModel, device_id)
        if device is None:
            return None

        device.status = new_status
        try:
            self.session.commit()
            self.session.refresh(device)
        except SQLAlchemyError:
            self.session.rollback()
            raise
        return self._to_device_response(device)

    def save_alert(self, alert: AlertResponse) -> None:
        self.session.add(
            AlertModel(
                device_id=alert.device_id,
                message=alert.message,
                timestamp=alert.timestamp,
            )
        )
        try:
            self.session.commit()
        except SQLAlchemyError:
            self.session.rollback()
            raise

    def list_alerts(self) -> list[AlertResponse]:
        alerts = self.session.scalars(
            select(AlertModel).order_by(AlertModel.timestamp, AlertModel.id)
        )
        return [
            AlertResponse(
                device_id=alert.device_id,
                message=alert.message,
                timestamp=alert.timestamp,
            )
            for alert in alerts
        ]

    @staticmethod
    def _to_device_response(device: DeviceModel) -> DeviceResponse:
        return DeviceResponse(
            device_id=device.device_id,
            name=device.name,
            device_type=device.device_type,
            ip_address=device.ip_address,
            status=device.status,
            location=device.location,
        )