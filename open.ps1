$ErrorActionPreference = 'Stop'
$runtime = (Join-Path $PSScriptRoot '.venv\Scripts\pythonw.exe')
Start-Process -FilePath $runtime -ArgumentList ('"{0}" --open' -f (Join-Path $PSScriptRoot 'alina.py')) -WindowStyle Hidden
