[CmdletBinding()]
param(
    [Parameter(Position=0)]
    [int]$Table,
    [string]$Id,
    [switch]$All,
    [switch]$Open
)

$env:ELECTRON_RUN_AS_NODE = $null
$runnerPath = Join-Path $PSScriptRoot "frontend\cypress\run_cypress_runner.js"

$cliArgs = @()
if ($PSBoundParameters.ContainsKey('Table')) {
    $cliArgs += "-Table"
    $cliArgs += "$Table"
}
if ($PSBoundParameters.ContainsKey('Id')) {
    $cliArgs += "-Id"
    $cliArgs += "$Id"
}
if ($All) {
    $cliArgs += "-All"
}
if ($Open) {
    $cliArgs += "-Open"
}

& node $runnerPath @cliArgs

