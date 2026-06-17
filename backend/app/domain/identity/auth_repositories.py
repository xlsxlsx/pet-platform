from typing import Protocol

from app.domain.identity.auth_entities import AuthenticatedUser
from app.domain.shared.enums import UserRoleCode


class AuthRepository(Protocol):
    async def get_by_phone(self, phone: str) -> AuthenticatedUser | None:
        raise NotImplementedError

    async def create_user(
        self,
        *,
        phone: str,
        display_name: str,
        password_hash: str,
        role: UserRoleCode,
        organization_name: str | None,
    ) -> AuthenticatedUser:
        raise NotImplementedError
