from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(slots=True)
class _VerificationValue:
    code: str
    expires_at: datetime


class InMemoryVerificationStore:
    def __init__(self) -> None:
        self._captchas: dict[str, _VerificationValue] = {}
        self._sms_codes: dict[tuple[str, str], _VerificationValue] = {}

    async def save_captcha(self, captcha_id: str, code: str, expires_at: datetime) -> None:
        self._captchas[captcha_id] = _VerificationValue(
            code=code.upper(),
            expires_at=expires_at,
        )
        self._purge_expired()

    async def verify_captcha(self, captcha_id: str, code: str) -> bool:
        self._purge_expired()
        value = self._captchas.pop(captcha_id, None)
        return value is not None and value.code == code.strip().upper()

    async def save_sms_code(
        self,
        *,
        phone: str,
        purpose: str,
        code: str,
        expires_at: datetime,
    ) -> None:
        self._sms_codes[(phone, purpose.upper())] = _VerificationValue(
            code=code,
            expires_at=expires_at,
        )
        self._purge_expired()

    async def verify_sms_code(self, *, phone: str, purpose: str, code: str) -> bool:
        self._purge_expired()
        value = self._sms_codes.pop((phone, purpose.upper()), None)
        return value is not None and value.code == code.strip()

    def _purge_expired(self) -> None:
        now = datetime.now(UTC)
        self._captchas = {
            key: value for key, value in self._captchas.items() if value.expires_at > now
        }
        self._sms_codes = {
            key: value for key, value in self._sms_codes.items() if value.expires_at > now
        }
