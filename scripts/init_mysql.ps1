param(
    [string]$HostName = "127.0.0.1",
    [int]$Port = 3306,
    [string]$User = "root",
    [Parameter(Mandatory = $true)]
    [string]$Password
)

$ErrorActionPreference = "Stop"
$sqlPath = Join-Path $PSScriptRoot "..\backend\database\init_mysql.sql"
$mysqlSqlPath = (Resolve-Path $sqlPath).Path -replace "\\", "/"

if (-not (Test-Path $sqlPath)) {
    throw "SQL file not found: $sqlPath"
}

$env:MYSQL_PWD = $Password
try {
    mysql --host=$HostName --port=$Port --user=$User --default-character-set=utf8mb4 --execute="source $mysqlSqlPath"
    mysql --host=$HostName --port=$Port --user=$User --database=pet_platform --default-character-set=utf8mb4 --execute="SELECT r.code AS role_code, COUNT(ur.user_id) AS users FROM roles r LEFT JOIN user_roles ur ON ur.role_id = r.id GROUP BY r.code ORDER BY r.code;"
}
finally {
    Remove-Item Env:\MYSQL_PWD -ErrorAction SilentlyContinue
}
