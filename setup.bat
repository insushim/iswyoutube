@echo off
chcp 65001 > nul
echo ============================================
echo   AI Knowledge YouTube Generator Setup
echo ============================================
echo.

REM Check Python
python --version > nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python이 설치되어 있지 않습니다.
    echo Python 3.11 이상을 설치해주세요: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/5] 가상환경 생성 중...
if not exist "venv" (
    python -m venv venv
    echo     가상환경 생성 완료
) else (
    echo     기존 가상환경 사용
)

echo.
echo [2/5] 가상환경 활성화...
call venv\Scripts\activate.bat

echo.
echo [3/5] pip 업그레이드...
python -m pip install --upgrade pip --quiet

echo.
echo [4/5] 필수 패키지 설치 중... (최소 버전)
pip install -r requirements-minimal.txt --quiet

echo.
echo [5/5] 디렉토리 구조 생성...
if not exist "output\audio" mkdir output\audio
if not exist "output\images" mkdir output\images
if not exist "output\videos" mkdir output\videos
if not exist "output\shorts" mkdir output\shorts
if not exist "output\thumbnails" mkdir output\thumbnails
if not exist "data\projects" mkdir data\projects
if not exist "data\cache" mkdir data\cache
if not exist "logs" mkdir logs
if not exist "backups" mkdir backups

echo.
echo ============================================
echo   설치 완료!
echo ============================================
echo.
echo 다음 단계:
echo 1. config\api_keys.env 파일에 API 키를 입력하세요
echo    - ANTHROPIC_API_KEY (필수)
echo    - OPENAI_API_KEY (필수)
echo    - ELEVENLABS_API_KEY (TTS용)
echo.
echo 2. 테스트 실행:
echo    run.bat
echo.
echo 3. 영상 생성:
echo    run.bat generate --topic "로마 제국의 멸망" --category history
echo.
pause
