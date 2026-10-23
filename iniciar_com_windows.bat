@echo off
REM Cria um atalho na pasta Inicializar para abrir o programa minimizado com o Windows.
powershell -NoProfile -Command "$s=(New-Object -ComObject WScript.Shell).CreateShortcut([Environment]::GetFolderPath('Startup')+'\Print no Controle.lnk'); $s.TargetPath='%~dp0print_controle.exe'; $s.WorkingDirectory='%~dp0'; $s.WindowStyle=7; $s.Save()"
echo Atalho criado. O programa vai abrir minimizado quando o Windows iniciar.
pause
