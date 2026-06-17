from typing import Protocol

from app.domain.catalog.entities import HospitalSummary, ProductSummary


class CatalogRepository(Protocol):
    async def list_products(self, *, limit: int, offset: int) -> list[ProductSummary]:
        raise NotImplementedError

    async def list_hospitals(self, *, limit: int, offset: int) -> list[HospitalSummary]:
        raise NotImplementedError

