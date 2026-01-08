# 설정 가이드

## 설정 파일 구조

```
config/
├── settings.yaml      # 메인 설정
└── api_keys.env       # API 키 (비공개)
```

## settings.yaml 상세

### 채널 설정

```yaml
channel:
  name: "지식의 바다"
  language: "ko"
  target_audience: "18-35세 지식 호기심 있는 성인"

  branding:
    intro_duration: 3
    outro_duration: 5
    watermark: true
    watermark_position: "bottom_right"
```

### 비디오 설정

```yaml
video:
  default_length: 600        # 기본 10분
  min_length: 300            # 최소 5분
  max_length: 1200           # 최대 20분

  resolution: "1080p"        # 720p, 1080p, 4k
  fps: 30                    # 24, 30, 60

  subtitles:
    enabled: true
    style: "modern"          # classic, modern, minimal
    font: "NanumGothic"
    size: 48
```

### 오디오 설정

```yaml
audio:
  tts:
    provider: "elevenlabs"   # elevenlabs, openai, google
    voice_id: "your_voice_id"
    speed: 1.0
    pitch: 0

  bgm:
    enabled: true
    volume: 0.15             # 배경음악 볼륨 (0-1)
    fade_in: 2
    fade_out: 3

  sfx:
    enabled: true
    volume: 0.3
```

### 비주얼 설정

```yaml
visual:
  image_generation:
    provider: "dall-e-3"     # dall-e-3, stable-diffusion
    style: "digital art"
    quality: "hd"

  animations:
    ken_burns: true
    parallax: true
    duration: 5
```

### 썸네일 설정

```yaml
thumbnail:
  resolution: [1280, 720]
  style: "bold"              # bold, minimal, dramatic

  text:
    max_words: 5
    font: "Pretendard"
    color: "#FFFFFF"
    outline: true

  ab_test:
    enabled: true
    variants: 3
```

### 다국어 설정

```yaml
localization:
  enabled: true
  target_languages:
    - "en"
    - "ja"
    - "zh"
    - "es"

  dubbing:
    enabled: false
    voice_cloning: false
```

### 업로드 설정

```yaml
upload:
  youtube:
    enabled: true
    privacy: "private"       # public, unlisted, private
    category: "Education"

  scheduling:
    enabled: true
    optimal_times:
      - "18:00"
      - "20:00"
```

### 수익화 설정

```yaml
monetization:
  ads:
    mid_roll: true
    min_interval: 180        # 중간광고 최소 간격 (초)

  affiliate:
    enabled: true
    platforms:
      - "amazon"
      - "coupang"
```

## 스타일 프리셋

### kurzgesagt

```yaml
styles:
  kurzgesagt:
    visual:
      color_palette: ["#FF6B6B", "#4ECDC4", "#45B7D1"]
      animation_style: "smooth"
      character_style: "geometric"
    audio:
      bgm_mood: "upbeat"
      pacing: "medium"
    video:
      target_length: 600
```

### veritasium

```yaml
styles:
  veritasium:
    visual:
      style: "documentary"
      b_roll: true
    audio:
      bgm_mood: "calm"
      pacing: "slow"
    video:
      target_length: 900
```

## 환경별 설정

### 개발 환경

```yaml
# config/settings.dev.yaml
debug: true
api:
  rate_limit: false
video:
  resolution: "720p"
```

### 프로덕션 환경

```yaml
# config/settings.prod.yaml
debug: false
api:
  rate_limit: true
video:
  resolution: "1080p"
```

## 설정 우선순위

1. 명령줄 인자
2. 환경 변수
3. settings.yaml
4. 기본값
