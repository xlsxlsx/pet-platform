from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ProductSummary:
    id: int
    name: str
    category: str
    price_cents: int
    stock: int
    status: str
    merchant_name: str


@dataclass(frozen=True, slots=True)
class HospitalSummary:
    id: int
    name: str
    city: str
    district: str
    address: str
    phone: str
    open_status: str
    rating: float

