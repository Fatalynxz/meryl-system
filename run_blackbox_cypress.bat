@echo off
setlocal
:: Ensure ELECTRON_RUN_AS_NODE is cleared so Cypress can launch Chrome/Electron
set ELECTRON_RUN_AS_NODE=
node "%~dp0frontend\cypress\run_cypress_runner.js" %*

