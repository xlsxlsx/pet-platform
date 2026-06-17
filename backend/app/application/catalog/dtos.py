from pydantic import BaseModel


class ProductSummaryDTO(BaseModel):
    id: int
    name: str
    category: str
    price_cents: int
    stock: int
    status: str
    merchant_name: str


class HospitalSummaryDTO(BaseModel):
    id: int
    name: str
    city: str
    district: str
    address: str
    phone: str
    open_status: str
    rating: float

