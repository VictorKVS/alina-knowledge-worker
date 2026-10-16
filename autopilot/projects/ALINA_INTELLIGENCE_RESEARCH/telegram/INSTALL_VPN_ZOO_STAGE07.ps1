# ============================================================
# FATHER / ALINA - STAGE 07 - VPN ZOO REINSTALL
# Windows PowerShell 5.1, ASCII-only script for safe parsing
# ============================================================
param([string]$RepoRoot="G:\1\alina-knowledge-worker")
$ErrorActionPreference="Stop"
$branch="feature/alina-k3-k10-autopilot"
$relative="autopilot/projects/ALINA_INTELLIGENCE_RESEARCH/telegram/evidence/VPN_INSTALL_STAGE07.md"
$log=Join-Path $env:TEMP "FATHER_VPN_ZOO_STAGE07.md"
$results=New-Object System.Collections.Generic.List[string]
$results.Add("# FATHER / ALINA - VPN installation stage 07")
$results.Add("")
$results.Add("- UTC: $([DateTime]::UtcNow.ToString('yyyy-MM-ddTHH:mm:ssZ'))")
$results.Add("- Amnezia profile backup: confirmed by user (contents NOT accessed).")
$results.Add("- No account passwords, tokens, private IPs or config values collected.")
$results.Add("")
$ids=@("AmneziaVPN.AmneziaVPN","Proton.ProtonVPN","Windscribe.Windscribe")
function RunWinget([string]$step,[string[]]$commandArgs) {
  Write-Host ("VPN ZOO: "+$step) -ForegroundColor Cyan
  & winget @commandArgs
  $rc=$LASTEXITCODE
  $results.Add(("- "+$step+": exit code "+$rc))
  return $rc
}
try {
  & winget --version
  if($LASTEXITCODE -ne 0){throw "winget not available"}
  foreach($id in $ids) {
    & winget show --id $id --exact --source winget --accept-source-agreements | Out-Null
    if($LASTEXITCODE -ne 0){throw ("Package not found in winget source: "+$id)}
  }
  Write-Host "Back up Amnezia settings before uninstalling. Do not remove VPN server or keys." -ForegroundColor Yellow
  $answer=Read-Host "Type REINSTALL to confirm uninstalling AmneziaVPN application"
  if($answer -ne "REINSTALL") { throw "User cancelled uninstall; no changes to VPN apps" }
  # The native uninstaller may show UAC and UI. Do not force-remove profiles.
  $found=& winget list --id "AmneziaVPN.AmneziaVPN" --exact --source winget 2>$null
  if($LASTEXITCODE -eq 0 -and (($found -join " ") -match "AmneziaVPN")) {
    $r=RunWinget "Uninstall AmneziaVPN application" @("uninstall","--id","AmneziaVPN.AmneziaVPN","--exact","--source","winget")
    if($r -ne 0){throw "AmneziaVPN uninstall failed; use Apps > Installed apps or official updater"}
  } else { $results.Add("- AmneziaVPN: winget did not list an installed version; skip uninstall") }
  foreach($id in $ids) {
    $r=RunWinget ("Install "+$id) @("install","--id",$id,"--exact","--source","winget","--accept-package-agreements","--accept-source-agreements")
    if($r -ne 0) {
      # package may already be present; winget upgrade is the non-destructive path
      $r=RunWinget ("Upgrade "+$id) @("upgrade","--id",$id,"--exact","--source","winget","--accept-package-agreements","--accept-source-agreements")
      if($r -ne 0){throw ("Installation/upgrade failed: "+$id)}
    }
  }
  $results.Add("- Stage result: COMPLETED_INSTALLATION_COMMANDS")
  $results.Add("- Live VPN tunnel and Telegram TDLib access: NOT TESTED")
} catch {
  $results.Add("- Stage result: ERROR")
  $results.Add("- Error category: installation or local command failed; inspect PowerShell output.")
  Write-Host ("STAGE 07 ERROR: "+$_.Exception.Message) -ForegroundColor Red
} finally {
  [IO.File]::WriteAllLines($log,[string[]]$results,(New-Object Text.UTF8Encoding($false)))
  Write-Host ("Sanitized local report: "+$log)
}
# Dedicated temporary Git worktree prevents altering the diverged local branch.
$worktree=Join-Path $env:TEMP ("FATHER_VPN_STAGE07_"+[guid]::NewGuid().ToString("N"))
try {
  Set-Location $RepoRoot
  & git fetch origin $branch
  if($LASTEXITCODE -ne 0){throw "fetch failed"}
  & git worktree add --detach $worktree ("origin/"+$branch)
  if($LASTEXITCODE -ne 0){throw "worktree failed"}
  $dest=Join-Path $worktree ($relative -replace "/", [IO.Path]::DirectorySeparatorChar)
  New-Item -ItemType Directory -Force (Split-Path $dest)|Out-Null
  Copy-Item $log $dest
  Push-Location $worktree
  try {
    & git add -- $relative
    if($LASTEXITCODE -ne 0){throw "git add failed"}
    & git diff --cached --quiet -- $relative
    if($LASTEXITCODE -eq 1) {
      & git commit -m "Алина: опубликован результат переустановки VPN" -- $relative
      if($LASTEXITCODE -ne 0){throw "git commit failed"}
    }
    & git push origin ("HEAD:refs/heads/"+$branch)
    if($LASTEXITCODE -ne 0){throw "git push failed"}
    & git fetch origin $branch
    & git show ("origin/"+$branch+":"+$relative)|Out-Null
    if($LASTEXITCODE -ne 0){throw "remote report not found"}
  } finally { Pop-Location }
  Write-Host "GITHUB REPORT VERIFIED" -ForegroundColor Green
  Write-Host "2" -ForegroundColor Cyan
} catch {
  Write-Host ("GITHUB PUBLICATION ERROR: "+$_.Exception.Message) -ForegroundColor Red
  Write-Host ("Local report: "+$log) -ForegroundColor Yellow
  exit 1
} finally {
  if(Test-Path $worktree) {
    Set-Location $RepoRoot
    & git worktree remove --force $worktree 2>$null
  }
}
