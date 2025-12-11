import re
from pydantic import BaseModel, Field, field_validator

PHONE_REGEX = r"^\+?[1-9]\d{1,14}$"


class PhoneAddressBase(BaseModel):
    address: str = Field(..., min_length=5, description="Client address")


class PhoneAddressCreate(PhoneAddressBase):
    phone: str = Field(..., description="Phone number in E.164 format")

    @field_validator("phone")
    def validate_phone(cls, v):
        if not re.match(PHONE_REGEX, v):
            raise ValueError(
                "The phone number must be in international format (e.g. +79990000000)"
            )
        return v


class PhoneAddressUpdate(PhoneAddressBase):
    pass


class PhoneAddressResponse(PhoneAddressBase):
    phone: str
