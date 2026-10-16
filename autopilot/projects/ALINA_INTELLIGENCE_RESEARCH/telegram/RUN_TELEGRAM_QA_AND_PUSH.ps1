# ============================================================
# FATHER / ALINA — TELEGRAM QA + GITHUB EVIDENCE
# STAGE 02: pull, test, publish sanitized status
# ============================================================
param([string]$RepoRoot = "", [switch]$SkipPull)
$ErrorActionPreference = "Stop"
if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..\..\..")).Path
}
$TargetBranch = "feature/alina-k3-k10-autopilot"
$EvidenceRelative = "autopilot/projects/ALINA_INTELLIGENCE_RESEARCH/telegram/evidence/TELEGRAM_QA_LATEST.md"
$Evidence = Join-Path $RepoRoot ($EvidenceRelative -replace "/", "\")
$TestsDir = Join-Path $RepoRoot "autopilot/projects/ALINA_INTELLIGENCE_RESEARCH/telegram"
Write-Host "=== FATHER / ALINA — TELEGRAM QA + GITHUB ===" -ForegroundColor Cyan
Set-Location $RepoRoot
if ((git rev-parse --show-toplevel).Trim() -ne ($RepoRoot -replace "\\","/")) {
    Write-Host "Repository path may use different canonical spelling. Continuing with explicit root." -ForegroundColor Yellow
}
$Branch = (git branch --show-current).Trim()
if ($Branch -ne $TargetBranch) {
    throw "Wrong branch: '$Branch'. Switch to '$TargetBranch' manually first; no automatic branch switch over local changes."
}
if (-not $SkipPull) {
    git pull --ff-only origin $TargetBranch
    if ($LASTEXITCODE -ne 0) { throw "git pull failed; local modifications/branches need attention" }
}
New-Item -ItemType Directory -Force -Path (Split-Path $Evidence) | Out-Null
$Timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
$Commit = (git rev-parse HEAD).Trim()
$RawLog = Join-Path $env:TEMP "father_alina_telegram_qa.log"
Push-Location $TestsDir
try {
    & python -m unittest discover -s . -p "test_pipeline.py" -v 2>&1 | Out-File -FilePath $RawLog -Encoding utf8
    $ExitCode = $LASTEXITCODE
} finally { Pop-Location }
# Publish ONLY a machine-generated summary, not raw stdout: paths, tokens or PII can leak via failures.
$Status = if ($ExitCode -eq 0) { "PASS" } else { "FAIL" }
$Digest = (Get-FileHash -Algorithm SHA256 $RawLog).Hash
$Report = @"
# FATHER / ALINA — Telegram Offline QA
- Result: **$Status**
- UTC: $Timestamp
- Tested commit: `$Commit`
- Command: `python -m unittest discover -s . -p "test_pipeline.py" -v`
- Exit code: $ExitCode
- Raw log SHA-256 (raw log NOT uploaded): `$Digest`
- Scope: offline JSONL classification tests only; no live TDLib or Telegram connection tested.
- Generated automatically by RUN_TELEGRAM_QA_AND_PUSH.ps1.
"@
Set-Content -Path $Evidence -Value $Report -Encoding UTF8
git add -- $EvidenceRelative
if ($LASTEXITCODE -ne 0) { throw "git add failed" }
git diff --cached --quiet
$HasChange = $LASTEXITCODE -eq 1
if ($HasChange) {
    git commit -m "test(alina): record Telegram offline QA status"
    if ($LASTEXITCODE -ne 0) { throw "git commit failed" }
    git push origin $TargetBranch
    if ($LASTEXITCODE -ne 0) { throw "git push failed" }
}
Write-Host "GitHub evidence: $EvidenceRelative" -ForegroundColor Green
Write-Host "Test status: $Status" -ForegroundColor $(if ($ExitCode -eq 0) { "Green" } else { "Red" })
Write-Host "Raw log (local only): $RawLog"
Write-Host "2" -ForegroundColor Cyan
if ($ExitCode -ne 0) { exit $ExitCode }
