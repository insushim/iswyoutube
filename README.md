# AI Knowledge YouTube Video Generator V2.0

완전 자동화 유튜브 지식 콘텐츠 제작 시스템

## 개요

500개 이상의 성공적인 지식 유튜브 채널 분석을 기반으로 개발된 AI 기반 비디오 생성 시스템입니다.

### 주요 기능

- **AI 기반 주제 생성**: 트렌드 분석, 키워드 연구, 경쟁자 분석
- **자동 스크립트 작성**: 스타일별 템플릿, 후크 생성, 유머 주입
- **고품질 TTS**: ElevenLabs, OpenAI TTS 지원
- **AI 이미지 생성**: DALL-E 3, Stable Diffusion 통합
- **자동 비디오 제작**: 장면 구성, 애니메이션, 자막
- **YouTube Shorts 자동 생성**: 세로 형식 자동 변환
- **다국어 지원**: 한국어, 영어, 일본어, 중국어, 스페인어
- **썸네일 A/B 테스트**: CTR 예측 및 최적화
- **자동 업로드**: YouTube, TikTok, Instagram 지원
- **커뮤니티 관리**: 댓글 분석 및 자동 응답
- **수익화 최적화**: 광고 배치, 중간 광고 최적화

## 빠른 시작

### 1. 설치

```bash
# 저장소 클론
git clone https://github.com/example/ai-knowledge-youtube.git
cd ai-knowledge-youtube

# 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 의존성 설치
pip install -r requirements.txt

# 또는 개발 모드로 설치
pip install -e ".[dev]"
```

### 2. API 키 설정

```bash
# API 키 파일 생성
cp config/api_keys.env.example config/api_keys.env

# 필수 API 키 설정
# - ANTHROPIC_API_KEY: Claude AI (스크립트 생성)
# - OPENAI_API_KEY: DALL-E 3 (이미지 생성)
# - ELEVENLABS_API_KEY: TTS (음성 합성)
# - YOUTUBE_* : YouTube API (업로드)
```

### 3. 비디오 생성

```bash
# 단일 비디오 생성
python -m src.main generate --topic "양자역학의 기초" --style kurzgesagt

# 시리즈 생성
python -m src.main series --topic "우주의 미스터리" --episodes 5

# 주제 추천
python -m src.main suggest --category science --count 10
```

## 프로젝트 구조

```
ai-knowledge-youtube/
├── config/                 # 설정 파일
│   ├── settings.yaml      # 메인 설정
│   └── api_keys.env       # API 키 (gitignore)
├── src/                    # 소스 코드
│   ├── main.py            # 메인 진입점
│   ├── research/          # 리서치 모듈
│   ├── script/            # 스크립트 생성
│   ├── audio/             # 오디오/TTS
│   ├── visual/            # 이미지/비주얼
│   ├── video/             # 비디오 합성
│   ├── shorts/            # Shorts 변환
│   ├── thumbnail/         # 썸네일 생성
│   ├── localization/      # 다국어 지원
│   ├── upload/            # 업로드 관리
│   ├── community/         # 커뮤니티 관리
│   ├── analytics/         # 분석
│   ├── monetization/      # 수익화
│   ├── quality/           # 품질 관리
│   ├── series/            # 시리즈 관리
│   ├── repurpose/         # 콘텐츠 재활용
│   └── backup/            # 백업 관리
├── assets/                 # 에셋 파일
├── data/                   # 데이터 파일
├── output/                 # 출력 파일
├── tests/                  # 테스트
└── docs/                   # 문서
```

## 비디오 생성 파이프라인

1. **주제 생성** - AI가 트렌드 분석 후 주제 제안
2. **리서치** - 팩트 체킹, 소스 수집
3. **스크립트** - 스타일별 스크립트 자동 생성
4. **오디오** - TTS 음성 합성 + BGM + 효과음
5. **비주얼** - AI 이미지 생성 + 인포그래픽
6. **비디오** - 장면 합성 + 자막 + 전환 효과
7. **Shorts** - 세로 형식 자동 변환
8. **썸네일** - A/B 테스트용 썸네일 생성
9. **다국어** - 번역 + 더빙
10. **품질 검사** - 저작권, 팩트 체크
11. **업로드** - SEO 최적화 후 업로드
12. **커뮤니티** - 댓글 모니터링
13. **분석** - 성과 분석 및 리포트
14. **수익화** - 광고 최적화

## 스타일 프리셋

| 스타일 | 설명 | 길이 |
|--------|------|------|
| `kurzgesagt` | 미니멀 플랫 디자인, 부드러운 애니메이션 | 8-12분 |
| `knowledge_pirate` | 실사 + 그래픽, 빠른 편집 | 10-15분 |
| `veritasium` | 실험/인터뷰 스타일 | 15-20분 |
| `3blue1brown` | 수학 시각화, 애니메이션 | 15-25분 |
| `vsauce` | 탐구형, 다양한 비주얼 | 12-20분 |

## API 사용량 및 비용

| 서비스 | 용도 | 예상 비용/비디오 |
|--------|------|------------------|
| Claude | 스크립트 생성 | ~$0.50 |
| DALL-E 3 | 이미지 생성 | ~$2.00 |
| ElevenLabs | TTS | ~$1.00 |
| **총계** | | **~$3.50** |

## 라이선스

MIT License

## 기여

이슈 및 PR 환영합니다!
