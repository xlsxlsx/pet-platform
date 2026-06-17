from pydantic import BaseModel


class DashboardMetricDTO(BaseModel):
    label: str
    value: str
    hint: str


class DashboardTaskDTO(BaseModel):
    title: str
    status: str
    detail: str


class RoleDashboardDTO(BaseModel):
    role: str
    title: str
    metrics: list[DashboardMetricDTO]
    tasks: list[DashboardTaskDTO]

