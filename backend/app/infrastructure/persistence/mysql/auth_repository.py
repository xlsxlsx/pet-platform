from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.identity.auth_entities import AuthenticatedUser
from app.domain.shared.enums import AccountStatus, UserRoleCode


class MySQLAuthRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_phone(self, phone: str) -> AuthenticatedUser | None:
        user_result = await self._session.execute(
            text(
                """
                SELECT id, phone, display_name, password_hash, status
                FROM users
                WHERE phone = :phone AND deleted_at IS NULL
                """
            ),
            {"phone": phone},
        )
        row = user_result.fetchone()
        if row is None:
            return None
        roles = await self._roles_for_user(int(row.id))
        return AuthenticatedUser(
            id=int(row.id),
            phone=row.phone,
            display_name=row.display_name,
            password_hash=row.password_hash,
            status=AccountStatus(row.status),
            roles=roles,
        )

    async def create_user(
        self,
        *,
        phone: str,
        display_name: str,
        password_hash: str,
        role: UserRoleCode,
        organization_name: str | None,
    ) -> AuthenticatedUser:
        existing = await self.get_by_phone(phone)
        if existing is not None:
            raise ValueError("phone already registered")

        user_result = await self._session.execute(
            text(
                """
                INSERT INTO users (phone, display_name, password_hash, status)
                VALUES (:phone, :display_name, :password_hash, 'ACTIVE')
                """
            ),
            {"phone": phone, "display_name": display_name, "password_hash": password_hash},
        )
        user_id = int(user_result.lastrowid)

        role_result = await self._session.execute(
            text("SELECT id FROM roles WHERE code = :role"),
            {"role": role.value},
        )
        role_id = int(role_result.scalar_one())
        await self._session.execute(
            text("INSERT INTO user_roles (user_id, role_id) VALUES (:user_id, :role_id)"),
            {"user_id": user_id, "role_id": role_id},
        )
        await self._create_profile(
            user_id=user_id,
            phone=phone,
            display_name=display_name,
            role=role,
            organization_name=organization_name,
        )
        await self._session.commit()
        created = await self.get_by_phone(phone)
        if created is None:
            raise RuntimeError("created account cannot be loaded")
        return created

    async def _roles_for_user(self, user_id: int) -> tuple[UserRoleCode, ...]:
        result = await self._session.execute(
            text(
                """
                SELECT r.code
                FROM roles r
                JOIN user_roles ur ON ur.role_id = r.id
                WHERE ur.user_id = :user_id
                ORDER BY r.code
                """
            ),
            {"user_id": user_id},
        )
        return tuple(UserRoleCode(row.code) for row in result.fetchall())

    async def _create_profile(
        self,
        *,
        user_id: int,
        phone: str,
        display_name: str,
        role: UserRoleCode,
        organization_name: str | None,
    ) -> None:
        if role is UserRoleCode.CUSTOMER:
            await self._session.execute(
                text("INSERT INTO customer_profiles (user_id, nickname) VALUES (:user_id, :name)"),
                {"user_id": user_id, "name": display_name},
            )
            return

        if role is UserRoleCode.MERCHANT:
            await self._session.execute(
                text(
                    """
                    INSERT INTO merchant_profiles (user_id, store_name, contact_phone, review_status)
                    VALUES (:user_id, :name, :phone, 'PENDING')
                    """
                ),
                {
                    "user_id": user_id,
                    "name": organization_name or f"{display_name}的宠物用品店",
                    "phone": phone,
                },
            )
            return

        if role is UserRoleCode.HOSPITAL:
            await self._session.execute(
                text(
                    """
                    INSERT INTO hospital_profiles (user_id, hospital_name, license_no, review_status)
                    VALUES (:user_id, :name, :license_no, 'PENDING')
                    """
                ),
                {
                    "user_id": user_id,
                    "name": organization_name or f"{display_name}宠物医院",
                    "license_no": "PENDING",
                },
            )
            return

        if role is UserRoleCode.ADMIN:
            await self._session.execute(
                text(
                    """
                    INSERT INTO admin_profiles (user_id, employee_no)
                    VALUES (:user_id, :employee_no)
                    """
                ),
                {"user_id": user_id, "employee_no": f"ADM-{user_id:04d}"},
            )
