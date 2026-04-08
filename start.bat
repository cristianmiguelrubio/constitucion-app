@echo off
echo =============================================
echo   Constitucion Espanola - App para Opositores
echo =============================================

:: Comprobar Python
python --version >nul 2>&1
if errorlevel 1 (echo [ERROR] Python no encontrado & pause & exit /b 1)

:: Comprobar Node
node --version >nul 2>&1
if errorlevel 1 (echo [ERROR] Node.js no encontrado & pause & exit /b 1)

:: Instalar dependencias backend
if not exist "backend\venv" (
    echo [1/4] Creando entorno virtual Python...
    python -m venv backend\venv
)
echo [2/4] Instalando dependencias backend...
call backend\venv\Scripts\activate.bat
pip install -r backend\requirements.txt -q

:: Instalar dependencias frontend
if not exist "frontend\node_modules" (
    echo [3/4] Instalando dependencias frontend...
    cd frontend && npm install && cd ..
) else (
    echo [3/4] Dependencias frontend OK
)

echo [4/4] Arrancando servidores...

:: Obtener IP local para mostrarla
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do (
    set IP=%%a
    goto :found_ip
)
:found_ip
set IP=%IP: =%

echo.
echo  Local:   http://localhost:5173
echo  Movil:   http://%IP%:5173  (misma red WiFi)
echo.
echo  *** Para que otros te accedan por internet: ver DEPLOY.md ***
echo  Pulsa Ctrl+C en cada ventana para parar
echo =============================================

:: Backend: escucha en toda la red (0.0.0.0)
start "Backend FastAPI" cmd /k "cd backend && venv\Scripts\activate && uvicorn main:app --reload --port 8000 --host 0.0.0.0"

timeout /t 3 /nobreak >nul

:: Frontend: escucha en toda la red (--host)
start "Frontend Vite" cmd /k "cd frontend && npm run dev -- --host"

timeout /t 5 /nobreak >nul
start http://localhost:5173

pause
