@echo off
cd /d "%~dp0\.."


:loop
python src/zeroreferance.py
pause
cls
goto loop
