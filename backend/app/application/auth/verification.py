from datetime import datetime
from typing import Protocol


class VerificationStore(Protocol):
    async def save_captcha(self, captcha_id: str, code: str, expires_at: datetime) -> None:
        raise NotImplementedError

    async def verify_captcha(self, captcha_id: str, code: str) -> bool:
        raise NotImplementedError

    async def save_sms_code(
        self,
        *,
        phone: str,
        purpose: str,
        code: str,
        expires_at: datetime,
    ) -> None:
        raise NotImplementedError

    async def verify_sms_code(self, *, phone: str, purpose: str, code: str) -> bool:
        raise NotImplementedError


class SmsSender(Protocol):
    async def send_code(self, *, phone: str, code: str, purpose: str) -> None:
        raise NotImplementedError
