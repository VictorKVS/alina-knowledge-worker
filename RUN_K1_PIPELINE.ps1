param(
    [string]$RegistryRoot = "G:\1\FATHER\data\source_registry"
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $root

$python = Join-Path $root ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}

Write-Host "============================================================"
Write-Host "ALINA / FATHER — K1 AUTO PIPELINE"
Write-Host "Registry: $RegistryRoot"
Write-Host "Stops automatically at first BLOCKED/HUMAN_GATE"
Write-Host "============================================================"

& $python -B "$root\k1_pipeline.py" --registry-root $RegistryRoot
$code = $LASTEXITCODE

Write-Host ""
Write-Host "Dashboard data:"
Write-Host "  $root\data\k1-run\latest.json"
Write-Host "Development journal:"
Write-Host "  $root\data\k1-run\DEV_JOURNAL_K1.md"
Write-Host ""

if ($code -eq 2) {
    Write-Host "K1 stopped on a BLOCKED stage." -ForegroundColor Yellow
} elseif ($code -eq 0) {
    Write-Host "K1 completed validation up to the first permitted gate." -ForegroundColor Green
}

exit $code
