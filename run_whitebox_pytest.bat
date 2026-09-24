@echo off
setlocal
set PYTHONIOENCODING=utf-8
"%~dp0.venv\Scripts\python.exe" "%~dp0whitebox_tests\run_pytest_runner.py" %*

