from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class DashboardMetric:
    label: str
    value: str
    hint: str


@dataclass(frozen=True, slots=True)
class DashboardTask:
    title: str
    status: str
    detail: str


@dataclass(frozen=True, slots=True)
class RoleDashboard:
    role: str
    title: str
    metrics: tuple[DashboardMetric, ...]
    tasks: tuple[DashboardTask, ...]

