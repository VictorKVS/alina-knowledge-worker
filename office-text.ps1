param([string]$Source, [string]$Output, [string]$PidFile, [string]$Format)
$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding
if ($Format -eq 'rtf') {
    Add-Type -AssemblyName System.Windows.Forms
    $box = New-Object System.Windows.Forms.RichTextBox
    try {
        $box.LoadFile($Source, [System.Windows.Forms.RichTextBoxStreamType]::RichText)
        [IO.File]::WriteAllText($Output, $box.Text, [Text.Encoding]::UTF8)
    } finally { $box.Dispose() }
    exit
}
Add-Type @'
using System;
using System.Runtime.InteropServices;
public class AlinaWindow { [DllImport("user32.dll")] public static extern uint GetWindowThreadProcessId(IntPtr h, out uint p); }
'@
$previous = @(Get-Process WINWORD -ErrorAction SilentlyContinue | ForEach-Object { $_.Id })
$word = New-Object -ComObject Word.Application
$owned = $false
try {
    [uint32]$wordProcess = 0
    if ($null -ne $word.Hwnd) {
        [void][AlinaWindow]::GetWindowThreadProcessId([IntPtr]$word.Hwnd, [ref]$wordProcess)
    } else {
        $created = @(Get-Process WINWORD -ErrorAction SilentlyContinue | Where-Object { $previous -notcontains $_.Id })
        if ($created.Count -ne 1) { throw 'Cannot identify isolated Word process' }
        $wordProcess = $created[0].Id
    }
    if ($previous -contains $wordProcess) { throw 'Cannot use an existing Word session' }
    $owned = $true
    [IO.File]::WriteAllText($PidFile, [string]$wordProcess)
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $word.AutomationSecurity = 3
    $word.Options.UpdateLinksAtOpen = $false
    $no = $false
    $yes = $true
    $password = 'ALINA_NO_PASSWORD'
    $zero = 0
    $doc = $word.Documents.Open([ref]$Source, [ref]$no, [ref]$yes, [ref]$no, [ref]$password)
    try { [IO.File]::WriteAllText($Output, $doc.Content.Text, [Text.Encoding]::UTF8) }
    finally { $doc.Close([ref]$zero) }
} finally {
    if ($owned) { $zero = 0; $word.Quit([ref]$zero) }
    [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($word)
}
