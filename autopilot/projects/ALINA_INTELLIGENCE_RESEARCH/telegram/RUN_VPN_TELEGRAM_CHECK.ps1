# ==============================================================
# FATHER / ALINA — ЭТАП 06
# ЗАПУСК AMNEZIAVPN -> ПРОВЕРКА ДОСТУПА К TELEGRAM -> GITHUB
# Не меняет параметры VPN, TDLib и основную локальную ветку.
# ==============================================================
param([string]$RepoRoot="G:\1\alina-knowledge-worker")
$ErrorActionPreference="Stop"
$Branch="feature/alina-k3-k10-autopilot"
$ReportRel="autopilot/projects/ALINA_INTELLIGENCE_RESEARCH/telegram/evidence/VPN_TELEGRAM_QA_LATEST.md"
$Diagnostics = New-Object System.Collections.Generic.List[string]
$VpnRunning=$false; $TcpApi=$false; $TcpWeb=$false; $HttpsApi=$false
$Published=$false

Write-Host "=== FATHER / ALINA — AMNEZIA VPN + TELEGRAM ===" -ForegroundColor Cyan
$Running = @(Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match "amnezia" })
if ($Running.Count -gt 0) { $VpnRunning=$true; Write-Host "AmneziaVPN: приложение запущено" -ForegroundColor Green }
else {
    $candidates=@(
        "$env:ProgramFiles\AmneziaVPN\AmneziaVPN.exe",
        "${env:ProgramFiles(x86)}\AmneziaVPN\AmneziaVPN.exe",
        "$env:LOCALAPPDATA\Programs\AmneziaVPN\AmneziaVPN.exe",
        "$env:LOCALAPPDATA\AmneziaVPN\AmneziaVPN.exe"
    )
    $Exe=$candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
    if ($Exe) {
        Start-Process -FilePath $Exe
        Start-Sleep -Seconds 3
        $VpnRunning=@(Get-Process -ErrorAction SilentlyContinue | Where-Object { $_.ProcessName -match "amnezia" }).Count -gt 0
        Write-Host "AmneziaVPN: попытка запуска выполнена" -ForegroundColor Yellow
    } else { Write-Host "AmneziaVPN.exe не найден по стандартным путям. Открой VPN вручную." -ForegroundColor Yellow }
}
Write-Host "Подключи в AmneziaVPN свой существующий профиль и дождись статуса «Подключено»." -ForegroundColor Cyan
Read-Host "Когда VPN подключён, нажми ENTER для автоматической проверки" | Out-Null

try { $TcpApi = [bool](Test-NetConnection "api.telegram.org" -Port 443 -InformationLevel Quiet -WarningAction SilentlyContinue) } catch {}
try { $TcpWeb = [bool](Test-NetConnection "web.telegram.org" -Port 443 -InformationLevel Quiet -WarningAction SilentlyContinue) } catch {}
try {
    $response=Invoke-WebRequest -Uri "https://api.telegram.org" -Method Get -UseBasicParsing -TimeoutSec 12 -ErrorAction Stop
    $HttpsApi=$true
} catch {
    # A Telegram API HTTP error response still means HTTPS transport may be available.
    if ($_.Exception.Response) { $HttpsApi=$true }
}
$VpnProcessStatus=if($VpnRunning){"DETECTED"}else{"NOT_DETECTED"}
$Status=if($TcpApi -and $TcpWeb -and $HttpsApi){"NETWORK_OK"}else{"NETWORK_CHECK_FAILED"}
$now=[DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")
$lines=@(
"# FATHER / ALINA — VPN и доступность Telegram",
"",
"- Дата UTC: $now",
"- AmneziaVPN приложение: $VpnProcessStatus",
"- TCP api.telegram.org:443: $TcpApi",
"- TCP web.telegram.org:443: $TcpWeb",
"- HTTPS api.telegram.org: $HttpsApi",
"- Итог проверки сети: **$Status**",
"- Важно: проверка не доказывает использование VPN-маршрута и успешное подключение TDLib.",
"- VPN-адреса, IP пользователя, ключи и данные Telegram не записываются.",
"- Отчёт сформирован на компьютере, результат должен быть опубликован в GitHub."
)
$localReport=Join-Path $env:TEMP "FATHER_ALINA_VPN_TELEGRAM_QA.md"
[IO.File]::WriteAllLines($localReport,[string[]]$lines,[Text.UTF8Encoding]::new($false))
Write-Host "Локальный отчёт: $localReport" -ForegroundColor Cyan

# Local branch is diverged; use a detached worktree at remote HEAD to publish only evidence.
$worktree=Join-Path $env:TEMP ("FATHER_QA_PUBLISH_"+[guid]::NewGuid().ToString("N"))
try {
    Set-Location $RepoRoot
    & git fetch origin $Branch
    if($LASTEXITCODE -ne 0){throw "GitHub: ошибка получения удалённой ветки"}
    & git worktree add --detach $worktree ("origin/"+$Branch)
    if($LASTEXITCODE -ne 0){throw "GitHub: не удалось создать временную копию"}
    $target=Join-Path $worktree ($ReportRel -replace "/", [IO.Path]::DirectorySeparatorChar)
    New-Item -ItemType Directory -Force -Path (Split-Path $target) | Out-Null
    Copy-Item $localReport $target -Force
    Push-Location $worktree
    try {
        & git add -- $ReportRel
        if($LASTEXITCODE -ne 0){throw "GitHub: ошибка git add"}
        & git diff --cached --quiet -- $ReportRel
        if($LASTEXITCODE -eq 1) {
            & git commit -m "Алина: сохранены результаты проверки VPN и Telegram" -- $ReportRel
            if($LASTEXITCODE -ne 0){throw "GitHub: ошибка git commit"}
        }
        & git push origin ("HEAD:refs/heads/"+$Branch)
        if($LASTEXITCODE -ne 0){throw "GitHub: не удалось отправить отчёт"}
        & git fetch origin $Branch
        if($LASTEXITCODE -ne 0){throw "GitHub: ошибка подтверждения"}
        $remotereport=& git show ("origin/"+$Branch+":"+$ReportRel)
        if($LASTEXITCODE -ne 0){throw "GitHub: удалённый отчёт не найден"}
        $Published=$true
    } finally { Pop-Location }
} catch { Write-Host ("Ошибка отправки отчёта: "+$_.Exception.Message) -ForegroundColor Red }
finally {
    if(Test-Path $worktree) {
        Set-Location $RepoRoot
        & git worktree remove --force $worktree 2>$null
    }
}
if($Published) { Write-Host "ОТЧЁТ ПОДТВЕРЖДЁН В GITHUB — $Status" -ForegroundColor Green; Write-Host "2" -ForegroundColor Cyan }
else { Write-Host "ОТЧЁТ ТОЛЬКО ЛОКАЛЬНО: $localReport" -ForegroundColor Yellow; exit 1 }
