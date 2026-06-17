from fastapi import APIRouter, Depends, HTTPException

from app.application.auth.dtos import (
    AuthSessionDTO,
    CaptchaDTO,
    LoginCommand,
    RegisterCommand,
    SmsCodeCommand,
    SmsCodeDTO,
)
from app.application.auth.use_cases import (
    CreateCaptchaUseCase,
    LoginUseCase,
    RegisterUseCase,
    SendSmsCodeUseCase,
)
from app.interfaces.http.dependencies import (
    get_create_captcha_use_case,
    get_login_use_case,
    get_register_use_case,
    get_send_sms_code_use_case,
)

router = APIRouter()


@router.get("/captcha", response_model=CaptchaDTO)
async def captcha(
    use_case: CreateCaptchaUseCase = Depends(get_create_captcha_use_case),
) -> CaptchaDTO:
    return await use_case.execute()


@router.post("/sms-code", response_model=SmsCodeDTO)
async def send_sms_code(
    command: SmsCodeCommand,
    use_case: SendSmsCodeUseCase = Depends(get_send_sms_code_use_case),
) -> SmsCodeDTO:
    try:
        return await use_case.execute(command)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@router.post("/login", response_model=AuthSessionDTO)
async def login(
    command: LoginCommand,
    use_case: LoginUseCase = Depends(get_login_use_case),
) -> AuthSessionDTO:
    try:
        return await use_case.execute(command)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc


@router.post("/register", response_model=AuthSessionDTO)
async def register(
    command: RegisterCommand,
    use_case: RegisterUseCase = Depends(get_register_use_case),
) -> AuthSessionDTO:
    try:
        return await use_case.execute(command)
    except PermissionError as exc:
        raise HTTPException(status_code=403, detail=str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
