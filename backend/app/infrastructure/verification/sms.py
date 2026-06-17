import logging

logger = logging.getLogger(__name__)


def _mask_phone(phone: str) -> str:
    if len(phone) < 7:
        return "***"
    return f"{phone[:3]}****{phone[-4:]}"


class LocalSmsSender:
    async def send_code(self, *, phone: str, code: str, purpose: str) -> None:
        logger.info("local sms code issued", extra={"phone": _mask_phone(phone), "purpose": purpose})
