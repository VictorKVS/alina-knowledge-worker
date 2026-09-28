param(
    [string]$RegistryRoot = "G:\\1\\FATHER\\data\\source_registry",
    [string]$HomeRoot = "G:\\1"
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $RepoRoot

$Python = Join-Path $RepoRoot ".venv\\Scripts\\python.exe"
if (-not (Test-Path $Python)) {
    $Python = (Get-Command python -ErrorAction Stop).Source
}

Write-Host "============================================================"
Write-Host "ALINA / FATHER — K1 AUTONOMOUS PROJECT"
Write-Host "Repository : $RepoRoot"
Write-Host "Registry   : $RegistryRoot"
Write-Host "Home root  : $HomeRoot"
Write-Host "Mode       : AUTO until BLOCKED/HUMAN_GATE"
Write-Host "============================================================"

$ArgsList = @(
    "-B",
    "$RepoRoot\\k1_autoproject.py",
    "--registry-root", $RegistryRoot,
    "--home-root", $HomeRoot
)

& $Python @ArgsList
$Code = $LASTEXITCODE

$Latest = Join-Path $RepoRoot "data\\k1-run\\latest.json"

if (Test-Path $Latest) {
    $Run = Get-Content $Latest -Raw -Encoding UTF8 | ConvertFrom-Json

    Write-Host ""
    Write-Host "============================================================"
    Write-Host "K1 SUMMARY"
    Write-Host "============================================================"
    Write-Host "Run ID           : $($Run.run_id)"
    Write-Host "Stop reason      : $($Run.stop_reason)"
    Write-Host "First human gate : $($Run.first_human_gate)"
    Write-Host ""

    $Run.stages |
        Select-Object stage,status,read_records,written_records,created,updated,warnings,errors,duration_seconds,detail |
        Format-Table -Wrap -AutoSize

    Write-Host ""
    Write-Host "Metrics:"
    $Run.metrics | Format-List

    Write-Host ""
    Write-Host "Safety:"
    $Run.safety | Format-List
}

Write-Host ""
Write-Host "Runtime outputs:"
Write-Host "  $RepoRoot\\data\\k1-run\\latest.json"
Write-Host "  $RepoRoot\\data\\k1-run\\history.jsonl"
Write-Host "  $RepoRoot\\data\\k1-run\\DEV_JOURNAL_K1.md"
Write-Host ""
Write-Host "Original documents are never modified, moved or deleted."

exit $Code
