from app.application.dashboard.dtos import DashboardMetricDTO, DashboardTaskDTO, RoleDashboardDTO
from app.domain.dashboard.repositories import DashboardRepository


class GetRoleDashboardUseCase:
    def __init__(self, dashboards: DashboardRepository) -> None:
        self._dashboards = dashboards

    async def execute(self, *, role: str) -> RoleDashboardDTO:
        dashboard = await self._dashboards.get_role_dashboard(role.upper())
        return RoleDashboardDTO(
            role=dashboard.role,
            title=dashboard.title,
            metrics=[
                DashboardMetricDTO(label=metric.label, value=metric.value, hint=metric.hint)
                for metric in dashboard.metrics
            ],
            tasks=[
                DashboardTaskDTO(title=task.title, status=task.status, detail=task.detail)
                for task in dashboard.tasks
            ],
        )

