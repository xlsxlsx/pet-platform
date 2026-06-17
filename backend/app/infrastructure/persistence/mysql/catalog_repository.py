from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.catalog.entities import HospitalSummary, ProductSummary


class MySQLCatalogRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def list_products(self, *, limit: int, offset: int) -> list[ProductSummary]:
        result = await self._session.execute(
            text(
                """
                SELECT p.id, p.name, p.category, p.price_cents, p.stock, p.status,
                       m.store_name AS merchant_name
                FROM products p
                JOIN merchant_profiles m ON m.id = p.merchant_id
                ORDER BY p.id
                LIMIT :limit OFFSET :offset
                """
            ),
            {"limit": limit, "offset": offset},
        )
        return [
            ProductSummary(
                id=int(row.id),
                name=row.name,
                category=row.category,
                price_cents=int(row.price_cents),
                stock=int(row.stock),
                status=row.status,
                merchant_name=row.merchant_name,
            )
            for row in result.fetchall()
        ]

    async def list_hospitals(self, *, limit: int, offset: int) -> list[HospitalSummary]:
        result = await self._session.execute(
            text(
                """
                SELECT id, name, city, district, address, phone, open_status, rating
                FROM hospitals
                ORDER BY rating DESC, id
                LIMIT :limit OFFSET :offset
                """
            ),
            {"limit": limit, "offset": offset},
        )
        return [
            HospitalSummary(
                id=int(row.id),
                name=row.name,
                city=row.city,
                district=row.district,
                address=row.address,
                phone=row.phone,
                open_status=row.open_status,
                rating=float(row.rating),
            )
            for row in result.fetchall()
        ]

