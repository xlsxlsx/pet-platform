import base64
import html
import secrets
import string
from datetime import UTC, datetime, timedelta

from app.application.auth.dtos import (
    AuthSessionDTO,
    CaptchaDTO,
    LoginCommand,
    RegisterCommand,
    SmsCodeCommand,
    SmsCodeDTO,
)
from app.application.auth.verification import SmsSender, VerificationStore
from app.core.config import settings
from app.core.security import PasswordHasher
from app.domain.identity.auth_repositories import AuthRepository
from app.domain.shared.enums import AccountStatus, UserRoleCode


class CreateCaptchaUseCase:
    def __init__(self, verification_store: VerificationStore) -> None:
        self._verification_store = verification_store

    async def execute(self) -> CaptchaDTO:
        captcha_id = secrets.token_urlsafe(24)
        code = _random_code(4, alphabet=string.ascii_uppercase + string.digits)
        expires_at = datetime.now(UTC) + timedelta(seconds=settings.captcha_ttl_seconds)
        await self._verification_store.save_captcha(captcha_id, code, expires_at)
        return CaptchaDTO(
            captcha_id=captcha_id,
            image_base64=_captcha_image_base64(code),
            expires_in_seconds=settings.captcha_ttl_seconds,
            debug_code=code if settings.auth_debug_codes else None,
        )


class SendSmsCodeUseCase:
    def __init__(
        self,
        auth: AuthRepository,
        verification_store: VerificationStore,
        sms_sender: SmsSender,
    ) -> None:
        self._auth = auth
        self._verification_store = verification_store
        self._sms_sender = sms_sender

    async def execute(self, command: SmsCodeCommand) -> SmsCodeDTO:
        captcha_ok = await self._verification_store.verify_captcha(
            command.captcha_id,
            command.captcha_code,
        )
        if not captcha_ok:
            raise ValueError("invalid captcha code")

        user = await self._auth.get_by_phone(command.phone)
        if command.purpose == "LOGIN" and user is None:
            raise ValueError("phone is not registered")
        if command.purpose == "LOGIN" and user is not None and user.status is not AccountStatus.ACTIVE:
            raise PermissionError("account is not active")
        if command.purpose == "REGISTER" and user is not None:
            raise ValueError("phone already registered")

        code = _random_code(settings.sms_code_length, alphabet=string.digits)
        expires_at = datetime.now(UTC) + timedelta(seconds=settings.sms_code_ttl_seconds)
        await self._verification_store.save_sms_code(
            phone=command.phone,
            purpose=command.purpose,
            code=code,
            expires_at=expires_at,
        )
        await self._sms_sender.send_code(phone=command.phone, code=code, purpose=command.purpose)
        return SmsCodeDTO(
            phone=command.phone,
            purpose=command.purpose,
            expires_in_seconds=settings.sms_code_ttl_seconds,
            debug_code=code if settings.auth_debug_codes else None,
        )


class LoginUseCase:
    def __init__(self, auth: AuthRepository, verification_store: VerificationStore) -> None:
        self._auth = auth
        self._verification_store = verification_store

    async def execute(self, command: LoginCommand) -> AuthSessionDTO:
        role = _parse_role(command.role)
        user = await self._auth.get_by_phone(command.phone)
        if user is None:
            raise ValueError("invalid phone or sms code")
        sms_ok = await self._verification_store.verify_sms_code(
            phone=command.phone,
            purpose="LOGIN",
            code=command.sms_code,
        )
        if not sms_ok:
            raise ValueError("invalid phone or sms code")
        if user.status is not AccountStatus.ACTIVE:
            raise PermissionError("account is not active")
        if not user.can_use_role(role):
            raise PermissionError("account cannot use requested role")
        return _session_for(
            user_id=user.id,
            phone=user.phone,
            display_name=user.display_name,
            roles=user.roles,
            role=role,
        )


class RegisterUseCase:
    def __init__(
        self,
        auth: AuthRepository,
        password_hasher: PasswordHasher,
        verification_store: VerificationStore,
    ) -> None:
        self._auth = auth
        self._password_hasher = password_hasher
        self._verification_store = verification_store

    async def execute(self, command: RegisterCommand) -> AuthSessionDTO:
        role = _parse_role(command.role)
        if role is UserRoleCode.ADMIN and not settings.allow_admin_registration:
            raise PermissionError("admin registration is disabled")
        sms_ok = await self._verification_store.verify_sms_code(
            phone=command.phone,
            purpose="REGISTER",
            code=command.sms_code,
        )
        if not sms_ok:
            raise ValueError("invalid phone or sms code")

        password_hash = self._password_hasher.hash_password(secrets.token_urlsafe(32))
        user = await self._auth.create_user(
            phone=command.phone,
            display_name=command.display_name,
            password_hash=password_hash,
            role=role,
            organization_name=command.organization_name,
        )
        return _session_for(
            user_id=user.id,
            phone=user.phone,
            display_name=user.display_name,
            roles=user.roles,
            role=role,
        )


def _parse_role(role: str) -> UserRoleCode:
    try:
        return UserRoleCode(role.upper())
    except ValueError as exc:
        raise ValueError("unsupported role") from exc


def _random_code(length: int, *, alphabet: str) -> str:
    return "".join(secrets.choice(alphabet) for _ in range(length))


def _captcha_image_base64(code: str) -> str:
    escaped = html.escape(code)
    noise = "\n".join(
        f'<line x1="{10 + index * 25}" y1="{15 + (index % 2) * 18}" '
        f'x2="{35 + index * 24}" y2="{42 - (index % 2) * 16}" '
        'stroke="#94a3b8" stroke-width="1" opacity="0.7" />'
        for index in range(4)
    )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="132" height="46" viewBox="0 0 132 46">
<rect width="132" height="46" rx="6" fill="#f8fafc"/>
{noise}
<text x="66" y="31" text-anchor="middle" font-family="Consolas, monospace" font-size="24" font-weight="700" fill="#0f172a" letter-spacing="4">{escaped}</text>
</svg>"""
    return base64.b64encode(svg.encode("utf-8")).decode("ascii")


def _session_for(
    *,
    user_id: int,
    phone: str,
    display_name: str,
    roles: tuple[UserRoleCode, ...],
    role: UserRoleCode,
) -> AuthSessionDTO:
    return AuthSessionDTO(
        user_id=user_id,
        phone=phone,
        display_name=display_name,
        roles=[item.value for item in roles],
        active_role=role.value,
        access_token=f"demo-token-{user_id}-{role.value.lower()}",
    )
