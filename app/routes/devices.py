from fastapi import APIRouter, HTTPException, status

from app.models import (
    AlertResponse,
    DeviceCreate,
    DeviceResponse,
    StatusUpdate,
)
from app.repositories.device_repository import InMemoryDeviceRepository
from app.services.device_service import (
    DeviceAlreadyExistsError,
    DeviceNotFoundError,
    DeviceService,
)


repository = InMemoryDeviceRepository()
device_service = DeviceService(repository)
router = APIRouter()


@router.post(
    "/devices",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "A device with this ID already exists."}},
)
def register_device(device: DeviceCreate) -> DeviceResponse:
    try:
        return device_service.register(device)
    except DeviceAlreadyExistsError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.get("/devices", response_model=list[DeviceResponse])
def list_devices() -> list[DeviceResponse]:
    return device_service.list()


@router.get(
    "/devices/{device_id}",
    response_model=DeviceResponse,
    responses={404: {"description": "The device does not exist."}},
)
def get_device(device_id: str) -> DeviceResponse:
    try:
        return device_service.get(device_id)
    except DeviceNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.patch(
    "/devices/{device_id}/status",
    response_model=DeviceResponse,
    responses={404: {"description": "The device does not exist."}},
)
def update_device_status(device_id: str, update: StatusUpdate) -> DeviceResponse:
    try:
        return device_service.update_status(device_id, update.status)
    except DeviceNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/alerts", response_model=list[AlertResponse])
def list_alerts() -> list[AlertResponse]:
    return repository.list_alerts()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}