# Local Testing

The local environment has been configured.

## Running Services

Backend API:

```text
http://127.0.0.1:8000
```

API docs:

```text
http://127.0.0.1:8000/docs
```

Web app:

```text
http://127.0.0.1:5173
```

## Visible Manual Start

From the project root:

```powershell
.\scripts\init_mysql.ps1 -User root -Password <your-local-mysql-password>
```

Open one terminal for the backend:

```powershell
cd backend
.\.venv312\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open another terminal for the web app:

```powershell
cd web
..\backend\.venv312\Scripts\python.exe -m http.server 5173 --bind 127.0.0.1
```

To stop local services, press `Ctrl+C` in the two terminal windows.

## Smoke Test

After the backend and web servers are running, run:

```powershell
.\scripts\smoke_test.ps1
```

The script checks:

- `GET /api/v1/health`
- captcha and local SMS-code issuing
- four seeded role logins
- four role dashboards
- product catalog
- hospital catalog
- one new customer registration and login after registration

## Database

Local MySQL database:

```text
pet_platform
```

Manual database initialization:

```powershell
.\scripts\init_mysql.ps1 -User root -Password <your-local-mysql-password>
```

## Backend

Virtual environment:

```text
backend\.venv312
```

Start backend manually:

```powershell
cd backend
.\.venv312\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Install runtime dependencies with a China-friendly mirror:

```powershell
cd backend
.\.venv312\Scripts\python.exe -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple fastapi "uvicorn[standard]" pydantic-settings sqlalchemy aiomysql pytest pytest-asyncio httpx ruff
```

The previous startup helper has been removed from the recommended workflow because hidden
background process launchers can trigger antivirus warnings. Use the visible commands above.

## Web

Start web manually:

```powershell
cd web
..\backend\.venv312\Scripts\python.exe -m http.server 5173 --bind 127.0.0.1
```

## Test Accounts

See:

```text
TEST_ACCOUNTS.md
```

## Local Security Note

`backend\.env` keeps `ALLOW_ADMIN_REGISTRATION=true` and `AUTH_DEBUG_CODES=true` so the local four-role registration flow can be tested without a real SMS provider. The code defaults are safer; keep administrator self-registration and debug verification-code responses disabled outside local development.
