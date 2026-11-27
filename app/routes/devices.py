from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_device_service, get_repository
from app.models import (
    AlertResponse,
    DeviceCreate,
    DeviceResponse,
    StatusUpdate,
)
from app.repositories.protocols import DeviceRepository
from app.services.device_service import (
    DeviceAlreadyExistsError,
    DeviceNotFoundError,
    DeviceService,
)


router = APIRouter()


@router.post(
    "/devices",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "A device with this ID already exists."}},
)
def register_device(
    device: DeviceCreate,
    device_service: DeviceService = Depends(get_device_service),
) -> DeviceResponse:
    try:
        return device_service.register(device)
    except DeviceAlreadyExistsError as error:
        raise HTTPException(status_code=409, detail=str(error)) from error


@router.get("/devices", response_model=list[DeviceResponse])
def list_devices(
    device_service: DeviceService = Depends(get_device_service),
) -> list[DeviceResponse]:
    return device_service.list()


@router.get(
    "/devices/{device_id}",
    response_model=DeviceResponse,
    responses={404: {"description": "The device does not exist."}},
)
def get_device(
    device_id: str,
    device_service: DeviceService = Depends(get_device_service),
) -> DeviceResponse:
    try:
        return device_service.get(device_id)
    except DeviceNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.patch(
    "/devices/{device_id}/status",
    response_model=DeviceResponse,
    responses={404: {"description": "The device does not exist."}},
)
def update_device_status(
    device_id: str,
    update: StatusUpdate,
    device_service: DeviceService = Depends(get_device_service),
) -> DeviceResponse:
    try:
        return device_service.update_status(device_id, update.status)
    except DeviceNotFoundError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/alerts", response_model=list[AlertResponse])
def list_alerts(
    repository: DeviceRepository = Depends(get_repository),
) -> list[AlertResponse]:
    return repository.list_alerts()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}