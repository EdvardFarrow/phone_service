import pytest
from fastapi import status

pytestmark = pytest.mark.asyncio

VALID_PHONE = "88005553535"
VALID_ADDRESS = "Ulaanbaatar, Mongolia"

async def test_create_phone_success(client):
    """Successful record creation test (201)"""
    payload = {"phone": VALID_PHONE, "address": VALID_ADDRESS}    
    response = await client.post("/phones", json=payload)
    
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["phone"] == payload["phone"]
    assert data["address"] == payload["address"]

async def test_create_phone_conflict(client):
    """Duplicate test (409)"""
    payload = {"phone": VALID_PHONE, "address": VALID_ADDRESS}
    
    # Creating for the first time
    await client.post("/phones", json=payload)
    
    # Trying to create it a second time.
    response = await client.post("/phones", json=payload)
    
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "already exists" in response.json()["detail"].lower()

async def test_get_phone_found(client):
    """Test for getting an existing record (200)"""
    await client.post("/phones", json={"phone": VALID_PHONE, "address": VALID_ADDRESS})    
    response = await client.get(f"/phones/{VALID_PHONE}")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["address"] == VALID_ADDRESS

async def test_get_phone_not_found(client):
    """Test for getting a non-existent record (404)"""
    response = await client.get("/phones/00000000000")
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_update_phone_success(client):
    """Address update test (200)"""
    await client.post("/phones", json={"phone": VALID_PHONE, "address": VALID_ADDRESS})  
    new_address = "Paris, France"
    response = await client.put(f"/phones/{VALID_PHONE}", json={"address": new_address})
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["address"] == new_address
    
    get_resp = await client.get(f"/phones/{VALID_PHONE}")
    assert get_resp.json()["address"] == new_address

async def test_update_phone_not_found(client):
    """Test updating a non-existent phone (404)"""
    response = await client.put("/phones/999111", json={"address": "Valid Address String"})
    assert response.status_code == status.HTTP_404_NOT_FOUND

async def test_delete_phone(client):
    """Removal and subsequent verification test (204 -> 404)"""
    await client.post("/phones", json={"phone": VALID_PHONE, "address": VALID_ADDRESS})   
    
    del_response = await client.delete(f"/phones/{VALID_PHONE}")
    assert del_response.status_code == status.HTTP_204_NO_CONTENT
    
    get_response = await client.get(f"/phones/{VALID_PHONE}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND
    
async def test_create_phone_invalid_format(client):
    """Phone format validation test (422)"""
    payload = {"phone": "not-a-number", "address": "Moscow"}
    
    response = await client.post("/phones", json=payload)
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT 