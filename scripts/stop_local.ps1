param(
    [switch]$Kill
)

$ErrorActionPreference = "Stop"

$connections = Get-NetTCPConnection -LocalPort 8000, 5173 -State Listen -ErrorAction SilentlyContinue
if (-not $connections) {
    Write-Host "No local services are listening on ports 8000 or 5173."
    return
}

$processIds = $connections | Select-Object -ExpandProperty OwningProcess -Unique
Write-Host "Processes listening on ports 8000 or 5173:"
foreach ($processId in $processIds) {
    Get-Process -Id $processId -ErrorAction SilentlyContinue |
        Select-Object Id, ProcessName, Path |
        Format-List
}

if (-not $Kill) {
    Write-Host "Press Ctrl+C in the visible backend/web terminal windows to stop services."
    Write-Host "If a process is stuck, re-run this script with: .\scripts\stop_local.ps1 -Kill"
    return
}

foreach ($processId in $processIds) {
    Stop-Process -Id $processId -ErrorAction SilentlyContinue
}

Write-Host "Stop signal sent to local services on ports 8000 and 5173."
