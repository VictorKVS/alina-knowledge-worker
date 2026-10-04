param([string[]]$Roots=@("G:\\1"),[string]$Output="alina_c0_local_inventory.json")
$ErrorActionPreference="Stop"
$Here=Split-Path -Parent $MyInvocation.MyCommand.Path
python (Join-Path $Here "local_db_probe.py") @Roots -o $Output
Write-Host "C0.2 probe complete: $Output"
