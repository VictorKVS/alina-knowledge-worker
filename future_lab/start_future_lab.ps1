$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..
python -m unittest test_future_lab.py -v
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
python future_lab\server.py
