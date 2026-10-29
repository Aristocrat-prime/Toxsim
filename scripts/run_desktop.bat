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
set "PYTHONPATH=%CD%\src;%PYTHONPATH%"
python -m toxsim
if errorlevel 1 (
  echo.
  echo Toxsim did not start. Confirm Python 3.11/3.12 and Tkinter are installed.
  pause
  exit /b 1
)
endlocal
