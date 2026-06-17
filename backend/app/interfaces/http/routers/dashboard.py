from fastapi import APIRouter, Depends, HTTPException

from app.application.dashboard.dtos import RoleDashboardDTO
from app.application.dashboard.use_cases import GetRoleDashboardUseCase
from app.interfaces.http.dependencies import get_role_dashboard_use_case

router = APIRouter()


@router.get("/{role}", response_model=RoleDashboardDTO)
async def get_role_dashboard(
    role: str,
    use_case: GetRoleDashboardUseCase = Depends(get_role_dashboard_use_case),
) -> RoleDashboardDTO:
    try:
        return await use_case.execute(role=role)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

