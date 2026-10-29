@echo off
setlocal
cd /d "%~dp0.."
where python >nul 2>nul
if errorlevel 1 (
  echo Python 3.11 or 3.12 was not found on PATH.
  echo Install Python and enable the launcher, then try again.
  pause
  exit /b 1
)
python -m toxsim
if errorlevel 1 (
  echo.
  echo Toxsim did not start. Confirm Python 3.11/3.12 is installed
  echo and that the repository environment is configured.
  pause
  exit /b 1
)
endlocal
