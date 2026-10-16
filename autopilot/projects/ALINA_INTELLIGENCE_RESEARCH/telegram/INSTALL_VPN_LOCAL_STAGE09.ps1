# ============================================================
# FATHER / VPN ZOO - STAGE 09
# SIGNATURE VERIFICATION, SEQUENTIAL OFFICIAL INSTALLERS, GITHUB REPORT
# ASCII-only source for Windows PowerShell 5.1
# ============================================================
param([string]$RepoRoot="G:\1\alina-knowledge-worker")
$ErrorActionPreference="Stop"
$branch="feature/alina-k3-k10-autopilot"
$reportRel="autopilot/projects/ALINA_INTELLIGENCE_RESEARCH/telegram/evidence/VPN_INSTALL_STAGE09.md"
$reportLocal=Join-Path $env:TEMP "FATHER_VPN_INSTALL_STAGE09.md"
$items=@(
 @{Name="AmneziaVPN";File="$env:USERPROFILE\Downloads\AmneziaVPN_5.0.3.0_windows_x64.exe";Publisher="Privacy Technologies"},
 @{Name="Proton VPN";File="$env:USERPROFILE\Downloads\ProtonVPN_v5.1.8_x64.exe";Publisher="Proton AG"},
 @{Name="Windscribe";File="$env:USERPROFILE\Downloads\Windscribe_2.24.13_amd64.exe";Publisher="Windscribe Limited"}
)
$results=New-Object System.Collections.Generic.List[string]
$results.Add("# FATHER - VPN installation / stage 09")
$results.Add("- Timestamp UTC: "+[DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ"))
$results.Add("- Mode: interactive vendor installers; server profiles are not deleted by this script")
$results.Add("")
$failed=$false
try {
  foreach($item in $items) {
    if(-not (Test-Path -LiteralPath $item.File)){throw ("Missing installer: "+$item.Name)}
    $sig=Get-AuthenticodeSignature -LiteralPath $item.File
    if($sig.Status -ne "Valid" -or -not $sig.SignerCertificate -or $sig.SignerCertificate.Subject -notlike ("*"+$item.Publisher+"*")) {throw ("Signature/publisher not verified: "+$item.Name)}
    $results.Add("- "+$item.Name+": signature and publisher verified")
  }
  Write-Host "All three installer signatures verified." -ForegroundColor Green
  Write-Host "Make sure the AmneziaVPN server/profile backup is safely stored." -ForegroundColor Yellow
  $ok=Read-Host "Type INSTALL to run the three interactive installers"
  if($ok -ne "INSTALL") {throw "Cancelled. No installer launched"}
  foreach($item in $items){
    Write-Host ("Opening vendor installer: "+$item.Name) -ForegroundColor Cyan
    Write-Host "Complete the vendor installer, then return to PowerShell." -ForegroundColor Yellow
    $p=Start-Process -FilePath $item.File -Wait -PassThru
    $results.Add("- "+$item.Name+": installer returned code "+$p.ExitCode+" (installation to be verified separately)")
    if($p.ExitCode -ne 0) {
      $failed=$true
      Write-Host ("Installer reported code "+$p.ExitCode+"; continuing to next client.") -ForegroundColor Yellow
    }
  }
  $results.Add("- Overall installer process: "+$(if($failed){"NEEDS_REVIEW"}else{"COMPLETED_NO_ERROR_REPORTED"}))
  $results.Add("- Actual client installation, VPN tunnel and Telegram access: NOT VERIFIED")
} catch {
  $failed=$true
  $results.Add("- Overall installer process: ERROR")
  $results.Add("- Reason: "+($_.Exception.Message -replace '[\r\n]+',' '))
  Write-Host ("Stage 09: "+$_.Exception.Message) -ForegroundColor Red
} finally {
  [IO.File]::WriteAllLines($reportLocal,[string[]]$results,(New-Object Text.UTF8Encoding($false)))
  Write-Host ("Local report: "+$reportLocal)
}
$wt=Join-Path $env:TEMP ("FATHER_VPN_INSTALL_"+[guid]::NewGuid().ToString("N"))
$worktreeCreated=$false
try {
  Set-Location $RepoRoot
  & git fetch origin $branch
  if($LASTEXITCODE -ne 0){throw "Cannot fetch GitHub branch"}
  & git worktree add --detach $wt ("origin/"+$branch)
  if($LASTEXITCODE -ne 0){throw "Cannot create safe temporary worktree"}
  $worktreeCreated=$true
  $dest=Join-Path $wt ($reportRel -replace '/', [IO.Path]::DirectorySeparatorChar)
  New-Item -ItemType Directory -Force -Path (Split-Path $dest)|Out-Null
  Copy-Item -LiteralPath $reportLocal -Destination $dest
  Push-Location $wt
  try {
    & git add -- $reportRel
    if($LASTEXITCODE -ne 0){throw "Cannot stage report"}
    & git diff --cached --quiet -- $reportRel
    if($LASTEXITCODE -eq 1) {
      & git commit -m "Алина: сохранён отчёт об установке трёх VPN-клиентов" -- $reportRel
      if($LASTEXITCODE -ne 0){throw "Cannot commit report"}
    }
    & git push origin ("HEAD:refs/heads/"+$branch)
    if($LASTEXITCODE -ne 0){throw "Cannot publish report"}
    & git fetch origin $branch
    if($LASTEXITCODE -ne 0){throw "Cannot refresh remote branch"}
    & git show ("origin/"+$branch+":"+$reportRel)|Out-Null
    if($LASTEXITCODE -ne 0){throw "Report not visible on remote"}
  } finally {Pop-Location}
  Write-Host "GITHUB REPORT VERIFIED" -ForegroundColor Green
  if($failed){Write-Host "Installation needs review; see report." -ForegroundColor Yellow}else{Write-Host "Installation steps finished; next verify clients and Telegram." -ForegroundColor Green}
  Write-Host "2" -ForegroundColor Cyan
} catch {
  Write-Host ("GitHub publication error: "+$_.Exception.Message) -ForegroundColor Red
  Write-Host ("Report remains local: "+$reportLocal) -ForegroundColor Yellow
  exit 1
} finally {
  if($worktreeCreated) {
    Set-Location $RepoRoot
    & git worktree remove --force $wt 2>$null
  }
}
