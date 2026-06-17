from app.application.catalog.dtos import HospitalSummaryDTO, ProductSummaryDTO
from app.domain.catalog.repositories import CatalogRepository


class ListProductsUseCase:
    def __init__(self, catalog: CatalogRepository) -> None:
        self._catalog = catalog

    async def execute(self, *, limit: int = 20, offset: int = 0) -> list[ProductSummaryDTO]:
        products = await self._catalog.list_products(limit=limit, offset=offset)
        return [
            ProductSummaryDTO(
                id=product.id,
                name=product.name,
                category=product.category,
                price_cents=product.price_cents,
                stock=product.stock,
                status=product.status,
                merchant_name=product.merchant_name,
            )
            for product in products
        ]


class ListHospitalsUseCase:
    def __init__(self, catalog: CatalogRepository) -> None:
        self._catalog = catalog

    async def execute(self, *, limit: int = 20, offset: int = 0) -> list[HospitalSummaryDTO]:
        hospitals = await self._catalog.list_hospitals(limit=limit, offset=offset)
        return [
            HospitalSummaryDTO(
                id=hospital.id,
                name=hospital.name,
                city=hospital.city,
                district=hospital.district,
                address=hospital.address,
                phone=hospital.phone,
                open_status=hospital.open_status,
                rating=hospital.rating,
            )
            for hospital in hospitals
        ]

