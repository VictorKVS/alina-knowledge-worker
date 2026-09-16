param([string]$Source, [string]$Output, [string]$PidFile, [string]$Format)
$ErrorActionPreference = 'Stop'
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
    [void][AlinaWindow]::GetWindowThreadProcessId([IntPtr]$word.Hwnd, [ref]$wordProcess)
    if ($previous -contains $wordProcess) { throw 'Cannot use an existing Word session' }
    $owned = $true
    [IO.File]::WriteAllText($PidFile, [string]$wordProcess)
    $word.Visible = $false
    $word.DisplayAlerts = 0
    $word.AutomationSecurity = 3
    $word.Options.UpdateLinksAtOpen = $false
    $doc = $word.Documents.Open($Source, $false, $true, $false, 'ALINA_NO_PASSWORD', '', $false, '', '', 0, '', $false, $false)
    try { [IO.File]::WriteAllText($Output, $doc.Content.Text, [Text.Encoding]::UTF8) }
    finally { $doc.Close(0) }
} finally {
    if ($owned) { $word.Quit(0) }
    [void][Runtime.InteropServices.Marshal]::FinalReleaseComObject($word)
}
