from pydantic import BaseModel, Field

PHONE_PATTERN = r"^1[3-9]\d{9}$"
ROLE_PATTERN = r"^(CUSTOMER|MERCHANT|HOSPITAL|ADMIN)$"


class CaptchaDTO(BaseModel):
    captcha_id: str
    image_base64: str
    expires_in_seconds: int
    debug_code: str | None = None


class SmsCodeCommand(BaseModel):
    phone: str = Field(pattern=PHONE_PATTERN)
    captcha_id: str = Field(min_length=8, max_length=128)
    captcha_code: str = Field(min_length=4, max_length=8)
    purpose: str = Field(pattern="^(LOGIN|REGISTER)$")


class SmsCodeDTO(BaseModel):
    phone: str
    purpose: str
    expires_in_seconds: int
    debug_code: str | None = None


class LoginCommand(BaseModel):
    phone: str = Field(pattern=PHONE_PATTERN)
    sms_code: str = Field(min_length=4, max_length=8)
    role: str = Field(pattern=ROLE_PATTERN)


class RegisterCommand(BaseModel):
    phone: str = Field(pattern=PHONE_PATTERN)
    sms_code: str = Field(min_length=4, max_length=8)
    display_name: str = Field(min_length=1, max_length=80)
    role: str = Field(pattern=ROLE_PATTERN)
    organization_name: str | None = Field(default=None, max_length=120)


class AuthSessionDTO(BaseModel):
    user_id: int
    phone: str
    display_name: str
    roles: list[str]
    active_role: str
    access_token: str
