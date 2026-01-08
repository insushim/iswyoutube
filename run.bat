@echo off
chcp 65001 > nul
REM AI Knowledge YouTube Video Generator - Windows Runner
REM Usage: run.bat generate --topic "Your Topic" --category history

setlocal enabledelayedexpansion

REM Check if venv exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo [WARNING] 가상환경이 없습니다. setup.bat를 먼저 실행하세요.
)

REM Set Python path
set PYTHONPATH=%~dp0

REM Run the generator
if "%1"=="" (
    echo.
    echo ============================================
    echo   AI Knowledge YouTube Generator V2.0
    echo ============================================
    echo.
    echo 사용법:
    echo   run.bat generate --topic "주제" --category 카테고리
    echo   run.bat series --topic "주제" --episodes 10
    echo   run.bat suggest --category science --count 10
    echo.
    echo 예시:
    echo   run.bat generate --topic "로마 제국의 멸망" --category history
    echo   run.bat generate --topic "블랙홀의 비밀" --category science --style kurzgesagt
    echo.
    echo 도움말:
    echo   run.bat --help
    echo.
    python -m src.main --help
) else (
    python -m src.main %*
)

endlocal
