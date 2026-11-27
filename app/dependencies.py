from fastapi import Depends
from sqlalchemy.orm import Session

from app.config import STORAGE_BACKEND
from app.db.session import get_db
from app.repositories.device_repository import InMemoryDeviceRepository
from app.repositories.mysql_device_repository import MySqlDeviceRepository
from app.repositories.protocols import DeviceRepository
from app.services.device_service import DeviceService


_in_memory_repository = InMemoryDeviceRepository()


def get_repository(db: Session | None = Depends(get_db)) -> DeviceRepository:
    if STORAGE_BACKEND == "mysql":
        if db is None:
            raise RuntimeError("MySQL storage is enabled but no database session exists.")
        return MySqlDeviceRepository(db)
    return _in_memory_repository


def get_device_service(
    repository: DeviceRepository = Depends(get_repository),
) -> DeviceService:
    return DeviceService(repository)