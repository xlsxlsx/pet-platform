import pytest
from fastapi.testclient import TestClient

from app.application.auth.use_cases import (
    CreateCaptchaUseCase,
    LoginUseCase,
    RegisterUseCase,
    SendSmsCodeUseCase,
)
from app.application.catalog.use_cases import ListHospitalsUseCase, ListProductsUseCase
from app.application.dashboard.use_cases import GetRoleDashboardUseCase
from app.core.config import settings
from app.core.security import PasswordHasher
from app.domain.catalog.entities import HospitalSummary, ProductSummary
from app.domain.dashboard.entities import DashboardMetric, DashboardTask, RoleDashboard
from app.domain.identity.auth_entities import AuthenticatedUser
from app.domain.shared.enums import AccountStatus, UserRoleCode
from app.infrastructure.verification.memory import InMemoryVerificationStore
from app.infrastructure.verification.sms import LocalSmsSender
from app.interfaces.http.dependencies import (
    get_create_captcha_use_case,
    get_list_hospitals_use_case,
    get_list_products_use_case,
    get_login_use_case,
    get_register_use_case,
    get_role_dashboard_use_case,
    get_send_sms_code_use_case,
)
from app.main import create_app


class FakeAuthRepository:
    def __init__(self) -> None:
        self._users: dict[str, AuthenticatedUser] = {
            "13800000001": AuthenticatedUser(
                id=1,
                phone="13800000001",
                display_name="Customer User",
                status=AccountStatus.ACTIVE,
                password_hash="unused",
                roles=(UserRoleCode.CUSTOMER,),
            ),
            "13800000002": AuthenticatedUser(
                id=2,
                phone="13800000002",
                display_name="Merchant User",
                status=AccountStatus.ACTIVE,
                password_hash="unused",
                roles=(UserRoleCode.MERCHANT,),
            ),
            "13800000005": AuthenticatedUser(
                id=5,
                phone="13800000005",
                display_name="Disabled User",
                status=AccountStatus.DISABLED,
                password_hash="unused",
                roles=(UserRoleCode.CUSTOMER,),
            ),
        }
        self._next_id = 100

    async def get_by_phone(self, phone: str) -> AuthenticatedUser | None:
        return self._users.get(phone)

    async def create_user(
        self,
        *,
        phone: str,
        display_name: str,
        password_hash: str,
        role: UserRoleCode,
        organization_name: str | None,
    ) -> AuthenticatedUser:
        self._next_id += 1
        user = AuthenticatedUser(
            id=self._next_id,
            phone=phone,
            display_name=display_name,
            status=AccountStatus.ACTIVE,
            password_hash=password_hash,
            roles=(role,),
        )
        self._users[phone] = user
        return user


class FakeDashboardRepository:
    async def get_role_dashboard(self, role: str) -> RoleDashboard:
        if role not in {item.value for item in UserRoleCode}:
            raise ValueError("unsupported role")
        return RoleDashboard(
            role=role,
            title=f"{role} dashboard",
            metrics=(DashboardMetric("Open items", "3", "Needs attention"),),
            tasks=(DashboardTask("Review queue", "TODO", "Check pending work"),),
        )


class FakeCatalogRepository:
    async def list_products(self, *, limit: int, offset: int) -> list[ProductSummary]:
        products = [
            ProductSummary(
                id=1,
                name="Cat Food",
                category="Food",
                price_cents=15900,
                stock=20,
                status="ON_SALE",
                merchant_name="Pet Store",
            )
        ]
        return products[offset : offset + limit]

    async def list_hospitals(self, *, limit: int, offset: int) -> list[HospitalSummary]:
        hospitals = [
            HospitalSummary(
                id=1,
                name="Care Hospital",
                city="Shanghai",
                district="Changning",
                address="Demo Road 1",
                phone="02100000000",
                open_status="OPEN",
                rating=4.9,
            )
        ]
        return hospitals[offset : offset + limit]


@pytest.fixture()
def client() -> TestClient:
    original_debug_codes = settings.auth_debug_codes
    original_admin_registration = settings.allow_admin_registration
    settings.auth_debug_codes = True
    settings.allow_admin_registration = True

    auth = FakeAuthRepository()
    verification_store = InMemoryVerificationStore()
    app = create_app()
    app.dependency_overrides[get_create_captcha_use_case] = lambda: CreateCaptchaUseCase(
        verification_store=verification_store,
    )
    app.dependency_overrides[get_send_sms_code_use_case] = lambda: SendSmsCodeUseCase(
        auth=auth,
        verification_store=verification_store,
        sms_sender=LocalSmsSender(),
    )
    app.dependency_overrides[get_login_use_case] = lambda: LoginUseCase(
        auth=auth,
        verification_store=verification_store,
    )
    app.dependency_overrides[get_register_use_case] = lambda: RegisterUseCase(
        auth=auth,
        password_hasher=PasswordHasher(),
        verification_store=verification_store,
    )
    app.dependency_overrides[get_role_dashboard_use_case] = lambda: GetRoleDashboardUseCase(
        dashboards=FakeDashboardRepository(),
    )
    app.dependency_overrides[get_list_products_use_case] = lambda: ListProductsUseCase(
        catalog=FakeCatalogRepository(),
    )
    app.dependency_overrides[get_list_hospitals_use_case] = lambda: ListHospitalsUseCase(
        catalog=FakeCatalogRepository(),
    )

    with TestClient(app) as test_client:
        yield test_client

    settings.auth_debug_codes = original_debug_codes
    settings.allow_admin_registration = original_admin_registration


def issue_sms_code(client: TestClient, *, phone: str, purpose: str) -> str:
    captcha = client.get("/api/v1/auth/captcha")
    assert captcha.status_code == 200
    captcha_payload = captcha.json()

    sms = client.post(
        "/api/v1/auth/sms-code",
        json={
            "phone": phone,
            "captcha_id": captcha_payload["captcha_id"],
            "captcha_code": captcha_payload["debug_code"],
            "purpose": purpose,
        },
    )
    assert sms.status_code == 200
    return sms.json()["debug_code"]


def test_health_check(client: TestClient) -> None:
    response = client.get("/api/v1/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_login_flow_uses_captcha_sms_and_role_permission(client: TestClient) -> None:
    sms_code = issue_sms_code(client, phone="13800000001", purpose="LOGIN")

    response = client.post(
        "/api/v1/auth/login",
        json={"phone": "13800000001", "sms_code": sms_code, "role": "CUSTOMER"},
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["phone"] == "13800000001"
    assert payload["active_role"] == "CUSTOMER"
    assert payload["access_token"]


def test_login_rejects_unowned_role(client: TestClient) -> None:
    sms_code = issue_sms_code(client, phone="13800000001", purpose="LOGIN")

    response = client.post(
        "/api/v1/auth/login",
        json={"phone": "13800000001", "sms_code": sms_code, "role": "ADMIN"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "account cannot use requested role"


def test_register_flow_creates_role_session(client: TestClient) -> None:
    sms_code = issue_sms_code(client, phone="13900000001", purpose="REGISTER")

    response = client.post(
        "/api/v1/auth/register",
        json={
            "phone": "13900000001",
            "sms_code": sms_code,
            "display_name": "New Customer",
            "role": "CUSTOMER",
        },
    )

    assert response.status_code == 200
    payload = response.json()
    assert payload["display_name"] == "New Customer"
    assert payload["active_role"] == "CUSTOMER"


def test_dashboard_and_catalog_contracts(client: TestClient) -> None:
    dashboard = client.get("/api/v1/dashboards/CUSTOMER")
    products = client.get("/api/v1/catalog/products?limit=1")
    hospitals = client.get("/api/v1/catalog/hospitals?limit=1")

    assert dashboard.status_code == 200
    assert dashboard.json()["metrics"][0]["label"] == "Open items"
    assert products.status_code == 200
    assert products.json()[0]["price_cents"] == 15900
    assert hospitals.status_code == 200
    assert hospitals.json()[0]["open_status"] == "OPEN"
