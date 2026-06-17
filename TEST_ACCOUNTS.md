# Test Accounts

Local database: `pet_platform`

These accounts are seeded by `backend/database/init_mysql.sql` and can be used to test the four role-specific login flows.

Login and registration now use phone verification codes as the primary credential. In local development, `AUTH_DEBUG_CODES=true` returns `debug_code` from the captcha and SMS endpoints so the browser and smoke test can fill the codes without a real SMS provider.

| User Type | Role | Phone | Notes |
| --- | --- | --- | --- |
| Customer | `CUSTOMER` | `13800000001` | Pet owner with pet profile, service orders, shop order, and hospital appointment |
| Merchant | `MERCHANT` | `13800000002` | Pet supply store account with products and mall order |
| Hospital | `HOSPITAL` | `13800000003` | Pet hospital account with hospital profile and appointment request |
| Admin | `ADMIN` | `13800000004` | Platform admin for review, tickets, and audit |

Extra test account:

| User Type | Role | Phone | Notes |
| --- | --- | --- | --- |
| Service provider sample | `CUSTOMER` | `13800000005` | Backing account for the seeded home-service provider |

## Local Login API Example

First fetch a captcha. Local mode includes `debug_code` only when `AUTH_DEBUG_CODES=true`; production should not.

```http
GET /api/v1/auth/captcha
```

Then send the SMS code after submitting the captcha.

```http
POST /api/v1/auth/sms-code
Content-Type: application/json

{
  "phone": "13800000001",
  "captcha_id": "<captcha_id>",
  "captcha_code": "<captcha_debug_code>",
  "purpose": "LOGIN"
}
```

Use the SMS `debug_code` as `sms_code` in local development.

```http
POST /api/v1/auth/login
Content-Type: application/json

{
  "phone": "13800000001",
  "sms_code": "<sms_debug_code>",
  "role": "CUSTOMER"
}
```

## Register API Example

Use `purpose: "REGISTER"` when sending the SMS code.

```http
POST /api/v1/auth/register
Content-Type: application/json

{
  "phone": "13900000001",
  "sms_code": "<sms_debug_code>",
  "display_name": "New User",
  "role": "CUSTOMER",
  "organization_name": null
}
```

For `MERCHANT`, `organization_name` is the store name.
For `HOSPITAL`, `organization_name` is the hospital name.
