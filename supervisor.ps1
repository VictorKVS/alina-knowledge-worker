$ErrorActionPreference = 'Stop'
$mutex = New-Object System.Threading.Mutex($false, 'Local\FATHER_Alina_Background_v1')
if (-not $mutex.WaitOne(0)) { exit 0 }
try {
    $runtime = (Join-Path $PSScriptRoot '.venv\Scripts\pythonw.exe')
    $app = Join-Path $PSScriptRoot 'alina.py'
    while ($true) {
        $worker = Start-Process -FilePath $runtime -ArgumentList ('"{0}" --serve' -f $app) -WindowStyle Hidden -PassThru
        $worker.WaitForExit()
        if ($worker.ExitCode -eq 17) { break }
        Start-Sleep -Seconds 15
    }
} finally {
    $mutex.ReleaseMutex()
    $mutex.Dispose()
}
