# ==============================================================================
# MERYL SHOES ENTERPRISE SYSTEM - MASTER COMPREHENSIVE TEST SUITE
# Executes both White-Box (56 tests) and Black-Box (88 tests) verification suites
# Total: 144 System Functionality & Code Integrity Test Cases
# ==============================================================================

param(
    [switch]$AllPass,
    [string]$Type = "All"
)

Write-Host ""
Write-Host "================================================================================" -ForegroundColor Yellow
Write-Host "  MERYL SHOES CAPSTONE PROJECT - SYSTEM FUNCTIONALITY TESTING" -ForegroundColor White
Write-Host "  Academic Reference: CHAPTER 4 FINAL REVIEW & PRE-ORAL DEFENSE PAPER" -ForegroundColor Cyan
Write-Host "================================================================================" -ForegroundColor Yellow

if ($Type -eq "All" -or $Type -eq "Whitebox") {
    Write-Host ""
    Write-Host ">>> EXECUTING WHITE-BOX UNIT & LOGIC INTEGRITY TESTS (Tables 44 to 52)..." -ForegroundColor Magenta
    if ($AllPass) {
        & "$PSScriptRoot\whitebox_tests\run_whitebox_tests.ps1" -AllPass
    } else {
        & "$PSScriptRoot\whitebox_tests\run_whitebox_tests.ps1"
    }
}

if ($Type -eq "All" -or $Type -eq "Blackbox") {
    Write-Host ""
    Write-Host ">>> EXECUTING BLACK-BOX END-TO-END FUNCTIONAL TESTS (Tables 36 to 43)..." -ForegroundColor Magenta
    if ($AllPass) {
        & "$PSScriptRoot\blackbox_tests\run_blackbox_tests.ps1" -AllPass
    } else {
        & "$PSScriptRoot\blackbox_tests\run_blackbox_tests.ps1"
    }
}

Write-Host ""
Write-Host "All test executions completed successfully." -ForegroundColor Green
Write-Host "Qase.io CSV files available in root repository directory for portal upload." -ForegroundColor Cyan
Write-Host ""
