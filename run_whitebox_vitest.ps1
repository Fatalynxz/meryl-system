[CmdletBinding()]
param(
    [switch]$Watch,
    [switch]$UI
)

$frontendDir = Join-Path $PSScriptRoot "frontend"

if ($UI) {
    Set-Location $frontendDir
    npx vitest --ui
} elseif ($Watch) {
    Set-Location $frontendDir
    npx vitest
} else {
    Set-Location $frontendDir
    npx vitest run --reporter=verbose
}

