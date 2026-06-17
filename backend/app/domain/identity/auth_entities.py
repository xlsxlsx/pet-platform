from dataclasses import dataclass

from app.domain.shared.enums import AccountStatus, UserRoleCode


@dataclass(frozen=True, slots=True)
class AuthenticatedUser:
    id: int
    phone: str
    display_name: str
    status: AccountStatus
    password_hash: str
    roles: tuple[UserRoleCode, ...]

    def can_use_role(self, role: UserRoleCode) -> bool:
        return self.status is AccountStatus.ACTIVE and role in self.roles

