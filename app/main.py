from fastapi import FastAPI, HTTPException, Depends, status, Path
from redis.asyncio import Redis
from .deps import get_redis
from .models import PhoneAddressCreate, PhoneAddressUpdate, PhoneAddressResponse

app = FastAPI(title="Phone Address Service", version="1.0.0")

@app.get(
    "/phones/{phone}",
    response_model=PhoneAddressResponse,
    summary="Get an address by phone"
)
async def get_address(
    phone: str = Path(..., description="Phone number to search"),
    redis: Redis = Depends(get_redis)
):
    """
    Gets a value from Redis. Operation is O(1)
    """
    address = await redis.get(phone)
    
    if not address:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phone not found"
        )
    
    return PhoneAddressResponse(phone=phone, address=address)


@app.post(
    "/phones",
    response_model=PhoneAddressResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new entry"
)
async def create_address(
    data: PhoneAddressCreate,
    redis: Redis = Depends(get_redis)
):
    """
    `set(..., nx=True)`.
    NX (Not Exists) — atomically sets the value ONLY if the key does not exist.
    This prevents a race condition
    """
    # Returns True if the key has been set, False if the key already exists.
    is_created = await redis.set(data.phone, data.address, nx=True)
    
    if not is_created:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="A record with this phone number already exists. Use PUT to update."
        )
    
    return PhoneAddressResponse(phone=data.phone, address=data.address)


@app.put(
    "/phones/{phone}",
    response_model=PhoneAddressResponse,
    summary="Update address"
)
async def update_address(
    data: PhoneAddressUpdate,
    phone: str = Path(...),
    redis: Redis = Depends(get_redis)
):
    """
    `set(..., xx=True)`.
    XX (Exists) — Atomically sets the value ONLY if the key already exists.
    This eliminates the need to do a get() before a set() and handle race conditions
    """
    is_updated = await redis.set(phone, data.address, xx=True)
    
    if not is_updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phone not found, update not possible."
        )
            
    return PhoneAddressResponse(phone=phone, address=data.address)


@app.delete(
    "/phones/{phone}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a entry"
)
async def delete_address(
    phone: str = Path(...),
    redis: Redis = Depends(get_redis)
):
    """
    Deletes a key. Redis returns the number of deleted keys
    """
    deleted_count = await redis.delete(phone)
    
    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Phone not found"
        )
    
    return None