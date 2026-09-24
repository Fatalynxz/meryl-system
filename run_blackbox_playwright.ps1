# ==============================================================================
# MERYL SHOES ENTERPRISE SYSTEM - PLAYWRIGHT BLACK-BOX E2E TEST RUNNER
# Carlos Hilado Memorial State University - College of Computer Studies
# Covers: Chapter 4 Tables 39 to 46 (TC-AUTH-001 through TC-CUST-007)
# ==============================================================================

param(
    [int]$Evidence = 0,
    [int]$Table = 0,
    [string]$Id = "",
    [string]$Module = "",
    [switch]$All,
    [switch]$Report,
    [switch]$CaptureScreenshot
)

$FrontendDir = Join-Path $PSScriptRoot "frontend"

if ($Report) {
    Write-Host "Opening Playwright HTML Report in Browser..." -ForegroundColor Cyan
    Push-Location $FrontendDir
    & npx playwright show-report
    Pop-Location
    exit
}

if ($CaptureScreenshot) {
    Write-Host "Capturing High-Resolution PNG Screenshot..." -ForegroundColor Cyan
    Push-Location $FrontendDir
    & node e2e/capture_evidence.js
    Pop-Location
    exit
}

$NodeRunner = Join-Path $FrontendDir "e2e\run_runner.js"

$PassThruArgs = @()
if ($Table -gt 0) { $PassThruArgs += @("-Table", $Table.ToString()) }
if ($Evidence -gt 0) { $PassThruArgs += @("-Evidence", $Evidence.ToString()) }
if ($Id) { $PassThruArgs += @("-Id", $Id) }
if ($All) { $PassThruArgs += @("-All") }

& node $NodeRunner $PassThruArgs
