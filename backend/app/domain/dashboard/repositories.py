from typing import Protocol

from app.domain.dashboard.entities import RoleDashboard


class DashboardRepository(Protocol):
    async def get_role_dashboard(self, role: str) -> RoleDashboard:
        raise NotImplementedError

