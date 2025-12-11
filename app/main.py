from fastapi import FastAPI, HTTPException, Depends, status, Path
from redis.asyncio import Redis
from .deps import get_redis
from .schemas import PhoneAddressCreate, PhoneAddressUpdate, PhoneAddressResponse
import logging
import sys


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Phone Address Service", version="1.0.0")


@app.get(
    "/phones/{phone}",
    response_model=PhoneAddressResponse,
    summary="Get an address by phone",
)
async def get_address(
    phone: str = Path(..., description="Phone number to search"),
    redis: Redis = Depends(get_redis),
):
    """
    Gets a value from Redis. Operation is O(1)
    """
    logger.info(f"Address search request for: {phone}")
    address = await redis.get(phone)

    if not address:
        logger.warning(f"Phone not found: {phone}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Phone not found"
        )

    return PhoneAddressResponse(phone=phone, address=address)


@app.post(
    "/phones",
    response_model=PhoneAddressResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new entry",
)
async def create_address(data: PhoneAddressCreate, redis: Redis = Depends(get_redis)):
    """
    `set(..., nx=True)`.
    NX (Not Exists) — atomically sets the value ONLY if the key does not exist.
    This prevents a race condition
    """
    logger.info(f"Attempt to create a record: {data.phone}")
    # returns True if set, False if key already exists
    is_created = await redis.set(data.phone, data.address, nx=True)

    if not is_created:
        logger.warning(f"A record with this phone number already exists. {data.phone}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A record with this phone number already exists. Use PUT to update.",
        )

    logger.info(f"The record was created successfully.: {data.phone}")
    return PhoneAddressResponse(phone=data.phone, address=data.address)


@app.put(
    "/phones/{phone}", response_model=PhoneAddressResponse, summary="Update address"
)
async def update_address(
    data: PhoneAddressUpdate, phone: str = Path(...), redis: Redis = Depends(get_redis)
):
    """
    `set(..., xx=True)`.
    XX (Exists) — Atomically sets the value ONLY if the key already exists.
    This eliminates the need to do a get() before a set() and handle race conditions
    """
    logger.info(f"Update address for: {phone}")
    is_updated = await redis.set(phone, data.address, xx=True)

    if not is_updated:
        logger.warning(f"Phone not found {phone}. Update not possible.")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phone not found, update not possible.",
        )

    return PhoneAddressResponse(phone=phone, address=data.address)


@app.delete(
    "/phones/{phone}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a entry"
)
async def delete_address(phone: str = Path(...), redis: Redis = Depends(get_redis)):
    """
    Deletes a key. Redis returns the number of deleted keys
    """
    logger.info(f"Delete entry: {phone}")
    deleted_count = await redis.delete(phone)

    if deleted_count == 0:
        logger.warning(f"Attempt to delete a non-existent number: {phone}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Phone not found"
        )

    return None
