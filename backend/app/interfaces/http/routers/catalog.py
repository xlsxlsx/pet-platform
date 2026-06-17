from fastapi import APIRouter, Depends, Query

from app.application.catalog.dtos import HospitalSummaryDTO, ProductSummaryDTO
from app.application.catalog.use_cases import ListHospitalsUseCase, ListProductsUseCase
from app.interfaces.http.dependencies import (
    get_list_hospitals_use_case,
    get_list_products_use_case,
)

router = APIRouter()


@router.get("/products", response_model=list[ProductSummaryDTO])
async def list_products(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    use_case: ListProductsUseCase = Depends(get_list_products_use_case),
) -> list[ProductSummaryDTO]:
    return await use_case.execute(limit=limit, offset=offset)


@router.get("/hospitals", response_model=list[HospitalSummaryDTO])
async def list_hospitals(
    limit: int = Query(default=20, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    use_case: ListHospitalsUseCase = Depends(get_list_hospitals_use_case),
) -> list[HospitalSummaryDTO]:
    return await use_case.execute(limit=limit, offset=offset)

