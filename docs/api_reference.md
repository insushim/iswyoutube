# API 레퍼런스

## VideoGenerator

메인 비디오 생성 클래스입니다.

### 초기화

```python
from src.main import VideoGenerator

generator = VideoGenerator(config_path="config/settings.yaml")
```

### 메서드

#### generate_video

단일 비디오를 생성합니다.

```python
async def generate_video(
    self,
    topic: str,
    category: VideoCategory = VideoCategory.SCIENCE,
    style: VideoStyle = VideoStyle.KURZGESAGT,
    language: Language = Language.KOREAN
) -> VideoProject
```

**매개변수:**
- `topic`: 비디오 주제
- `category`: 비디오 카테고리
- `style`: 비디오 스타일
- `language`: 출력 언어

**반환값:** `VideoProject` 객체

**예시:**
```python
project = await generator.generate_video(
    topic="양자역학의 기초",
    category=VideoCategory.SCIENCE,
    style=VideoStyle.KURZGESAGT
)
```

#### generate_series

시리즈 비디오를 생성합니다.

```python
async def generate_series(
    self,
    topic: str,
    episode_count: int = 5,
    category: VideoCategory = VideoCategory.SCIENCE,
    style: VideoStyle = VideoStyle.KURZGESAGT
) -> SeriesProject
```

#### suggest_topics

주제를 추천받습니다.

```python
async def suggest_topics(
    self,
    category: str,
    count: int = 10
) -> List[str]
```

## 데이터 클래스

### VideoProject

```python
@dataclass
class VideoProject:
    id: str
    topic: str
    category: VideoCategory
    style: VideoStyle
    language: Language
    status: ProjectStatus = ProjectStatus.CREATED
    created_at: datetime = field(default_factory=datetime.now)

    # 생성된 데이터
    research_data: Optional[ResearchData] = None
    script_data: Optional[ScriptData] = None
    audio_data: Optional[AudioData] = None
    visual_data: Optional[VisualData] = None
    video_path: Optional[str] = None
    thumbnail_path: Optional[str] = None
```

### SeriesProject

```python
@dataclass
class SeriesProject:
    id: str
    title: str
    topic: str
    category: VideoCategory
    style: VideoStyle
    language: Language
    episode_count: int
    episodes: List[VideoProject] = field(default_factory=list)
```

## Enum 타입

### VideoCategory

```python
class VideoCategory(Enum):
    SCIENCE = "science"
    TECHNOLOGY = "technology"
    HISTORY = "history"
    PHILOSOPHY = "philosophy"
    PSYCHOLOGY = "psychology"
    ECONOMICS = "economics"
    NATURE = "nature"
    SPACE = "space"
    HEALTH = "health"
    SOCIETY = "society"
```

### VideoStyle

```python
class VideoStyle(Enum):
    KURZGESAGT = "kurzgesagt"
    VERITASIUM = "veritasium"
    VSAUCE = "vsauce"
    BLUE1BROWN = "3blue1brown"
    KNOWLEDGE_PIRATE = "knowledge_pirate"
    CUSTOM = "custom"
```

### Language

```python
class Language(Enum):
    KOREAN = "ko"
    ENGLISH = "en"
    JAPANESE = "ja"
    CHINESE = "zh"
    SPANISH = "es"
```

## 모듈별 API

### Research Module

```python
from src.research import TopicGenerator, TrendAnalyzer, FactChecker

# 주제 생성
topic_gen = TopicGenerator(config)
topics = await topic_gen.generate("science", count=10)

# 트렌드 분석
analyzer = TrendAnalyzer(config)
trends = await analyzer.analyze("AI")

# 팩트 체크
checker = FactChecker(config)
result = await checker.check(["claim1", "claim2"])
```

### Script Module

```python
from src.script import ScriptGenerator, HookCreator

# 스크립트 생성
script_gen = ScriptGenerator(config)
script = await script_gen.generate(research_data, style="kurzgesagt")

# 후크 생성
hook = HookCreator(config)
intro = await hook.create("흥미로운 주제")
```

### Audio Module

```python
from src.audio import TTSEngine, AudioMixer

# TTS 생성
tts = TTSEngine(config)
audio_path = await tts.synthesize("안녕하세요", voice_id="voice1")

# 오디오 믹싱
mixer = AudioMixer(config)
final = await mixer.mix(voice=audio_path, bgm=bgm_path)
```

### Visual Module

```python
from src.visual import ImageGenerator, ChartGenerator

# 이미지 생성
img_gen = ImageGenerator(config)
image = await img_gen.generate(prompt="우주 배경", output_path="output.png")

# 차트 생성
chart_gen = ChartGenerator(config)
chart = await chart_gen.generate(
    chart_type="bar",
    data={"labels": ["A", "B"], "values": [10, 20]}
)
```

### Video Module

```python
from src.video import VideoComposer, SubtitleGenerator

# 비디오 합성
composer = VideoComposer(config)
video = await composer.compose(
    scenes=scenes,
    audio=audio_path,
    output_path="output.mp4"
)

# 자막 생성
subtitle = SubtitleGenerator(config)
srt = await subtitle.generate(segments, output_path="subs.srt")
```

## 에러 처리

```python
from src.main import VideoGeneratorError, APIError, ConfigError

try:
    project = await generator.generate_video(topic="테스트")
except APIError as e:
    print(f"API 오류: {e}")
except ConfigError as e:
    print(f"설정 오류: {e}")
except VideoGeneratorError as e:
    print(f"생성 오류: {e}")
```
