$ErrorActionPreference = 'Stop'
$checkout = Join-Path $PSScriptRoot ('remote-checkout-' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
$log = Join-Path $PSScriptRoot 'commands.txt'
Start-Transcript -LiteralPath $log -Force
try {
    function Invoke-GitEvidence {
        param([string[]]$GitArgs)
        Write-Host ('PS> git ' + ($GitArgs -join ' '))
        # Windows PowerShell treats native stderr progress as an ErrorRecord.
        $ErrorActionPreference = 'Continue'
        & git @GitArgs 2>&1 | ForEach-Object { Write-Host "$_" }
        if ($LASTEXITCODE -ne 0) { throw "git failed: $LASTEXITCODE" }
    }
    Invoke-GitEvidence -GitArgs @('clone', '--branch', 'main', 'https://github.com/duly-208129/mission2.git', $checkout)
    Invoke-GitEvidence -GitArgs @('-C', $checkout, 'pull', '--ff-only', 'origin', 'main')
    Invoke-GitEvidence -GitArgs @('-C', $checkout, 'branch', '-a')
    Invoke-GitEvidence -GitArgs @('-C', $checkout, 'log', '--all', '--oneline', '--decorate', '--graph')
    Invoke-GitEvidence -GitArgs @('-C', $checkout, 'rev-list', '--count', 'origin/master')
    Invoke-GitEvidence -GitArgs @('-C', $checkout, 'rev-list', '--count', 'origin/main')
    Write-Host 'PS> git log --all --merges --oneline'
    $merges = & git -C $checkout log --all --merges --oneline
    if ($LASTEXITCODE -ne 0) { throw 'merge log failed' }
    if ($merges) { $merges | ForEach-Object { Write-Host $_ } }
    else { Write-Host '(no merge commits)' }
} finally {
    Stop-Transcript
}
