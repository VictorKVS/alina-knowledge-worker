param([Parameter(Mandatory=$true)][string]$ReportPath, [string]$DashboardUrl='http://127.0.0.1:8768')
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$report = Get-Content -LiteralPath $ReportPath -Raw -Encoding UTF8 | ConvertFrom-Json
$form = New-Object System.Windows.Forms.Form
$form.Text = if ($report.preview) { 'Алина — проверка окна отчёта' } else { 'Алина — отчёт о работе' }
$form.Size = New-Object System.Drawing.Size(560, 305)
$form.StartPosition = 'Manual'
$form.FormBorderStyle = 'FixedDialog'
$form.MaximizeBox = $false
$form.MinimizeBox = $true
$form.TopMost = $true
$form.BackColor = [System.Drawing.Color]::FromArgb(20,34,56)
$form.ForeColor = [System.Drawing.Color]::White
$area = [System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea
$form.Location = New-Object System.Drawing.Point(($area.Right-$form.Width-20),($area.Bottom-$form.Height-20))
$title = New-Object System.Windows.Forms.Label
$title.Location = New-Object System.Drawing.Point(22,18)
$title.Size = New-Object System.Drawing.Size(500,30)
$title.Font = New-Object System.Drawing.Font('Segoe UI',16,[System.Drawing.FontStyle]::Bold)
$title.Text = 'Алина · было → стало'
$body = New-Object System.Windows.Forms.Label
$body.Location = New-Object System.Drawing.Point(22,60)
$body.Size = New-Object System.Drawing.Size(505,140)
$body.Font = New-Object System.Drawing.Font('Segoe UI',11)
$hours = [math]::Floor($report.active_seconds/3600)
$minutes = [math]::Floor(($report.active_seconds%3600)/60)
$body.Text = "Разборов: $($report.before.processed) → $($report.after.processed)  (+$($report.delta.processed))`nФрагментов: $($report.before.chunks) → $($report.after.chunks)`nОшибок за период: $($report.delta.errors) · В очереди: $($report.pending)`nОбработано текущей очереди: $($report.progress)%`nВремя работы: $hours ч $minutes мин · $($report.phase)"
$button = New-Object System.Windows.Forms.Button
$button.Location = New-Object System.Drawing.Point(22,210)
$button.Size = New-Object System.Drawing.Size(220,34)
$button.Text = 'Открыть дашборд'
$button.ForeColor = [System.Drawing.Color]::Black
$button.Add_Click({ Start-Process -FilePath $DashboardUrl; $form.Close() })
$note = New-Object System.Windows.Forms.Label
$note.Location = New-Object System.Drawing.Point(260,218)
$note.Size = New-Object System.Drawing.Size(270,25)
$note.Text = 'Окно скроется через 25 секунд'
$form.Controls.AddRange(@($title,$body,$button,$note))
$timer = New-Object System.Windows.Forms.Timer
$timer.Interval=25000
$timer.Add_Tick({$timer.Stop();$form.Close()})
$eventLog = Join-Path (Split-Path -Parent $ReportPath) 'notification-events.jsonl'
$form.Add_Shown({
    @{at=(Get-Date).ToString('o');event='shown';preview=[bool]$report.preview} | ConvertTo-Json -Compress | Add-Content -LiteralPath $eventLog -Encoding UTF8
    $timer.Start()
})
$form.Add_FormClosed({
    @{at=(Get-Date).ToString('o');event='closed';preview=[bool]$report.preview} | ConvertTo-Json -Compress | Add-Content -LiteralPath $eventLog -Encoding UTF8
})
[System.Windows.Forms.Application]::Run($form)
$timer.Dispose()
$form.Dispose()
