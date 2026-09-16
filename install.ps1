$ErrorActionPreference = 'Stop'
$desktop = [Environment]::GetFolderPath('Desktop')
$startup = [Environment]::GetFolderPath('Startup')
$shell = New-Object -ComObject WScript.Shell
$powershell = Join-Path $env:WINDIR 'System32\WindowsPowerShell\v1.0\powershell.exe'
$items = @(
    @{Dir=$desktop; Name='Алина — база знаний.lnk'; Script='open.ps1'; Description='Алина: дашборд работы с базой знаний'},
    @{Dir=$startup; Name='Алина — фоновая работа.lnk'; Script='supervisor.ps1'; Description='Алина: фоновый запуск при входе в Windows'}
)
foreach ($item in $items) {
    $link = $shell.CreateShortcut((Join-Path $item.Dir $item.Name))
    $link.TargetPath = $powershell
    $link.Arguments = '-NoProfile -WindowStyle Hidden -File "' + (Join-Path $PSScriptRoot $item.Script) + '"'
    $link.WorkingDirectory = $PSScriptRoot
    $link.IconLocation = (Join-Path $env:WINDIR 'System32\shell32.dll') + ',23'
    $link.Description = $item.Description
    $link.WindowStyle = 7
    $link.Save()
    Write-Output (Join-Path $item.Dir $item.Name)
}
Start-Process -FilePath $powershell -ArgumentList ('-NoProfile -WindowStyle Hidden -File "{0}"' -f (Join-Path $PSScriptRoot 'supervisor.ps1')) -WindowStyle Hidden
