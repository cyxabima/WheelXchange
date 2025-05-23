from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid
from typing import List, Literal, Optional

from src.db.models import Booking, Cars, Customers


class UserCreateModel(BaseModel):
    email: EmailStr
    password: str
    phone_no: str


class UserLoginModel(BaseModel):
    email: EmailStr
    password: str
    phone_no: Optional[str] = None


class UserDeleteModel(BaseModel):
    email: EmailStr
    password: str


class CustomerCreateModel(UserCreateModel):
    first_name: str
    last_name: str


class CustomerResponseModel(CustomerCreateModel):
    uid: uuid.UUID
    created_at: datetime
    updated_at: datetime


class VendorCreateModel(UserCreateModel):
    first_name: Optional[str] = None  # For individuals
    last_name: Optional[str] = None  # For individuals
    business_name: Optional[str] = None  # For businesses
    is_business: bool


class VendorResponseModel(VendorCreateModel):
    uid: uuid.UUID
    cars: List[Cars]
    created_at: datetime
    updated_at: datetime


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenDataModel(BaseModel):
    # uid: uuid.UUID
    email: EmailStr
    role: Literal["Customer", "Vendor", "Admin"]


class GetMyCustomerResponse(BaseModel):
    customer: Customers
    booking: Booking
    pass
