# API Overview

Base path: `/api/v1`

## Health

```http
GET /api/v1/health
```

Returns API health status.

## Auth

```http
GET /api/v1/auth/captcha
POST /api/v1/auth/sms-code
POST /api/v1/auth/login
POST /api/v1/auth/register
```

Login and registration are phone-code based.
`/auth/captcha` returns an image captcha. It returns `debug_code` only when `AUTH_DEBUG_CODES=true` in local development.
`/auth/sms-code` verifies the captcha first, then issues a login or register SMS code.
`/auth/login` and `/auth/register` consume `sms_code` instead of passwords.
Supports `CUSTOMER`, `MERCHANT`, `HOSPITAL`, and `ADMIN` role login/register.

## Role Dashboards

```http
GET /api/v1/dashboards/CUSTOMER
GET /api/v1/dashboards/MERCHANT
GET /api/v1/dashboards/HOSPITAL
GET /api/v1/dashboards/ADMIN
```

Returns role-specific metrics and task lists.

## Catalog

```http
GET /api/v1/catalog/products
GET /api/v1/catalog/hospitals
```

Returns product and hospital summaries for user-facing browsing.

## Notes

- Current endpoints are read models for MVP simulation.
- Authentication and RBAC middleware should be added before exposing write operations.
- Account listing is intentionally not exposed in the MVP API. Add it back only as an authenticated administrator endpoint.
- Response shapes are typed by Pydantic DTOs in `backend/app/application`.
