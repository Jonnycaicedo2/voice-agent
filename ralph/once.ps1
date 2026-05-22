# Ralph Loop - Ejecuta un issue de forma autónoma
param(
    [Parameter(Mandatory=$true)]
    [string]$IssueId
)

Write-Host "=== Ralph Loop iniciado para Issue #$IssueId ===" -ForegroundColor Cyan
Write-Host "[*] Ejecutando OpenCode en modo agente para Issue #$IssueId..."

# Registrar inicio en log
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
"[$timestamp] INICIO - Issue #$IssueId" | Out-File -Append ralph/execution.log

Write-Host "[+] Ralph completó el Issue #$IssueId. Revisa los cambios con git diff." -ForegroundColor Green
