# 시작 가이드

## 목차
1. [시스템 요구사항](#시스템-요구사항)
2. [설치](#설치)
3. [API 키 설정](#api-키-설정)
4. [첫 번째 비디오 생성](#첫-번째-비디오-생성)
5. [문제 해결](#문제-해결)

## 시스템 요구사항

### 필수
- Python 3.10 이상
- FFmpeg (비디오 처리용)
- 8GB RAM 이상
- 10GB 이상 디스크 공간

### 선택
- CUDA 지원 GPU (이미지 생성 가속)
- Docker (컨테이너 실행 시)

## 설치

### 1. 저장소 클론

```bash
git clone https://github.com/example/ai-knowledge-youtube.git
cd ai-knowledge-youtube
```

### 2. 가상환경 생성

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate
```

### 3. 의존성 설치

```bash
pip install -r requirements.txt
```

### 4. FFmpeg 설치

**Windows:**
```bash
# Chocolatey 사용
choco install ffmpeg

# 또는 https://ffmpeg.org/download.html 에서 다운로드
```

**macOS:**
```bash
brew install ffmpeg
```

**Linux:**
```bash
sudo apt update
sudo apt install ffmpeg
```

## API 키 설정

### 1. 환경 파일 생성

```bash
cp config/api_keys.env.example config/api_keys.env
```

### 2. API 키 입력

`config/api_keys.env` 파일을 열어 필요한 API 키를 입력합니다:

```env
# 필수 API 키
ANTHROPIC_API_KEY=your_anthropic_key_here
OPENAI_API_KEY=your_openai_key_here
ELEVENLABS_API_KEY=your_elevenlabs_key_here

# YouTube 업로드용 (선택)
YOUTUBE_CLIENT_ID=your_client_id
YOUTUBE_CLIENT_SECRET=your_client_secret
```

### API 키 발급 방법

1. **Anthropic (Claude)**: https://console.anthropic.com/
2. **OpenAI (DALL-E 3)**: https://platform.openai.com/
3. **ElevenLabs (TTS)**: https://elevenlabs.io/

## 첫 번째 비디오 생성

### 기본 생성

```bash
python -m src.main generate --topic "양자역학의 기초"
```

### 스타일 지정

```bash
python -m src.main generate --topic "블랙홀의 비밀" --style kurzgesagt
```

### 사용 가능한 스타일
- `kurzgesagt`: 미니멀 플랫 디자인
- `veritasium`: 다큐멘터리 스타일
- `3blue1brown`: 수학 시각화
- `vsauce`: 탐구형
- `knowledge_pirate`: 빠른 편집

### 시리즈 생성

```bash
python -m src.main series --topic "우주의 미스터리" --episodes 5
```

## 문제 해결

### FFmpeg를 찾을 수 없음

```
Error: FFmpeg not found
```

해결: FFmpeg가 PATH에 추가되었는지 확인하세요.

### API 키 오류

```
Error: Invalid API key
```

해결: `config/api_keys.env` 파일의 API 키가 올바른지 확인하세요.

### 메모리 부족

```
Error: Out of memory
```

해결: `config/settings.yaml`에서 해상도를 낮추거나 배치 크기를 줄이세요.

## 다음 단계

- [설정 가이드](configuration.md)
- [스타일 커스터마이징](styles.md)
- [API 레퍼런스](api_reference.md)
