from dataclasses import dataclass
from datetime import datetime

from app.domain.shared.enums import AccountStatus, UserRoleCode


@dataclass(frozen=True, slots=True)
class Role:
    id: int
    code: UserRoleCode
    name: str


@dataclass(frozen=True, slots=True)
class Permission:
    id: int
    code: str
    name: str


@dataclass(slots=True)
class UserAccount:
    id: int
    phone: str
    display_name: str
    status: AccountStatus
    roles: tuple[UserRoleCode, ...]
    created_at: datetime

    def has_role(self, role: UserRoleCode) -> bool:
        return role in self.roles

    def ensure_active(self) -> None:
        if self.status is not AccountStatus.ACTIVE:
            raise ValueError("account is not active")

