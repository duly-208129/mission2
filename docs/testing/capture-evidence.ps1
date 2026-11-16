# Capture a dedicated window containing unedited command output, not the desktop.
Add-Type 'using System.Runtime.InteropServices; public class EvidenceDpi { [DllImport("user32.dll")] public static extern bool SetProcessDPIAware(); }'
[EvidenceDpi]::SetProcessDPIAware() | Out-Null
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing
$files = @('01-python', '02-git', '04-menu', '05-quiz', '06-restart', '07-add', '08-delete', '09-summary', '10-list', 'environment', 'git-graph')
foreach ($name in $files) {
    $path = Join-Path $PSScriptRoot ($name + '.txt')
    if (-not (Test-Path -LiteralPath $path)) { continue }
    $form = New-Object System.Windows.Forms.Form
    $form.Text = "Actual command output - $name"
    $form.Size = New-Object System.Drawing.Size(1100, 850)
    $form.StartPosition = 'CenterScreen'
    $box = New-Object System.Windows.Forms.TextBox
    $box.Multiline = $true
    $box.ReadOnly = $true
    $box.ScrollBars = 'Both'
    $box.Dock = 'Fill'
    $box.Font = New-Object System.Drawing.Font('Consolas', 11)
    $box.Text = [IO.File]::ReadAllText($path) -replace "`r?`n", "`r`n"
    $form.Controls.Add($box)
    $form.Show()
    $box.SelectionStart = 0
    $box.SelectionLength = 0
    $form.Activate()
    [System.Windows.Forms.Application]::DoEvents()
    Start-Sleep -Milliseconds 350
    $bitmap = New-Object System.Drawing.Bitmap($form.Width, $form.Height)
    $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
    $graphics.CopyFromScreen($form.Location, [System.Drawing.Point]::Empty, $form.Size)
    $bitmap.Save((Join-Path $PSScriptRoot ($name + '.png')), [System.Drawing.Imaging.ImageFormat]::Png)
    $graphics.Dispose()
    $bitmap.Dispose()
    $form.Close()
    $form.Dispose()
}
