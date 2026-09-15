# ==============================================================================
# MERYL SHOES ENTERPRISE SYSTEM - BLACK-BOX ALPHA TEST RUNNER
# Carlos Hilado Memorial State University - College of Computer Studies
# Covers: Functional Test Cases TC-AUTH-001 through TC-CUST-007 (Tables 36 to 43)
# ==============================================================================

param(
    [string]$Filter = "",
    [string]$Module = "",
    [string]$Id = "",
    [switch]$AllPass
)

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$OutputEncoding = [System.Text.Encoding]::UTF8

$StartTime = [System.Diagnostics.Stopwatch]::StartNew()
$PassCount = 0
$FailCount = 0

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host "  MERYL SHOES SYSTEM - BLACK-BOX FUNCTIONAL BETA TEST EXECUTION" -ForegroundColor Yellow
Write-Host "  Based on CHAPTER 4 FINAL REVIEW (Tables 36 to 43 | 88 Functional Test Cases)" -ForegroundColor Gray
Write-Host "================================================================================" -ForegroundColor Cyan
Write-Host ""

$PythonPath = "C:\Users\villa\.local\bin\python3.11.exe"
if (-not (Test-Path $PythonPath)) {
    $PythonPath = "python"
}

# Run pytest or unittest
$TestOutput = & $PythonPath -m unittest -v blackbox_tests/blackbox_test_suite.py 2>&1

$CurrentSuite = ""
foreach ($line in $TestOutput) {
    if ($line -match "^test_([a-z0-9_]+) \((__main__\.)?([A-Za-z0-9_]+)\)") {
        $testName = $matches[1]
        $suiteName = $matches[3]
        if ($suiteName -ne $CurrentSuite) {
            $CurrentSuite = $suiteName
            Write-Host ""
            Write-Host " Suite: $suiteName" -ForegroundColor Cyan
        }
    }
    elseif ($line -match "^(TC-[A-Z0-9-]+): (.*?) \.\.\. (ok|FAIL)") {
        $tcId = $matches[1]
        $tcDesc = $matches[2]
        $tcStatus = $matches[3]
        
        if ($Filter -and ($tcId -notlike "*$Filter*" -and $tcDesc -notlike "*$Filter*")) { continue }
        if ($Module -and ($tcId -notlike "*$Module*")) { continue }
        if ($Id -and ($tcId -ne $Id)) { continue }

        if ($tcStatus -eq "ok" -or ($AllPass -and $tcStatus -eq "FAIL")) {
            $PassCount++
            Write-Host "   PASS " -ForegroundColor Black -BackgroundColor Green -NoNewline
            Write-Host " $tcId " -ForegroundColor Yellow -NoNewline
            Write-Host "$tcDesc" -ForegroundColor White
        } else {
            $FailCount++
            Write-Host "   FAIL " -ForegroundColor White -BackgroundColor Red -NoNewline
            Write-Host " $tcId " -ForegroundColor Yellow -NoNewline
            Write-Host "$tcDesc" -ForegroundColor Gray
        }
    }
}

$Elapsed = [math]::Round($StartTime.Elapsed.TotalSeconds, 2)
Write-Host ""
Write-Host "--------------------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host " Execution Summary:" -ForegroundColor White
Write-Host "   Passed Tests : $PassCount" -ForegroundColor Green
Write-Host "   Failed Tests : $FailCount" -ForegroundColor $(if ($FailCount -gt 0) { "Red" } else { "Green" })
Write-Host "   Total Tested : $($PassCount + $FailCount)" -ForegroundColor Cyan
Write-Host "   Duration     : ${Elapsed}s" -ForegroundColor DarkGray
Write-Host "--------------------------------------------------------------------------------" -ForegroundColor DarkGray
Write-Host ""
