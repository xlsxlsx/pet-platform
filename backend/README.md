# Pet Platform Backend

Python backend using FastAPI, MySQL and clean architecture.

## Layers

- `domain`: entities, value objects, policies, repository ports.
- `application`: use cases and DTOs.
- `infrastructure`: MySQL, security, third-party adapters.
- `interfaces`: FastAPI routers, dependencies, response mapping.

## Local Run

Recommended from the project root:

```powershell
.\scripts\init_mysql.ps1 -User root -Password <your-local-mysql-password>
cd backend
.\.venv312\Scripts\python.exe -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

Open another terminal for the web app:

```powershell
cd web
..\backend\.venv312\Scripts\python.exe -m http.server 5173 --bind 127.0.0.1
```

Then open:

- Backend: `http://127.0.0.1:8000`
- API docs: `http://127.0.0.1:8000/docs`
- Web app: `http://127.0.0.1:5173`

Run smoke checks:

```powershell
.\scripts\smoke_test.ps1
```

Manual backend setup:

```powershell
cd backend
python -m venv .venv312
.\.venv312\Scripts\Activate.ps1
pip install -e .[dev]
copy .env.example .env
uvicorn app.main:app --reload
```

Use visible terminal commands for local startup. Hidden background startup helpers are intentionally
not part of the recommended workflow because antivirus products may flag them.

Put real local secrets in `.env`. Do not commit `.env`.

## MVP APIs

- `GET /api/v1/health`
- `GET /api/v1/auth/captcha`
- `POST /api/v1/auth/sms-code`
- `POST /api/v1/auth/login`
- `POST /api/v1/auth/register`
- `GET /api/v1/dashboards/{role}`
- `GET /api/v1/catalog/products`
- `GET /api/v1/catalog/hospitals`

Auth uses phone + captcha + SMS code as the primary flow.
Passwords are no longer exposed in the UI or API contract.
Local `.env` can enable `AUTH_DEBUG_CODES=true` for manual testing; keep it disabled outside local development.

Supported dashboard roles:

- `CUSTOMER`
- `MERCHANT`
- `HOSPITAL`
- `ADMIN`
