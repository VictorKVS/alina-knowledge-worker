# ============================================================
# FATHER / ALINA — TELEGRAM QA: RUN TESTS AND PUSH SAFE EVIDENCE
# Compatible with Windows PowerShell 5.1 and PowerShell 7
# ============================================================
param([string]$RepoRoot = "")
$ErrorActionPreference = "Stop"
$BranchName = "feature/alina-k3-k10-autopilot"
$Rel = "autopilot/projects/ALINA_INTELLIGENCE_RESEARCH/telegram/evidence/TELEGRAM_QA_LATEST.md"
if (-not $RepoRoot) {
    $RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "../../../..")).Path
}
Set-Location $RepoRoot
Write-Host "=== FATHER / ALINA / TELEGRAM QA ===" -ForegroundColor Cyan
$Current = (& git branch --show-current).Trim()
if ($LASTEXITCODE -ne 0 -or $Current -ne $BranchName) { throw "Expected branch $BranchName. Actual: $Current" }
$TestDir = Join-Path $RepoRoot "autopilot/projects/ALINA_INTELLIGENCE_RESEARCH/telegram"
$LogPath = Join-Path $env:TEMP "father_alina_telegram_qa_stdout_stderr.log"
$Py = (Get-Command python -ErrorAction Stop).Source
$ReportPath = Join-Path $RepoRoot ($Rel -replace "/", [IO.Path]::DirectorySeparatorChar)
# Start-Process redirects both streams without PowerShell 5.1 native STDERR promotion.
$Process = Start-Process -FilePath $Py -ArgumentList @("-m","unittest","discover","-s",".","-p","test_pipeline.py","-v") -WorkingDirectory $TestDir -Wait -PassThru -RedirectStandardOutput ($LogPath + ".out") -RedirectStandardError ($LogPath + ".err") -NoNewWindow
$ExitCode = $Process.ExitCode
$Status = if ($ExitCode -eq 0) { "PASS" } else { "FAIL" }
$TimeUtc = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")
$Sha = (& git rev-parse HEAD).Trim()
$ErrHash = (Get-FileHash -Algorithm SHA256 ($LogPath + ".err")).Hash
$OutHash = (Get-FileHash -Algorithm SHA256 ($LogPath + ".out")).Hash
New-Item -ItemType Directory -Force -Path (Split-Path $ReportPath) | Out-Null
$Lines = @(
    "# FATHER / ALINA — Telegram Offline QA",
    "",
    "- Status: **$Status**",
    "- UTC: $TimeUtc",
    "- Tested commit: $Sha",
    "- Exit code: $ExitCode",
    "- Command: python -m unittest discover -s . -p test_pipeline.py -v",
    "- stdout SHA256: $OutHash",
    "- stderr SHA256: $ErrHash",
    "- Scope: offline candidate-intake tests only. No Telegram API/TDLib connection was tested.",
    "- Raw logs are kept locally in the user's temporary directory, not pushed to GitHub."
)
[IO.File]::WriteAllLines($ReportPath, [string[]]$Lines, [Text.UTF8Encoding]::new($false))
# Stage ONLY known evidence path. Do not upload messages, secrets or unrelated files.
& git add -- $Rel
if ($LASTEXITCODE -ne 0) { throw "git add failed" }
& git diff --cached --quiet -- $Rel
if ($LASTEXITCODE -eq 1) {
    & git commit -m "test(alina): record offline Telegram QA status" -- $Rel
    if ($LASTEXITCODE -ne 0) { throw "git commit failed" }
}
& git push origin $BranchName
if ($LASTEXITCODE -ne 0) { throw "git push failed: verify remote permissions and conflicts" }
Write-Host "QA=$Status; evidence uploaded to $Rel" -ForegroundColor $(if($ExitCode -eq 0){"Green"}else{"Red"})
Write-Host "2" -ForegroundColor Cyan
if ($ExitCode -ne 0) { exit $ExitCode }
