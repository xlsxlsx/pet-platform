param(
    [string]$BaseUrl = "http://127.0.0.1:8000/api/v1"
)

$ErrorActionPreference = "Stop"

function Invoke-JsonPost {
    param(
        [string]$Uri,
        [hashtable]$Body
    )

    $json = $Body | ConvertTo-Json -Compress
    Invoke-RestMethod -Uri $Uri -Method Post -ContentType "application/json; charset=utf-8" -Body $json
}

$accounts = @(
    @{ role = "CUSTOMER"; phone = "13800000001" },
    @{ role = "MERCHANT"; phone = "13800000002" },
    @{ role = "HOSPITAL"; phone = "13800000003" },
    @{ role = "ADMIN"; phone = "13800000004" }
)

function Get-SmsCode {
    param(
        [string]$Phone,
        [string]$Purpose
    )

    $captcha = Invoke-RestMethod -Uri "$BaseUrl/auth/captcha" -Method Get
    if (-not $captcha.debug_code) {
        throw "Smoke test requires auth_debug_codes=true for captcha"
    }

    $sms = Invoke-JsonPost -Uri "$BaseUrl/auth/sms-code" -Body @{
        phone = $Phone
        captcha_id = $captcha.captcha_id
        captcha_code = $captcha.debug_code
        purpose = $Purpose
    }
    if (-not $sms.debug_code) {
        throw "Smoke test requires auth_debug_codes=true for sms"
    }
    return $sms.debug_code
}

$health = Invoke-RestMethod -Uri "$BaseUrl/health" -Method Get
if ($health.status -ne "ok") {
    throw "Health check failed"
}
Write-Host "OK health"

foreach ($account in $accounts) {
    $smsCode = Get-SmsCode -Phone $account.phone -Purpose "LOGIN"
    $session = Invoke-JsonPost -Uri "$BaseUrl/auth/login" -Body @{
        role = $account.role
        phone = $account.phone
        sms_code = $smsCode
    }
    if (-not $session.access_token -or $session.active_role -ne $account.role) {
        throw "Login failed for role $($account.role)"
    }

    $dashboard = Invoke-RestMethod -Uri "$BaseUrl/dashboards/$($account.role)" -Method Get
    if ($dashboard.metrics.Count -lt 1 -or $dashboard.tasks.Count -lt 1) {
        throw "Dashboard failed for role $($account.role)"
    }

    Write-Host "OK $($account.role) login and dashboard"
}

$products = Invoke-RestMethod -Uri "$BaseUrl/catalog/products?limit=3" -Method Get
if ($products.Count -lt 1) {
    throw "Product catalog is empty"
}
Write-Host "OK product catalog"

$hospitals = Invoke-RestMethod -Uri "$BaseUrl/catalog/hospitals?limit=3" -Method Get
if ($hospitals.Count -lt 1) {
    throw "Hospital catalog is empty"
}
Write-Host "OK hospital catalog"

$suffix = Get-Date -Format "HHmmss"
$newPhone = "13900$suffix"
$registerCode = Get-SmsCode -Phone $newPhone -Purpose "REGISTER"
$registration = Invoke-JsonPost -Uri "$BaseUrl/auth/register" -Body @{
    role = "CUSTOMER"
    phone = $newPhone
    sms_code = $registerCode
    display_name = "冒烟测试用户"
    organization_name = $null
}
if ($registration.active_role -ne "CUSTOMER") {
    throw "Customer registration failed"
}
Write-Host "OK customer registration"

$newLoginCode = Get-SmsCode -Phone $newPhone -Purpose "LOGIN"
$newLogin = Invoke-JsonPost -Uri "$BaseUrl/auth/login" -Body @{
    role = "CUSTOMER"
    phone = $newPhone
    sms_code = $newLoginCode
}
if ($newLogin.active_role -ne "CUSTOMER") {
    throw "Customer login after registration failed"
}
Write-Host "OK customer login after registration"

Write-Host "Smoke test passed."
