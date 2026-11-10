@echo off
:: 1. Vai para a pasta do projeto
cd /d "%~dp0"

:: 2. Prepara a máquina virtual (cria se não existir, ou apenas ativa)
if not exist ".venv\Scripts\activate.bat" (
    echo Criando ambiente virtual e instalando dependencias...
    python -m venv .venv
    call .venv\Scripts\activate.bat
    pip install -r requirements.txt
) else (
    call .venv\Scripts\activate.bat
)

:: 3. Abre a interface gráfica silenciosamente (pythonw) em segundo plano (start)
start "" pythonw main.py

:: 4. Fecha o terminal CMD imediatamente
exit