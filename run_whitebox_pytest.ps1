[CmdletBinding()]
param(
    [Parameter(Position=0)]
    [int]$Evidence,
    [int]$Module,
    [string]$Id,
    [switch]$All,
    [switch]$Coverage
)

$pythonExe = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
$runnerScript = Join-Path $PSScriptRoot "whitebox_tests\run_pytest_runner.py"

$cliArgs = @()
if ($PSBoundParameters.ContainsKey('Evidence')) {
    $cliArgs += "-Evidence"
    $cliArgs += "$Evidence"
}
if ($PSBoundParameters.ContainsKey('Module')) {
    $cliArgs += "-Module"
    $cliArgs += "$Module"
}
if ($PSBoundParameters.ContainsKey('Id')) {
    $cliArgs += "-Id"
    $cliArgs += "$Id"
}
if ($All) {
    $cliArgs += "-All"
}
if ($Coverage) {
    $cliArgs += "-Coverage"
}

& $pythonExe $runnerScript @cliArgs

