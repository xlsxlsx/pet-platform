from collections.abc import AsyncIterator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.auth.use_cases import (
    CreateCaptchaUseCase,
    LoginUseCase,
    RegisterUseCase,
    SendSmsCodeUseCase,
)
from app.application.catalog.use_cases import ListHospitalsUseCase, ListProductsUseCase
from app.application.dashboard.use_cases import GetRoleDashboardUseCase
from app.core.database import get_db_session
from app.core.security import password_hasher
from app.infrastructure.persistence.mysql.auth_repository import MySQLAuthRepository
from app.infrastructure.persistence.mysql.catalog_repository import MySQLCatalogRepository
from app.infrastructure.persistence.mysql.dashboard_repository import MySQLDashboardRepository
from app.infrastructure.verification.memory import InMemoryVerificationStore
from app.infrastructure.verification.sms import LocalSmsSender

verification_store = InMemoryVerificationStore()
sms_sender = LocalSmsSender()


async def get_session() -> AsyncIterator[AsyncSession]:
    async for session in get_db_session():
        yield session


def get_login_use_case(session: AsyncSession = Depends(get_session)) -> LoginUseCase:
    return LoginUseCase(auth=MySQLAuthRepository(session), verification_store=verification_store)


def get_register_use_case(session: AsyncSession = Depends(get_session)) -> RegisterUseCase:
    return RegisterUseCase(
        auth=MySQLAuthRepository(session),
        password_hasher=password_hasher,
        verification_store=verification_store,
    )


def get_create_captcha_use_case() -> CreateCaptchaUseCase:
    return CreateCaptchaUseCase(verification_store=verification_store)


def get_send_sms_code_use_case(session: AsyncSession = Depends(get_session)) -> SendSmsCodeUseCase:
    return SendSmsCodeUseCase(
        auth=MySQLAuthRepository(session),
        verification_store=verification_store,
        sms_sender=sms_sender,
    )


def get_role_dashboard_use_case(
    session: AsyncSession = Depends(get_session),
) -> GetRoleDashboardUseCase:
    return GetRoleDashboardUseCase(dashboards=MySQLDashboardRepository(session))


def get_list_products_use_case(session: AsyncSession = Depends(get_session)) -> ListProductsUseCase:
    return ListProductsUseCase(catalog=MySQLCatalogRepository(session))


def get_list_hospitals_use_case(session: AsyncSession = Depends(get_session)) -> ListHospitalsUseCase:
    return ListHospitalsUseCase(catalog=MySQLCatalogRepository(session))
