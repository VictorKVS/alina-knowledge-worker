# ================================================================
# FATHER / ALINA — STAGE 05 / TELEGRAM QA REPORTER V2
# Tests + sanitized GitHub evidence + remote verification
# ================================================================
param([string]$RepoRoot = "G:\1\alina-knowledge-worker")
$ErrorActionPreference = "Stop"
$Branch = "feature/alina-k3-k10-autopilot"
$RelDir = "autopilot/projects/ALINA_INTELLIGENCE_RESEARCH/telegram"
$ReportRel = "$RelDir/evidence/TELEGRAM_QA_LATEST.md"
$LocalFallback = Join-Path $env:TEMP "FATHER_ALINA_QA_LAST_REPORT.md"

function Invoke-Git([string[]]$Arguments) {
    & git @Arguments
    if ($LASTEXITCODE -ne 0) { throw "git command failed: $($Arguments[0]) (exit $LASTEXITCODE)" }
}
function Write-Report([string]$Status,[int]$Code,[string]$Commit,[string]$Note,[string]$ErrHash) {
    $at = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")
    $lines = @(
        "# FATHER / ALINA - Telegram QA",
        "",
        "- Status: $Status",
        "- UTC: $at",
        "- Branch: $Branch",
        "- Tested commit: $Commit",
        "- Test exit code: $Code",
        "- stderr SHA256: $ErrHash",
        "- Test command: python -m unittest discover -s . -p test_*.py -v",
        "- Scope: offline tests only; live Telegram and TDLib NOT TESTED.",
        "- Diagnostic: $Note"
    )
    [IO.File]::WriteAllLines($LocalFallback,[string[]]$lines,[Text.UTF8Encoding]::new($false))
    $target = Join-Path $RepoRoot ($ReportRel -replace "/", [IO.Path]::DirectorySeparatorChar)
    New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null
    [IO.File]::WriteAllLines($target,[string[]]$lines,[Text.UTF8Encoding]::new($false))
}
try {
    Set-Location $RepoRoot
    $top = (& git rev-parse --show-toplevel).Trim()
    if ($LASTEXITCODE -ne 0) { throw "Not a Git working tree" }
    $current = (& git branch --show-current).Trim()
    if ($current -ne $Branch) { throw "Expected branch $Branch, found $current. Switch manually, preserving local changes." }
    $remote = (& git remote get-url origin).Trim()
    if ($LASTEXITCODE -ne 0 -or -not $remote) { throw "Origin remote is not configured" }

    # No reset, checkout or clean. Pull only when safely fast-forwardable.
    Invoke-Git @("fetch","origin",$Branch)
    Invoke-Git @("merge","--ff-only","FETCH_HEAD")
    $head = (& git rev-parse HEAD).Trim()

    $TestDir = Join-Path $RepoRoot $RelDir
    $stdout = Join-Path $env:TEMP "father_alina_qa_v2.stdout.txt"
    $stderr = Join-Path $env:TEMP "father_alina_qa_v2.stderr.txt"
    $python = (Get-Command python -ErrorAction Stop).Source
    $proc = Start-Process -FilePath $python -ArgumentList @("-m","unittest","discover","-s",".","-p","test_*.py","-v") -WorkingDirectory $TestDir -Wait -PassThru -RedirectStandardOutput $stdout -RedirectStandardError $stderr
    $testCode = $proc.ExitCode
    $hash = (Get-FileHash -Algorithm SHA256 $stderr).Hash
    $status = if ($testCode -eq 0) { "PASS" } else { "FAIL" }
    $summary = if ($testCode -eq 0) { "Offline test runner returned exit code zero" } else { "Tests failed; full log kept locally, not published" }
    Write-Report $status $testCode $head $summary $hash

    Invoke-Git @("add","--",$ReportRel)
    & git diff --cached --quiet -- $ReportRel
    if ($LASTEXITCODE -eq 1) {
        Invoke-Git @("commit","-m","test(alina): publish safe Telegram QA evidence","--",$ReportRel)
    } elseif ($LASTEXITCODE -ne 0) { throw "git diff staged validation failed" }
    Invoke-Git @("push","origin",$Branch)
    Invoke-Git @("fetch","origin",$Branch)
    # git show verifies remote ref rather than local working tree
    & git show ("refs/remotes/origin/" + $Branch + ":" + $ReportRel) | Out-Null
    if ($LASTEXITCODE -ne 0) { throw "Remote report missing after git push" }
    Write-Host "GITHUB_REPORT_VERIFIED" -ForegroundColor Green
    Write-Host "QA_STATUS=$status" -ForegroundColor $(if ($status -eq "PASS") { "Green" } else { "Yellow" })
    Write-Host "2" -ForegroundColor Cyan
} catch {
    Write-Host ("ERROR: " + $_.Exception.Message) -ForegroundColor Red
    Write-Host ("Local fallback report: " + $LocalFallback) -ForegroundColor Yellow
    Write-Host "Do not report PASS. Send the visible ERROR line if GitHub push cannot complete."
    exit 1
}
