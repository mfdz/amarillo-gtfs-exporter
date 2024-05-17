import logging
import requests
import os
from datetime import datetime, date, timedelta
from fastapi import APIRouter, HTTPException, Response, status, Depends

from amarillo.models.Carpool import Region
from amarillo.services.regions import RegionService
from amarillo.services.oauth2 import get_current_user, verify_permission
from amarillo.models.User import User
from amarillo.utils.container import container
from fastapi.responses import FileResponse
from .config import config

logger = logging.getLogger(__name__)

router = APIRouter()

#TODO: move to amarillo/utils?
def _assert_region_exists(region_id: str) -> Region:
    regions: RegionService = container['regions']
    region = regions.get_region(region_id)
    region_exists = region is not None

    if not region_exists:
        message = f"Region with id {region_id} does not exist."
        logger.error(message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=message)

    return region

def is_cached(path : str):
    if not os.path.isfile(path): return False

    timestamp = os.path.getmtime(path)
    return datetime.fromtimestamp(timestamp).date() == date.today()

@router.get("/region/{region_id}/gtfs", 
    summary="Return GTFS Feed for this region",
    response_description="GTFS-Feed (zip-file)",
    response_class=FileResponse,
    responses={
                status.HTTP_404_NOT_FOUND: {"description": "Region not found"},
        }
    )
async def get_file(region_id: str, requesting_user: User = Depends(get_current_user)):
    verify_permission("gtfs", requesting_user)
    _assert_region_exists(region_id)
    file_path = f'data/gtfs/amarillo.{region_id}.gtfs.zip'
    if is_cached(file_path):
        logger.info("Returning cached response")
        return FileResponse(file_path)
    
    logger.info("Returning new response")
    response = requests.get(f"{config.generator_url}/region/{region_id}/gtfs/")
    # cache response
    with open(file_path, "wb") as file:
        file.write(response.content)

    return  Response(content=response.content, media_type="application/zip")

@router.get("/region/{region_id}/gtfs-rt",
    summary="Return GTFS-RT Feed for this region",
    response_description="GTFS-RT-Feed",
    response_class=FileResponse,
    responses={
                status.HTTP_404_NOT_FOUND: {"description": "Region not found"},
                status.HTTP_400_BAD_REQUEST: {"description": "Bad request, e.g. because format is not supported, i.e. neither protobuf nor json."}
        }
    )
async def get_file(region_id: str, format: str = 'protobuf', requesting_user: User = Depends(get_current_user)):
    verify_permission("gtfs", requesting_user)
    _assert_region_exists(region_id)
    if format == 'json':
        file_path = f'data/gtfs/amarillo.{region_id}.gtfsrt.json'
    elif format == 'protobuf':
        file_path = f'data/gtfs/amarillo.{region_id}.gtfsrt.pbf'
    else:
        message = "Specified format is not supported, i.e. neither protobuf nor json."
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=message)
    
    if is_cached(file_path):
        logger.info("Returning cached response")
        return FileResponse(file_path)
    
    logger.info("Returning new response")
    response = requests.get(f"{config.generator_url}/region/{region_id}/gtfs-rt/?format={format}")
    # cache response
    with open(file_path, "wb") as file:
        file.write(response.content)

    return  Response(content=response.content)