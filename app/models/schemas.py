from pydantic import BaseModel, Field
from typing import List, Optional
from .domain import OfferType


class ProductCreate(BaseModel):
    code: str
    name: str
    price: float


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None


class ProductOut(BaseModel):
    id: int
    code: str
    name: str
    price: float

    class Config:
        from_attributes = True


class DeliveryRuleCreate(BaseModel):
    min_total: float
    charge: float


class DeliveryRuleUpdate(BaseModel):
    min_total: Optional[float] = None
    charge: Optional[float] = None


class DeliveryRuleOut(BaseModel):
    id: int
    min_total: float
    charge: float

    class Config:
        from_attributes = True


class OfferCreate(BaseModel):
    type: OfferType
    product_code: Optional[str] = Field(default=None)


class OfferUpdate(BaseModel):
    type: Optional[OfferType] = None
    product_code: Optional[str] = None


class OfferOut(BaseModel):
    id: int
    type: OfferType
    product_code: Optional[str]

    class Config:
        from_attributes = True


class BasketItem(BaseModel):
    product_code: str
    quantity: int = Field(ge=1)


class BasketTotalRequest(BaseModel):
    items: List[BasketItem]


class BasketTotalResponse(BaseModel):
    subtotal: float
    discount: float
    delivery: float
    total: float
