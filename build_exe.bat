@echo off
cd /d "%~dp0"
REM Gera o print_controle.exe na pasta dist\ (precisa do Python instalado).
python -m pip install --upgrade pygame-ce pyinstaller
python -m PyInstaller --onefile --name print_controle print_controle.py
copy /Y dist\print_controle.exe . >nul
echo.
echo Pronto! O programa print_controle.exe esta nesta pasta.
pause
