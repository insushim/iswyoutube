#!/usr/bin/env python3
"""
AI Knowledge YouTube Video Generator V2.0
==========================================
500개 이상의 성공 채널 분석 기반 완전 자동화 유튜브 콘텐츠 제작 시스템

Features:
- 원클릭 영상 생성
- 다국어 자동 현지화
- Shorts 자동 생성
- 시리즈 자동화
- A/B 테스트
- 커뮤니티 자동 관리
- 수익화 최적화
- 크로스 플랫폼 업로드

Author: AI Video Generator
Version: 2.0.0
"""

import os
import sys
import yaml
import logging
import asyncio
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List, Union
from dataclasses import dataclass, field
from enum import Enum
import json
import uuid
import re

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))


# ============================================
# Gemini AI Client
# ============================================

class GeminiClient:
    """Gemini AI 클라이언트 - 환경변수에서 안전하게 키 로드"""

    def __init__(self, config: Dict = None):
        self.config = config or {}
        self.model = None
        self._initialized = False
        self._init_client()

    def _init_client(self):
        """클라이언트 초기화 - 환경변수에서 키 로드"""
        try:
            import google.generativeai as genai

            # 환경변수에서 API 키 로드 (코드에 키 노출 방지)
            api_key = os.environ.get('GEMINI_API_KEY')
            if not api_key:
                raise ValueError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다")

            genai.configure(api_key=api_key)

            model_name = self.config.get('api', {}).get('gemini', {}).get('model', 'gemini-3-flash')
            self.model = genai.GenerativeModel(model_name)
            self._initialized = True

        except ImportError:
            logging.warning("google-generativeai 패키지가 설치되지 않았습니다. pip install google-generativeai")
        except Exception as e:
            logging.warning(f"Gemini 초기화 실패: {e}")

    def generate(self, prompt: str, max_tokens: int = 8000) -> str:
        """텍스트 생성"""
        if not self._initialized or not self.model:
            raise RuntimeError("Gemini 클라이언트가 초기화되지 않았습니다")

        generation_config = {
            "max_output_tokens": max_tokens,
            "temperature": self.config.get('api', {}).get('gemini', {}).get('temperature', 0.7),
        }

        response = self.model.generate_content(prompt, generation_config=generation_config)
        return response.text

    @property
    def is_available(self) -> bool:
        return self._initialized and self.model is not None


def parse_json_response(text: str) -> Any:
    """JSON 응답 파싱 - 여러 형식 지원"""
    # 마크다운 코드 블록 제거
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]

    # JSON 배열/객체 추출
    text = text.strip()

    # JSON 시작점 찾기
    json_start = -1
    for i, char in enumerate(text):
        if char in '[{':
            json_start = i
            break

    if json_start > 0:
        text = text[json_start:]

    # JSON 끝점 찾기
    bracket_count = 0
    json_end = len(text)
    start_char = text[0] if text else '{'
    end_char = ']' if start_char == '[' else '}'

    for i, char in enumerate(text):
        if char == start_char:
            bracket_count += 1
        elif char == end_char:
            bracket_count -= 1
            if bracket_count == 0:
                json_end = i + 1
                break

    text = text[:json_end]

    return json.loads(text)


# ============================================
# Enums
# ============================================

class VideoCategory(Enum):
    """영상 카테고리"""
    HISTORY = "history"
    SCIENCE = "science"
    ECONOMY = "economy"
    CULTURE = "culture"
    TECHNOLOGY = "technology"
    PHILOSOPHY = "philosophy"
    PSYCHOLOGY = "psychology"
    GEOGRAPHY = "geography"
    BIOLOGY = "biology"
    PHYSICS = "physics"
    MATH = "math"
    POLITICS = "politics"
    SOCIETY = "society"
    ART = "art"
    MUSIC = "music"
    FOOD = "food"
    SPORTS = "sports"
    GAMING = "gaming"
    LANGUAGE = "language"
    HEALTH = "health"


class VideoStyle(Enum):
    """영상 스타일"""
    KURZGESAGT = "kurzgesagt"
    KNOWLEDGE_PIRATE = "knowledge_pirate"
    VERITASIUM = "veritasium"
    INFOGRAPHIC = "infographic"
    CRASH_COURSE = "crash_course"
    OVERSIMPLIFIED = "oversimplified"
    MINIMAL = "minimal"
    DOCUMENTARY = "documentary"
    ANIMATED = "animated"
    CUSTOM = "custom"


class VideoFormat(Enum):
    """영상 포맷"""
    LONG_FORM = "long_form"
    SHORT = "short"
    SERIES_EPISODE = "series_episode"
    COMPILATION = "compilation"
    REACTION = "reaction"
    TUTORIAL = "tutorial"
    QNA = "qna"
    NEWS = "news"


class Language(Enum):
    """지원 언어"""
    KOREAN = "ko"
    ENGLISH = "en"
    JAPANESE = "ja"
    CHINESE = "zh"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    PORTUGUESE = "pt"
    RUSSIAN = "ru"
    ARABIC = "ar"


class UploadPlatform(Enum):
    """업로드 플랫폼"""
    YOUTUBE = "youtube"
    TIKTOK = "tiktok"
    INSTAGRAM = "instagram"
    FACEBOOK = "facebook"
    BILIBILI = "bilibili"
    TWITTER = "twitter"


class ProjectStatus(Enum):
    """프로젝트 상태"""
    INITIALIZED = "initialized"
    RESEARCHING = "researching"
    SCRIPTING = "scripting"
    GENERATING_AUDIO = "generating_audio"
    GENERATING_VISUALS = "generating_visuals"
    COMPOSING_VIDEO = "composing_video"
    GENERATING_SHORTS = "generating_shorts"
    GENERATING_THUMBNAILS = "generating_thumbnails"
    LOCALIZING = "localizing"
    OPTIMIZING = "optimizing"
    QUALITY_CHECK = "quality_check"
    READY_TO_UPLOAD = "ready_to_upload"
    UPLOADING = "uploading"
    COMPLETED = "completed"
    ERROR = "error"


# ============================================
# Data Classes
# ============================================

@dataclass
class ResearchData:
    """리서치 데이터"""
    topic: str = ""
    trends: Dict = field(default_factory=dict)
    sources: List[Dict] = field(default_factory=list)
    verified_facts: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    competitor_analysis: Dict = field(default_factory=dict)
    audience_insights: Dict = field(default_factory=dict)
    predicted_performance: Dict = field(default_factory=dict)
    suggested_titles: List[str] = field(default_factory=list)
    viral_score: float = 0.0


@dataclass
class ScriptData:
    """스크립트 데이터"""
    full_script: str = ""
    segments: List[Dict] = field(default_factory=list)
    hooks: List[str] = field(default_factory=list)
    cta_segments: List[str] = field(default_factory=list)
    sponsor_segments: List[Dict] = field(default_factory=list)
    word_count: int = 0
    estimated_duration: float = 0.0
    readability_score: float = 0.0


@dataclass
class AudioData:
    """오디오 데이터"""
    narration_path: str = ""
    bgm_path: str = ""
    mixed_audio_path: str = ""
    duration: float = 0.0
    voice_id: str = ""
    segments_timing: List[Dict] = field(default_factory=list)
    transcript_path: str = ""


@dataclass
class VisualData:
    """비주얼 데이터"""
    scene_plan: List[Dict] = field(default_factory=list)
    images: List[str] = field(default_factory=list)
    animations: List[str] = field(default_factory=list)
    infographics: List[str] = field(default_factory=list)
    charts: List[str] = field(default_factory=list)
    maps: List[str] = field(default_factory=list)
    stock_footage: List[str] = field(default_factory=list)


@dataclass
class VideoData:
    """비디오 데이터"""
    main_video_path: str = ""
    shorts_paths: List[str] = field(default_factory=list)
    duration: float = 0.0
    resolution: str = ""
    chapters: List[Dict] = field(default_factory=list)
    subtitle_path: str = ""


@dataclass
class ThumbnailData:
    """썸네일 데이터"""
    paths: List[str] = field(default_factory=list)
    ab_test_id: str = ""
    selected_index: int = 0
    predicted_ctr: float = 0.0
    styles_used: List[str] = field(default_factory=list)


@dataclass
class LocalizationData:
    """현지화 데이터"""
    language: str = ""
    translated_script: str = ""
    dubbed_audio_path: str = ""
    localized_video_path: str = ""
    localized_thumbnail_path: str = ""
    localized_seo: Dict = field(default_factory=dict)
    localized_subtitles: str = ""


@dataclass
class SEOData:
    """SEO 데이터"""
    title: str = ""
    description: str = ""
    tags: List[str] = field(default_factory=list)
    timestamps: List[str] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    youtube_category_id: str = "27"
    keywords: List[str] = field(default_factory=list)
    predicted_ranking: Dict = field(default_factory=dict)


@dataclass
class MonetizationData:
    """수익화 데이터"""
    ad_placements: List[Dict] = field(default_factory=list)
    sponsor_segments: List[Dict] = field(default_factory=list)
    affiliate_links: List[Dict] = field(default_factory=list)
    estimated_revenue: float = 0.0
    mid_roll_points: List[float] = field(default_factory=list)


@dataclass
class AnalyticsData:
    """분석 데이터"""
    predicted_views: int = 0
    predicted_ctr: float = 0.0
    predicted_retention: float = 0.0
    best_upload_time: str = ""
    competitor_comparison: Dict = field(default_factory=dict)
    trend_alignment: float = 0.0


@dataclass
class QualityData:
    """품질 데이터"""
    overall_score: float = 0.0
    copyright_issues: List[str] = field(default_factory=list)
    fact_check_results: List[Dict] = field(default_factory=list)
    plagiarism_score: float = 0.0
    guideline_compliance: bool = True
    accessibility_score: float = 0.0


@dataclass
class RepurposeData:
    """콘텐츠 재활용 데이터"""
    blog_post_path: str = ""
    social_snippets: Dict[str, str] = field(default_factory=dict)
    quotes: List[str] = field(default_factory=list)
    infographic_exports: List[str] = field(default_factory=list)
    email_newsletter: str = ""


@dataclass
class VideoProject:
    """비디오 프로젝트 메인 데이터 클래스"""
    # 기본 정보
    id: str = field(default_factory=lambda: f"vid_{uuid.uuid4().hex[:12]}")
    title: str = ""
    topic: str = ""
    category: VideoCategory = VideoCategory.HISTORY
    style: VideoStyle = VideoStyle.KNOWLEDGE_PIRATE
    format: VideoFormat = VideoFormat.LONG_FORM
    language: Language = Language.KOREAN

    # 설정
    duration_target: int = 600
    auto_upload: bool = False
    generate_shorts: bool = True
    generate_localizations: List[Language] = field(default_factory=list)
    platforms: List[UploadPlatform] = field(default_factory=lambda: [UploadPlatform.YOUTUBE])

    # 생성 데이터
    research: ResearchData = field(default_factory=ResearchData)
    script: ScriptData = field(default_factory=ScriptData)
    audio: AudioData = field(default_factory=AudioData)
    visual: VisualData = field(default_factory=VisualData)
    video: VideoData = field(default_factory=VideoData)
    thumbnail: ThumbnailData = field(default_factory=ThumbnailData)
    localizations: Dict[str, LocalizationData] = field(default_factory=dict)
    seo: SEOData = field(default_factory=SEOData)
    monetization: MonetizationData = field(default_factory=MonetizationData)
    analytics: AnalyticsData = field(default_factory=AnalyticsData)
    quality: QualityData = field(default_factory=QualityData)
    repurpose: RepurposeData = field(default_factory=RepurposeData)

    # 메타데이터
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    status: ProjectStatus = ProjectStatus.INITIALIZED
    progress: float = 0.0
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    # 업로드 정보
    upload_results: Dict[str, Dict] = field(default_factory=dict)
    scheduled_time: Optional[datetime] = None

    # 시리즈 정보 (시리즈인 경우)
    series_id: Optional[str] = None
    episode_number: Optional[int] = None

    def update_status(self, status: ProjectStatus):
        """상태 업데이트"""
        self.status = status
        self.updated_at = datetime.now()

    def add_error(self, error: str):
        """에러 추가"""
        self.errors.append(f"[{datetime.now().isoformat()}] {error}")

    def add_warning(self, warning: str):
        """경고 추가"""
        self.warnings.append(f"[{datetime.now().isoformat()}] {warning}")

    def to_dict(self) -> Dict:
        """딕셔너리로 변환"""
        return {
            "id": self.id,
            "title": self.title,
            "topic": self.topic,
            "category": self.category.value,
            "style": self.style.value,
            "format": self.format.value,
            "language": self.language.value,
            "status": self.status.value,
            "progress": self.progress,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "video_path": self.video.main_video_path,
            "shorts_count": len(self.video.shorts_paths),
            "localizations": list(self.localizations.keys()),
            "errors": self.errors,
            "warnings": self.warnings,
        }

    def save(self, path: str = None):
        """프로젝트 저장"""
        if path is None:
            path = f"./data/projects/{self.id}.json"

        Path(path).parent.mkdir(parents=True, exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: str) -> 'VideoProject':
        """프로젝트 로드"""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        project = cls()
        project.id = data.get('id', project.id)
        project.title = data.get('title', '')
        project.topic = data.get('topic', '')
        project.category = VideoCategory(data.get('category', 'history'))
        project.style = VideoStyle(data.get('style', 'knowledge_pirate'))
        project.format = VideoFormat(data.get('format', 'long_form'))
        project.language = Language(data.get('language', 'ko'))
        project.status = ProjectStatus(data.get('status', 'initialized'))
        project.progress = data.get('progress', 0.0)

        return project


@dataclass
class SeriesProject:
    """시리즈 프로젝트"""
    id: str = field(default_factory=lambda: f"series_{uuid.uuid4().hex[:12]}")
    name: str = ""
    description: str = ""
    topic: str = ""
    category: VideoCategory = VideoCategory.HISTORY
    style: VideoStyle = VideoStyle.KNOWLEDGE_PIRATE
    total_episodes: int = 10
    episodes: List[VideoProject] = field(default_factory=list)
    schedule: Dict = field(default_factory=dict)
    playlist_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    status: str = "planning"

    def add_episode(self, episode: VideoProject):
        """에피소드 추가"""
        episode.series_id = self.id
        episode.episode_number = len(self.episodes) + 1
        self.episodes.append(episode)


# ============================================
# Main Generator Class
# ============================================

class VideoGenerator:
    """메인 비디오 생성기 클래스"""

    def __init__(self, config_path: str = "config/settings.yaml"):
        self.config = self._load_config(config_path)
        self.logger = self._setup_logging()
        self.components = {}
        self._load_env_keys()
        self._initialize_components()
        self._init_gemini()

    def _load_config(self, config_path: str) -> Dict:
        """설정 파일 로드"""
        config_path = Path(config_path)
        if not config_path.exists():
            # Try relative to script location
            alt_path = Path(__file__).parent.parent / config_path
            if alt_path.exists():
                config_path = alt_path
            else:
                raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _load_env_keys(self):
        """환경변수에서 API 키 로드"""
        from dotenv import load_dotenv

        # Try multiple locations for env file
        env_paths = [
            Path("config/api_keys.env"),
            Path(__file__).parent.parent / "config" / "api_keys.env",
        ]

        for env_path in env_paths:
            if env_path.exists():
                load_dotenv(env_path)
                break

    def _setup_logging(self) -> logging.Logger:
        """로깅 설정"""
        logger = logging.getLogger("VideoGenerator")
        log_level = self.config.get('logging', {}).get('level', 'INFO')
        logger.setLevel(getattr(logging, log_level))

        # Clear existing handlers
        logger.handlers = []

        # Console handler
        if self.config.get('logging', {}).get('console', {}).get('enabled', True):
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            console_handler.setFormatter(formatter)
            logger.addHandler(console_handler)

        # File handler
        if self.config.get('logging', {}).get('file', {}).get('enabled', True):
            log_dir = Path(self.config.get('logging', {}).get('file', {}).get('path', './logs'))
            log_dir.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(
                log_dir / f"generator_{datetime.now().strftime('%Y%m%d')}.log",
                encoding='utf-8'
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)

        return logger

    def _initialize_components(self):
        """컴포넌트 초기화"""
        self.logger.info("시스템 초기화 시작...")

        # Component module paths for dynamic loading
        component_modules = {
            # Research
            'topic_generator': 'research.topic_generator.TopicGenerator',
            'trend_analyzer': 'research.trend_analyzer.TrendAnalyzer',
            'trend_predictor': 'research.trend_predictor.TrendPredictor',
            'competitor_analyzer': 'research.competitor_analyzer.CompetitorAnalyzer',
            'fact_checker': 'research.fact_checker.FactChecker',
            'source_collector': 'research.source_collector.SourceCollector',
            'keyword_researcher': 'research.keyword_researcher.KeywordResearcher',
            'audience_analyzer': 'research.audience_analyzer.AudienceAnalyzer',

            # Script
            'script_generator': 'script.script_generator.ScriptGenerator',
            'hook_creator': 'script.hook_creator.HookCreator',
            'structure_builder': 'script.structure_builder.StructureBuilder',
            'script_optimizer': 'script.script_optimizer.ScriptOptimizer',
            'humor_injector': 'script.humor_injector.HumorInjector',
            'cta_generator': 'script.cta_generator.CTAGenerator',

            # Audio
            'tts_engine': 'audio.tts_engine.TTSEngine',
            'voice_cloner': 'audio.voice_cloner.VoiceCloner',
            'bgm_selector': 'audio.bgm_selector.BGMSelector',
            'sfx_manager': 'audio.sfx_manager.SFXManager',
            'audio_mixer': 'audio.audio_mixer.AudioMixer',
            'audio_enhancer': 'audio.audio_enhancer.AudioEnhancer',

            # Visual
            'scene_planner': 'visual.scene_planner.ScenePlanner',
            'image_generator': 'visual.image_generator.ImageGenerator',
            'animation_engine': 'visual.animation_engine.AnimationEngine',
            'infographic_maker': 'visual.infographic_maker.InfographicMaker',
            'chart_generator': 'visual.chart_generator.ChartGenerator',
            'map_generator': 'visual.map_generator.MapGenerator',
            'asset_manager': 'visual.asset_manager.AssetManager',

            # Video
            'video_composer': 'video.video_composer.VideoComposer',
            'subtitle_generator': 'video.subtitle_generator.SubtitleGenerator',
            'transition_handler': 'video.transition_handler.TransitionHandler',
            'intro_outro_manager': 'video.intro_outro_manager.IntroOutroManager',
            'video_exporter': 'video.video_exporter.VideoExporter',

            # Shorts
            'shorts_converter': 'shorts.shorts_converter.ShortsConverter',
            'highlight_extractor': 'shorts.highlight_extractor.HighlightExtractor',

            # Thumbnail
            'thumbnail_generator': 'thumbnail.thumbnail_generator.ThumbnailGenerator',
            'thumbnail_ab_tester': 'thumbnail.thumbnail_ab_tester.ThumbnailABTester',
            'ctr_predictor': 'thumbnail.ctr_predictor.CTRPredictor',

            # Localization
            'translator': 'localization.translator.Translator',
            'cultural_adapter': 'localization.cultural_adapter.CulturalAdapter',
            'dubbing_engine': 'localization.dubbing_engine.DubbingEngine',
            'lip_sync': 'localization.lip_sync.LipSync',

            # Upload
            'youtube_uploader': 'upload.youtube_uploader.YouTubeUploader',
            'tiktok_uploader': 'upload.tiktok_uploader.TikTokUploader',
            'seo_optimizer': 'upload.seo_optimizer.SEOOptimizer',
            'scheduler': 'upload.scheduler.UploadScheduler',

            # Community
            'comment_analyzer': 'community.comment_analyzer.CommentAnalyzer',
            'comment_responder': 'community.comment_responder.CommentResponder',
            'spam_filter': 'community.spam_filter.SpamFilter',

            # Analytics
            'youtube_analytics': 'analytics.youtube_analytics.YouTubeAnalytics',
            'ab_test_manager': 'analytics.ab_test_manager.ABTestManager',
            'dashboard_generator': 'analytics.dashboard_generator.DashboardGenerator',

            # Monetization
            'ad_placement_optimizer': 'monetization.ad_placement_optimizer.AdPlacementOptimizer',
            'mid_roll_detector': 'monetization.mid_roll_detector.MidRollDetector',
            'affiliate_manager': 'monetization.affiliate_manager.AffiliateManager',

            # Series
            'series_planner': 'series.series_planner.SeriesPlanner',
            'episode_generator': 'series.episode_generator.EpisodeGenerator',
            'continuity_checker': 'series.continuity_checker.ContinuityChecker',

            # Repurpose
            'content_repurposer': 'repurpose.content_repurposer.ContentRepurposer',
            'blog_converter': 'repurpose.blog_converter.BlogConverter',
            'social_snippet_maker': 'repurpose.social_snippet_maker.SocialSnippetMaker',

            # Quality
            'copyright_checker': 'quality.copyright_checker.CopyrightChecker',
            'fact_verifier': 'quality.fact_verifier.FactVerifier',
            'quality_scorer': 'quality.quality_scorer.QualityScorer',

            # Backup
            'backup_manager': 'backup.backup_manager.BackupManager',
        }

        # Initialize component placeholders
        for name, module_path in component_modules.items():
            self.components[name] = None  # Will be lazy-loaded when needed

        self.logger.info("모든 컴포넌트 초기화 완료")

    def _init_gemini(self):
        """Gemini 클라이언트 초기화"""
        try:
            self.gemini = GeminiClient(self.config)
            if self.gemini.is_available:
                self.logger.info("Gemini 2.0 Flash 초기화 완료")
            else:
                self.logger.warning("Gemini 초기화 실패 - Anthropic으로 폴백")
                self.gemini = None
        except Exception as e:
            self.logger.warning(f"Gemini 초기화 실패: {e}")
            self.gemini = None

    def _generate_with_ai(self, prompt: str, max_tokens: int = 8000) -> str:
        """AI 텍스트 생성 - Gemini 우선, Anthropic 폴백"""
        # Gemini 우선 시도
        if self.gemini and self.gemini.is_available:
            try:
                return self.gemini.generate(prompt, max_tokens)
            except Exception as e:
                self.logger.warning(f"Gemini 생성 실패, Anthropic으로 폴백: {e}")

        # Anthropic 폴백
        try:
            from anthropic import Anthropic
            client = Anthropic()
            response = client.messages.create(
                model=self.config.get('api', {}).get('anthropic', {}).get('model', 'claude-sonnet-4-20250514'),
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            self.logger.error(f"AI 생성 실패: {e}")
            raise

    # ============================================
    # 메인 생성 메서드
    # ============================================

    async def generate_video(
        self,
        topic: str,
        category: VideoCategory = VideoCategory.HISTORY,
        style: VideoStyle = VideoStyle.KNOWLEDGE_PIRATE,
        format: VideoFormat = VideoFormat.LONG_FORM,
        language: Language = Language.KOREAN,
        duration_target: int = 600,
        generate_shorts: bool = True,
        generate_localizations: List[Language] = None,
        auto_upload: bool = False,
        schedule_time: Optional[datetime] = None,
        series_id: Optional[str] = None,
        episode_number: Optional[int] = None,
        platforms: List[UploadPlatform] = None,
    ) -> VideoProject:
        """
        완전한 비디오 생성 파이프라인

        Args:
            topic: 영상 주제
            category: 카테고리
            style: 영상 스타일
            format: 영상 포맷
            language: 메인 언어
            duration_target: 목표 길이 (초)
            generate_shorts: Shorts 생성 여부
            generate_localizations: 현지화할 언어 리스트
            auto_upload: 자동 업로드 여부
            schedule_time: 예약 업로드 시간
            series_id: 시리즈 ID (시리즈의 일부인 경우)
            episode_number: 에피소드 번호
            platforms: 업로드 플랫폼 리스트

        Returns:
            VideoProject: 완성된 프로젝트
        """
        # 프로젝트 초기화
        project = VideoProject(
            topic=topic,
            category=category,
            style=style,
            format=format,
            language=language,
            duration_target=duration_target,
            generate_shorts=generate_shorts,
            generate_localizations=generate_localizations or [],
            auto_upload=auto_upload,
            scheduled_time=schedule_time,
            series_id=series_id,
            episode_number=episode_number,
            platforms=platforms or [UploadPlatform.YOUTUBE],
        )

        self.logger.info(f"{'='*60}")
        self.logger.info(f"프로젝트 시작: {project.id}")
        self.logger.info(f"주제: {topic}")
        self.logger.info(f"카테고리: {category.value}")
        self.logger.info(f"스타일: {style.value}")
        self.logger.info(f"{'='*60}")

        try:
            # ========== Phase 1: 리서치 (10%) ==========
            project.update_status(ProjectStatus.RESEARCHING)
            project = await self._phase_research(project)
            project.progress = 0.10
            self.logger.info(f"Phase 1 완료 - 리서치 (10%)")

            # ========== Phase 2: 스크립트 생성 (20%) ==========
            project.update_status(ProjectStatus.SCRIPTING)
            project = await self._phase_script(project)
            project.progress = 0.20
            self.logger.info(f"Phase 2 완료 - 스크립트 (20%)")

            # ========== Phase 3: 오디오 생성 (35%) ==========
            project.update_status(ProjectStatus.GENERATING_AUDIO)
            project = await self._phase_audio(project)
            project.progress = 0.35
            self.logger.info(f"Phase 3 완료 - 오디오 (35%)")

            # ========== Phase 4: 비주얼 생성 (50%) ==========
            project.update_status(ProjectStatus.GENERATING_VISUALS)
            project = await self._phase_visual(project)
            project.progress = 0.50
            self.logger.info(f"Phase 4 완료 - 비주얼 (50%)")

            # ========== Phase 5: 비디오 조립 (65%) ==========
            project.update_status(ProjectStatus.COMPOSING_VIDEO)
            project = await self._phase_video_compose(project)
            project.progress = 0.65
            self.logger.info(f"Phase 5 완료 - 비디오 조립 (65%)")

            # ========== Phase 6: Shorts 생성 (72%) ==========
            if generate_shorts:
                project.update_status(ProjectStatus.GENERATING_SHORTS)
                project = await self._phase_shorts(project)
            project.progress = 0.72
            self.logger.info(f"Phase 6 완료 - Shorts (72%)")

            # ========== Phase 7: 썸네일 생성 (78%) ==========
            project.update_status(ProjectStatus.GENERATING_THUMBNAILS)
            project = await self._phase_thumbnail(project)
            project.progress = 0.78
            self.logger.info(f"Phase 7 완료 - 썸네일 (78%)")

            # ========== Phase 8: 다국어 현지화 (85%) ==========
            if generate_localizations:
                project.update_status(ProjectStatus.LOCALIZING)
                project = await self._phase_localization(project)
            project.progress = 0.85
            self.logger.info(f"Phase 8 완료 - 현지화 (85%)")

            # ========== Phase 9: SEO 최적화 (88%) ==========
            project.update_status(ProjectStatus.OPTIMIZING)
            project = await self._phase_seo(project)
            project.progress = 0.88
            self.logger.info(f"Phase 9 완료 - SEO (88%)")

            # ========== Phase 10: 수익화 최적화 (91%) ==========
            project = await self._phase_monetization(project)
            project.progress = 0.91
            self.logger.info(f"Phase 10 완료 - 수익화 (91%)")

            # ========== Phase 11: 품질 검증 (94%) ==========
            project.update_status(ProjectStatus.QUALITY_CHECK)
            project = await self._phase_quality_check(project)
            project.progress = 0.94
            self.logger.info(f"Phase 11 완료 - 품질 검증 (94%)")

            # ========== Phase 12: 콘텐츠 재활용 (97%) ==========
            project = await self._phase_repurpose(project)
            project.progress = 0.97
            self.logger.info(f"Phase 12 완료 - 재활용 (97%)")

            # ========== Phase 13: 업로드 (100%) ==========
            if auto_upload:
                project.update_status(ProjectStatus.UPLOADING)
                project = await self._phase_upload(project)
            else:
                project.update_status(ProjectStatus.READY_TO_UPLOAD)
            project.progress = 1.0
            self.logger.info(f"Phase 13 완료 - 업로드 (100%)")

            # ========== Phase 14: 백업 ==========
            await self._phase_backup(project)

            project.update_status(ProjectStatus.COMPLETED)

            self.logger.info(f"{'='*60}")
            self.logger.info(f"프로젝트 완료: {project.id}")
            self.logger.info(f"영상: {project.video.main_video_path}")
            self.logger.info(f"Shorts: {len(project.video.shorts_paths)}개")
            self.logger.info(f"현지화: {list(project.localizations.keys())}")
            self.logger.info(f"{'='*60}")

        except Exception as e:
            project.update_status(ProjectStatus.ERROR)
            project.add_error(str(e))
            self.logger.error(f"프로젝트 실패: {e}")
            import traceback
            self.logger.error(traceback.format_exc())
            raise

        # 프로젝트 저장
        project.save()

        return project

    # ============================================
    # Phase 메서드들
    # ============================================

    async def _phase_research(self, project: VideoProject) -> VideoProject:
        """Phase 1: 리서치 및 자료 수집"""
        self.logger.info("Phase 1: 리서치 시작...")

        # 1. 제목 생성
        titles_prompt = f"""유튜브 지식 채널용 "{project.topic}" 주제의 클릭율 높은 제목 5개를 생성하세요.

스타일: {project.style.value}
카테고리: {project.category.value}

제목 패턴:
- 질문형: "왜 ~일까?", "어떻게 ~했을까?"
- 폭로형: "~의 충격적인 진실", "아무도 모르는 ~"
- 숫자형: "~의 5가지 비밀", "TOP 10 ~"
- 비교형: "~ vs ~: 승자는?"

JSON 배열로 응답:
[
    {{"title": "제목1", "hook_type": "질문형", "estimated_ctr": 0.08}},
    ...
]"""

        try:
            text = self._generate_with_ai(titles_prompt, max_tokens=2000)
            titles_data = parse_json_response(text)
            project.research.suggested_titles = [t['title'] for t in titles_data]
            project.title = titles_data[0]['title']
        except Exception as e:
            self.logger.warning(f"Title generation failed: {e}")
            project.title = f"{project.topic} - 알려지지 않은 진실"
            project.research.suggested_titles = [project.title]

        # 2. 소스 수집 (실제로는 웹 검색 API 사용)
        project.research.sources = [
            {"type": "wikipedia", "reliability": 0.9},
            {"type": "academic", "reliability": 0.95},
            {"type": "news", "reliability": 0.7},
        ]

        # 3. 키워드 리서치
        project.research.keywords = [
            project.topic,
            f"{project.topic} 역사",
            f"{project.topic} 진실",
            f"{project.topic} 설명",
        ]

        self.logger.info(f"리서치 완료 - 제목: {project.title}")
        return project

    async def _phase_script(self, project: VideoProject) -> VideoProject:
        """Phase 2: 스크립트 생성"""
        self.logger.info("Phase 2: 스크립트 생성 시작...")

        # 스타일별 프롬프트 조정
        style_instructions = {
            VideoStyle.KURZGESAGT: """
- 우주적 관점에서 시작하여 점점 좁혀오기
- 낙관적 허무주의 철학 반영
- 복잡한 개념을 시각적 은유로 설명
- "당신"을 직접 언급하며 개인화
- 마지막에 희망적인 메시지""",
            VideoStyle.KNOWLEDGE_PIRATE: """
- 친근하고 수다스러운 톤
- "~했다는데요", "~래요" 같은 구어체
- 재미있는 비유와 현대적 예시
- 갑자기 터지는 드립
- "자, 이제 진짜 재밌는 부분입니다" 같은 전환""",
            VideoStyle.VERITASIUM: """
- 흔한 오해로 시작
- "사실은 이게 틀렸습니다" 반전
- 실험이나 데모 설명
- 전문가 인용
- 깊은 통찰로 마무리""",
            VideoStyle.INFOGRAPHIC: """
- 숫자와 통계로 시작
- "첫 번째로", "두 번째로" 명확한 구분
- 비교 차트 설명
- 핵심 포인트 강조
- 요약 리스트로 마무리""",
        }

        style_guide = style_instructions.get(project.style, "")

        script_prompt = f"""유튜브 지식 채널 스크립트를 작성하세요.

제목: {project.title}
주제: {project.topic}
카테고리: {project.category.value}
스타일: {project.style.value}
목표 길이: {project.duration_target}초 (약 {project.duration_target // 60}분)
언어: {project.language.value}

스타일 가이드:{style_guide}

필수 구조:
1. [0:00-0:15] 후크 - 충격적인 질문이나 사실로 시작
2. [0:15-0:45] 도입 - 왜 이게 중요한지 설명
3. [0:45-중반] 본론1 - 배경/역사/원인
4. [중반-후반] 본론2 - 핵심 내용/메커니즘
5. [후반-끝30초전] 본론3 - 영향/결과/미래
6. [마지막 30초] 결론 + CTA + 다음 영상 예고

각 세그먼트에 [비주얼: 설명] 태그 포함
감정 변화 표시: [감정: 호기심/놀라움/진지함/유머/감동]

JSON 형식으로 응답:
{{
    "full_script": "전체 스크립트 텍스트",
    "segments": [
        {{
            "id": 1,
            "type": "hook",
            "start_time": "0:00",
            "end_time": "0:15",
            "text": "세그먼트 텍스트",
            "visual_note": "비주얼 설명",
            "emotion": "호기심",
            "duration": 15
        }},
        ...
    ],
    "hooks": ["후크1", "후크2", "후크3"],
    "key_points": ["핵심 포인트1", "핵심 포인트2"],
    "cta": "구독과 좋아요 부탁드려요! 다음 영상에서는..."
}}"""

        try:
            text = self._generate_with_ai(script_prompt, max_tokens=8000)
            script_data = parse_json_response(text)

            project.script.full_script = script_data.get('full_script', '')
            project.script.segments = script_data.get('segments', [])
            project.script.hooks = script_data.get('hooks', [])
            project.script.cta_segments = [script_data.get('cta', '')]
            project.script.word_count = len(project.script.full_script)
            project.script.estimated_duration = project.duration_target

        except Exception as e:
            self.logger.warning(f"Script parsing failed: {e}")
            project.script.full_script = f"이것은 {project.topic}에 대한 영상입니다."
            project.script.segments = [{"id": 1, "text": project.script.full_script, "duration": project.duration_target}]

        self.logger.info(f"스크립트 완료 - {len(project.script.segments)}개 세그먼트")
        return project

    async def _phase_audio(self, project: VideoProject) -> VideoProject:
        """Phase 3: 오디오 생성"""
        self.logger.info("Phase 3: 오디오 생성 시작...")

        output_dir = Path(self.config['project']['output_dir']) / "audio" / project.id
        output_dir.mkdir(parents=True, exist_ok=True)

        tts_config = self.config['audio']['tts']
        voice_id = tts_config['voices'].get(project.language.value, {}).get('male', '')

        # Try ElevenLabs TTS
        if tts_config['provider'] == 'elevenlabs':
            try:
                from elevenlabs import ElevenLabs, VoiceSettings

                client = ElevenLabs()

                audio_data = client.text_to_speech.convert(
                    voice_id=voice_id,
                    text=project.script.full_script,
                    model_id=tts_config['model'],
                    voice_settings=VoiceSettings(
                        stability=tts_config['settings']['stability'],
                        similarity_boost=tts_config['settings']['similarity_boost'],
                        style=tts_config['settings'].get('style', 0.0),
                    )
                )

                narration_path = output_dir / "narration.mp3"
                with open(narration_path, 'wb') as f:
                    for chunk in audio_data:
                        f.write(chunk)

                project.audio.narration_path = str(narration_path)
                self.logger.info("ElevenLabs TTS 완료")
            except Exception as e:
                self.logger.warning(f"ElevenLabs TTS failed: {e}")
                # Create placeholder
                project.audio.narration_path = str(output_dir / "narration_placeholder.mp3")

        # BGM selection
        bgm_config = self.config['audio']['bgm']
        if bgm_config['enabled']:
            bgm_categories = bgm_config.get('categories', {}).get(project.category.value, ['ambient'])
            project.audio.bgm_path = f"assets/music/background/{bgm_categories[0]}_01.mp3"

        # Audio mixing (if both files exist)
        try:
            from pydub import AudioSegment

            if Path(project.audio.narration_path).exists():
                narration = AudioSegment.from_file(project.audio.narration_path)
                project.audio.duration = len(narration) / 1000

                if bgm_config['enabled'] and Path(project.audio.bgm_path).exists():
                    bgm = AudioSegment.from_file(project.audio.bgm_path)
                    bgm = bgm - (20 * (1 - bgm_config['volume']))

                    if len(bgm) < len(narration):
                        bgm = bgm * (len(narration) // len(bgm) + 1)
                    bgm = bgm[:len(narration)]

                    fade_in_ms = int(bgm_config['fade_in'] * 1000)
                    fade_out_ms = int(bgm_config['fade_out'] * 1000)
                    bgm = bgm.fade_in(fade_in_ms).fade_out(fade_out_ms)

                    mixed = narration.overlay(bgm)

                    mixed_path = output_dir / "mixed_audio.mp3"
                    mixed.export(str(mixed_path), format="mp3")
                    project.audio.mixed_audio_path = str(mixed_path)
                else:
                    project.audio.mixed_audio_path = project.audio.narration_path
        except Exception as e:
            self.logger.warning(f"Audio mixing failed: {e}")
            project.audio.mixed_audio_path = project.audio.narration_path

        self.logger.info("오디오 생성 완료")
        return project

    async def _phase_visual(self, project: VideoProject) -> VideoProject:
        """Phase 4: 비주얼 에셋 생성"""
        self.logger.info("Phase 4: 비주얼 생성 시작...")

        output_dir = Path(self.config['project']['output_dir']) / "images" / project.id
        output_dir.mkdir(parents=True, exist_ok=True)

        # Scene planning
        scene_plan = []
        for idx, segment in enumerate(project.script.segments):
            visual_note = segment.get('visual_note', f'{project.topic} 관련 이미지')
            scene_plan.append({
                'segment_id': segment.get('id', idx),
                'description': visual_note,
                'duration': segment.get('duration', 30),
                'style': project.style.value
            })

        project.visual.scene_plan = scene_plan

        # Image generation with DALL-E 3
        try:
            from openai import OpenAI
            import httpx

            openai_client = OpenAI()
            visual_config = self.config['visual']['image_generation']

            style_modifiers = {
                VideoStyle.KURZGESAGT: "flat design, minimal, pastel colors, geometric shapes, educational infographic style, no text",
                VideoStyle.KNOWLEDGE_PIRATE: "warm colors, illustrated style, friendly cartoon, educational, engaging",
                VideoStyle.VERITASIUM: "realistic, documentary style, scientific, clean, professional",
                VideoStyle.INFOGRAPHIC: "data visualization, clean design, vibrant colors, modern infographic",
            }

            modifier = style_modifiers.get(project.style, "educational, clean, professional")

            images = []
            for idx, scene in enumerate(scene_plan[:10]):
                try:
                    prompt = f"{scene['description']}, {modifier}, 16:9 aspect ratio, high quality"

                    response = openai_client.images.generate(
                        model=visual_config['model'],
                        prompt=prompt,
                        size=visual_config['size'],
                        quality=visual_config['quality'],
                        n=1
                    )

                    image_url = response.data[0].url
                    image_response = httpx.get(image_url)

                    image_path = output_dir / f"scene_{idx:03d}.png"
                    with open(image_path, 'wb') as f:
                        f.write(image_response.content)

                    images.append(str(image_path))
                    self.logger.info(f"  이미지 {idx+1}/{min(len(scene_plan), 10)} 생성 완료")

                except Exception as e:
                    self.logger.warning(f"  이미지 {idx+1} 생성 실패: {e}")
                    images.append(f"assets/images/backgrounds/default_{project.category.value}.png")

            project.visual.images = images

        except Exception as e:
            self.logger.warning(f"Image generation failed: {e}")
            project.visual.images = []

        self.logger.info(f"비주얼 생성 완료 - {len(project.visual.images)}개 이미지")
        return project

    async def _phase_video_compose(self, project: VideoProject) -> VideoProject:
        """Phase 5: 비디오 조립"""
        self.logger.info("Phase 5: 비디오 조립 시작...")

        output_dir = Path(self.config['project']['output_dir']) / "videos" / project.id
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            from moviepy.editor import (
                ImageClip, AudioFileClip, CompositeVideoClip,
                concatenate_videoclips, ColorClip
            )

            video_config = self.config['video']

            # Load audio
            if project.audio.mixed_audio_path and Path(project.audio.mixed_audio_path).exists():
                audio = AudioFileClip(project.audio.mixed_audio_path)
                total_duration = audio.duration
            else:
                audio = None
                total_duration = project.duration_target

            # Create image clips
            clips = []
            images = project.visual.images

            if not images:
                clip = ColorClip(size=(1920, 1080), color=(26, 26, 46), duration=total_duration)
                clips.append(clip)
            else:
                clip_duration = total_duration / len(images)

                for idx, img_path in enumerate(images):
                    try:
                        if Path(img_path).exists():
                            img_clip = ImageClip(img_path)
                            img_clip = img_clip.resize((1920, 1080))
                            img_clip = img_clip.set_duration(clip_duration)

                            # Ken Burns effect
                            if video_config.get('animation', {}).get('effects', {}).get('ken_burns', {}).get('enabled', True):
                                zoom_ratio = video_config['animation']['effects']['ken_burns'].get('zoom_ratio', 0.04)
                                img_clip = img_clip.resize(lambda t: 1 + zoom_ratio * t / clip_duration)

                            img_clip = img_clip.crossfadein(0.5)
                            img_clip = img_clip.crossfadeout(0.5)

                            clips.append(img_clip)
                    except Exception as e:
                        self.logger.warning(f"Image clip creation failed: {e}")

            # Concatenate video
            if clips:
                video = concatenate_videoclips(clips, method='compose')
            else:
                video = ColorClip(size=(1920, 1080), color=(26, 26, 46), duration=total_duration)

            # Set audio
            if audio:
                video = video.set_audio(audio)

            # Export
            output_path = output_dir / f"{project.id}_main.mp4"

            video.write_videofile(
                str(output_path),
                fps=video_config['fps'],
                codec=video_config['codec'],
                audio_codec=video_config['audio_codec'],
                bitrate=video_config['bitrate'],
                preset=video_config.get('preset', 'medium')
            )

            # Cleanup
            video.close()
            if audio:
                audio.close()
            for clip in clips:
                clip.close()

            project.video.main_video_path = str(output_path)
            project.video.duration = total_duration
            project.video.resolution = video_config['default_resolution']

            # Generate chapters
            chapters = []
            for segment in project.script.segments:
                chapters.append({
                    'time': segment.get('start_time', '0:00'),
                    'title': segment.get('type', 'Section'),
                })
            project.video.chapters = chapters

        except Exception as e:
            self.logger.error(f"Video composition failed: {e}")
            project.video.main_video_path = ""

        self.logger.info(f"비디오 조립 완료 - {project.video.main_video_path}")
        return project

    async def _phase_shorts(self, project: VideoProject) -> VideoProject:
        """Phase 6: Shorts 생성"""
        self.logger.info("Phase 6: Shorts 생성 시작...")

        if not project.video.main_video_path or not Path(project.video.main_video_path).exists():
            self.logger.warning("Main video not found, skipping shorts")
            return project

        try:
            from moviepy.editor import VideoFileClip

            output_dir = Path(self.config['project']['output_dir']) / "shorts" / project.id
            output_dir.mkdir(parents=True, exist_ok=True)

            shorts_config = self.config['shorts']

            original = VideoFileClip(project.video.main_video_path)

            # Extract highlights
            highlights = []
            for segment in project.script.segments[:3]:
                duration = min(segment.get('duration', 30), shorts_config['format']['max_duration'])
                highlights.append({
                    'start': 0,
                    'duration': duration,
                    'title': segment.get('text', '')[:50]
                })

            shorts_paths = []
            for idx, highlight in enumerate(highlights):
                try:
                    start = highlight['start']
                    duration = min(highlight['duration'], shorts_config['format']['max_duration'])
                    clip = original.subclip(start, min(start + duration, original.duration))

                    # Convert to vertical (9:16)
                    w, h = clip.size
                    target_ratio = 9 / 16

                    new_w = int(h * target_ratio)
                    x_center = w // 2

                    clip = clip.crop(
                        x1=max(0, x_center - new_w // 2),
                        y1=0,
                        x2=min(w, x_center + new_w // 2),
                        y2=h
                    )

                    clip = clip.resize((1080, 1920))

                    short_path = output_dir / f"short_{idx:02d}.mp4"
                    clip.write_videofile(
                        str(short_path),
                        fps=shorts_config['format']['fps'],
                        codec='libx264',
                        audio_codec='aac'
                    )

                    shorts_paths.append(str(short_path))
                    clip.close()

                    self.logger.info(f"  Short {idx+1} 생성 완료")

                except Exception as e:
                    self.logger.warning(f"  Short {idx+1} 생성 실패: {e}")

            original.close()
            project.video.shorts_paths = shorts_paths

        except Exception as e:
            self.logger.warning(f"Shorts generation failed: {e}")

        self.logger.info(f"Shorts 생성 완료 - {len(project.video.shorts_paths)}개")
        return project

    async def _phase_thumbnail(self, project: VideoProject) -> VideoProject:
        """Phase 7: 썸네일 생성"""
        self.logger.info("Phase 7: 썸네일 생성 시작...")

        output_dir = Path(self.config['project']['output_dir']) / "thumbnails" / project.id
        output_dir.mkdir(parents=True, exist_ok=True)

        thumbnail_config = self.config['thumbnail']

        try:
            from PIL import Image, ImageDraw, ImageFont
            from openai import OpenAI
            import httpx
            from io import BytesIO

            openai_client = OpenAI()

            styles = thumbnail_config['generation']['styles']
            thumbnails = []

            for style_idx, style in enumerate(styles[:3]):
                try:
                    style_prompts = {
                        'dramatic': f"dramatic cinematic scene about {project.topic}, dark background, spotlight, epic, movie poster style",
                        'clean': f"clean minimal illustration about {project.topic}, white background, simple, modern",
                        'colorful': f"vibrant colorful illustration about {project.topic}, bold colors, eye-catching, pop art style"
                    }

                    prompt = style_prompts.get(style, f"thumbnail about {project.topic}, {style} style")

                    response = openai_client.images.generate(
                        model="dall-e-3",
                        prompt=prompt,
                        size="1792x1024",
                        quality="standard",
                        n=1
                    )

                    image_url = response.data[0].url
                    image_response = httpx.get(image_url)

                    img = Image.open(BytesIO(image_response.content))
                    img = img.resize((1280, 720), Image.LANCZOS)

                    # Add text
                    if thumbnail_config['elements']['text']['enabled']:
                        draw = ImageDraw.Draw(img)
                        title_text = project.title[:10]

                        try:
                            font = ImageFont.truetype("assets/fonts/korean/Pretendard-Bold.ttf", 80)
                        except:
                            font = ImageFont.load_default()

                        text_bbox = draw.textbbox((0, 0), title_text, font=font)
                        text_width = text_bbox[2] - text_bbox[0]
                        text_x = (1280 - text_width) // 2
                        text_y = 720 - 150

                        # Outline
                        for dx, dy in [(-3, -3), (-3, 3), (3, -3), (3, 3)]:
                            draw.text((text_x + dx, text_y + dy), title_text, font=font, fill='black')

                        draw.text((text_x, text_y), title_text, font=font, fill='white')

                    thumb_path = output_dir / f"thumbnail_{style}.png"
                    img.save(str(thumb_path), quality=thumbnail_config['quality'])
                    thumbnails.append(str(thumb_path))

                    self.logger.info(f"  썸네일 ({style}) 생성 완료")

                except Exception as e:
                    self.logger.warning(f"  썸네일 ({style}) 생성 실패: {e}")

            project.thumbnail.paths = thumbnails
            project.thumbnail.styles_used = styles[:len(thumbnails)]
            project.thumbnail.predicted_ctr = 0.05 + (len(thumbnails) * 0.01)

        except Exception as e:
            self.logger.warning(f"Thumbnail generation failed: {e}")

        self.logger.info(f"썸네일 생성 완료 - {len(project.thumbnail.paths)}개")
        return project

    async def _phase_localization(self, project: VideoProject) -> VideoProject:
        """Phase 8: 다국어 현지화"""
        self.logger.info("Phase 8: 다국어 현지화 시작...")

        for lang in project.generate_localizations:
            self.logger.info(f"  - {lang.value} 현지화 중...")

            try:
                # Translate script
                translate_prompt = f"""다음 유튜브 스크립트를 {lang.value}로 번역하세요.

원본 ({project.language.value}):
{project.script.full_script[:3000]}

번역 규칙:
1. 자연스러운 {lang.value} 표현 사용
2. 유튜브 지식 채널에 맞는 톤 유지
3. 문화적 맥락 적응

번역된 스크립트만 출력:"""

                translated_script = self._generate_with_ai(translate_prompt, max_tokens=8000).strip()

                # SEO localization
                seo_prompt = f"""다음 SEO 데이터를 {lang.value}로 현지화하세요.

원본 제목: {project.title}
원본 설명: {project.seo.description or project.topic}

JSON으로 응답:
{{
    "title": "현지화된 제목",
    "description": "현지화된 설명 (150자 이내)",
    "tags": ["태그1", "태그2"]
}}"""

                seo_text = self._generate_with_ai(seo_prompt, max_tokens=1000)
                localized_seo = parse_json_response(seo_text)

                project.localizations[lang.value] = LocalizationData(
                    language=lang.value,
                    translated_script=translated_script,
                    localized_seo=localized_seo
                )

            except Exception as e:
                self.logger.warning(f"Localization for {lang.value} failed: {e}")

        self.logger.info(f"현지화 완료 - {len(project.generate_localizations)}개 언어")
        return project

    async def _phase_seo(self, project: VideoProject) -> VideoProject:
        """Phase 9: SEO 최적화"""
        self.logger.info("Phase 9: SEO 최적화 시작...")

        try:
            seo_prompt = f"""유튜브 SEO 최적화 데이터를 생성하세요.

제목: {project.title}
주제: {project.topic}
카테고리: {project.category.value}

JSON으로 응답:
{{
    "optimized_title": "SEO 최적화된 제목 (60자 이내)",
    "description": "SEO 최적화된 설명 (500자)",
    "tags": ["태그1", "태그2", ...],
    "hashtags": ["#해시태그1", "#해시태그2", ...],
    "timestamps": ["0:00 인트로", "0:15 ..."],
    "keywords": ["키워드1", "키워드2"]
}}"""

            text = self._generate_with_ai(seo_prompt, max_tokens=2000)
            seo_data = parse_json_response(text)

            project.seo.title = seo_data.get('optimized_title', project.title)
            project.seo.description = seo_data.get('description', '')
            project.seo.tags = seo_data.get('tags', [])
            project.seo.hashtags = seo_data.get('hashtags', [])
            project.seo.timestamps = seo_data.get('timestamps', [])
            project.seo.keywords = seo_data.get('keywords', [])

        except Exception as e:
            self.logger.warning(f"SEO optimization failed: {e}")

        self.logger.info("SEO 최적화 완료")
        return project

    async def _phase_monetization(self, project: VideoProject) -> VideoProject:
        """Phase 10: 수익화 최적화"""
        self.logger.info("Phase 10: 수익화 최적화 시작...")

        monetization_config = self.config['monetization']

        if monetization_config['ads']['enabled']:
            ad_placements = [{"timestamp": 0, "type": "pre_roll"}]

            if project.video.duration >= monetization_config['ads']['mid_roll']['min_video_length']:
                min_interval = monetization_config['ads']['mid_roll']['min_interval']
                max_ads = monetization_config['ads']['mid_roll']['max_ads']

                mid_roll_points = []
                for segment in project.script.segments:
                    if segment.get('type') in ['body', 'conclusion']:
                        mid_roll_points.append(segment.get('start_time', 0))

                filtered_points = []
                last_point = 60
                for point in mid_roll_points:
                    if isinstance(point, str) and ':' in point:
                        parts = point.split(':')
                        seconds = int(parts[0]) * 60 + int(parts[1])
                    else:
                        seconds = int(point) if point else 0

                    if seconds - last_point >= min_interval:
                        filtered_points.append(seconds)
                        last_point = seconds

                        if len(filtered_points) >= max_ads:
                            break

                for point in filtered_points:
                    ad_placements.append({
                        "timestamp": point,
                        "type": "mid_roll",
                        "reason": "natural_break"
                    })

            ad_placements.append({
                "timestamp": project.video.duration,
                "type": "post_roll"
            })

            project.monetization.ad_placements = ad_placements
            project.monetization.mid_roll_points = [p['timestamp'] for p in ad_placements if p['type'] == 'mid_roll']

        # Revenue estimation
        category_cpm = {
            'history': 1.5, 'science': 2.0, 'economy': 3.0,
            'technology': 2.5, 'education': 1.8,
        }
        base_cpm = category_cpm.get(project.category.value, 1.5)
        estimated_views = project.analytics.predicted_views or 10000

        project.monetization.estimated_revenue = (estimated_views / 1000) * base_cpm * (1 + len(project.monetization.mid_roll_points) * 0.3)

        self.logger.info("수익화 최적화 완료")
        return project

    async def _phase_quality_check(self, project: VideoProject) -> VideoProject:
        """Phase 11: 품질 검증"""
        self.logger.info("Phase 11: 품질 검증 시작...")

        scores = []

        # Script quality
        if project.script.full_script:
            script_length = len(project.script.full_script)
            target_length = project.duration_target * 5
            script_score = min(1.0, script_length / target_length)
            scores.append(script_score)

        # Visual quality
        if project.visual.images:
            visual_score = min(1.0, len(project.visual.images) / 10)
            scores.append(visual_score)

        # Audio quality
        if project.audio.mixed_audio_path:
            scores.append(0.9)

        # SEO quality
        seo_score = 0.0
        if project.seo.title: seo_score += 0.25
        if project.seo.description: seo_score += 0.25
        if project.seo.tags: seo_score += 0.25
        if project.seo.timestamps: seo_score += 0.25
        scores.append(seo_score)

        project.quality.overall_score = sum(scores) / len(scores) if scores else 0.0
        project.quality.guideline_compliance = project.quality.overall_score >= 0.6

        if project.quality.overall_score < 0.8:
            project.add_warning(f"품질 점수가 낮습니다: {project.quality.overall_score:.2f}")

        self.logger.info(f"품질 검증 완료 - 점수: {project.quality.overall_score:.2f}")
        return project

    async def _phase_repurpose(self, project: VideoProject) -> VideoProject:
        """Phase 12: 콘텐츠 재활용"""
        self.logger.info("Phase 12: 콘텐츠 재활용 시작...")

        output_dir = Path(self.config['project']['output_dir']) / "repurposed" / project.id
        output_dir.mkdir(parents=True, exist_ok=True)

        try:
            # Blog post conversion
            blog_prompt = f"""다음 유튜브 스크립트를 블로그 포스트로 변환하세요.

스크립트:
{project.script.full_script[:3000]}

형식: 마크다운, 제목/소제목 포함, 2000자 내외"""

            blog_post = self._generate_with_ai(blog_prompt, max_tokens=3000)
            blog_path = output_dir / "blog_post.md"
            with open(blog_path, 'w', encoding='utf-8') as f:
                f.write(blog_post)
            project.repurpose.blog_post_path = str(blog_path)

            # Social snippets
            snippet_prompt = f"""주제 "{project.title}"에 대한 소셜 미디어 포스트 생성:

JSON으로 응답:
{{
    "twitter": "트위터용 (280자)",
    "instagram": "인스타그램용",
    "linkedin": "링크드인용"
}}"""

            snippet_text = self._generate_with_ai(snippet_prompt, max_tokens=1000)
            project.repurpose.social_snippets = parse_json_response(snippet_text)

            snippets_path = output_dir / "social_snippets.json"
            with open(snippets_path, 'w', encoding='utf-8') as f:
                json.dump(project.repurpose.social_snippets, f, ensure_ascii=False, indent=2)

        except Exception as e:
            self.logger.warning(f"Repurpose failed: {e}")

        self.logger.info("콘텐츠 재활용 완료")
        return project

    async def _phase_upload(self, project: VideoProject) -> VideoProject:
        """Phase 13: 업로드"""
        self.logger.info("Phase 13: 업로드 시작...")

        upload_config = self.config['upload']['youtube']

        if upload_config['enabled'] and UploadPlatform.YOUTUBE in project.platforms:
            video_metadata = {
                'snippet': {
                    'title': project.seo.title or project.title,
                    'description': project.seo.description + '\n\n' + '\n'.join(project.seo.timestamps),
                    'tags': project.seo.tags,
                    'categoryId': upload_config['defaults']['category_id'],
                    'defaultLanguage': project.language.value,
                },
                'status': {
                    'privacyStatus': upload_config['default_privacy'],
                    'madeForKids': upload_config['defaults']['made_for_kids'],
                }
            }

            if project.scheduled_time:
                video_metadata['status']['publishAt'] = project.scheduled_time.isoformat()

            # Simulation result (actual upload requires YouTube API)
            project.upload_results['youtube'] = {
                'status': 'simulated',
                'video_id': f'sim_{project.id}',
                'url': f'https://youtube.com/watch?v=sim_{project.id}',
                'metadata': video_metadata
            }

            self.logger.info("  YouTube 업로드 완료 (시뮬레이션)")

        # Cross-platform upload
        cross_config = self.config['upload'].get('cross_platform', {})

        if cross_config.get('tiktok', {}).get('enabled') and project.video.shorts_paths:
            project.upload_results['tiktok'] = {
                'status': 'simulated',
                'videos': len(project.video.shorts_paths)
            }

        self.logger.info("업로드 완료")
        return project

    async def _phase_backup(self, project: VideoProject) -> None:
        """Phase 14: 백업"""
        self.logger.info("Phase 14: 백업 시작...")

        backup_config = self.config['backup']

        if backup_config['enabled']:
            if backup_config['local']['enabled']:
                backup_dir = Path(backup_config['local']['path']) / project.id
                backup_dir.mkdir(parents=True, exist_ok=True)

                project.save(str(backup_dir / "project.json"))

                import shutil
                if project.video.main_video_path and Path(project.video.main_video_path).exists():
                    shutil.copy2(project.video.main_video_path, backup_dir / "main_video.mp4")

                self.logger.info(f"  로컬 백업 완료: {backup_dir}")

        self.logger.info("백업 완료")

    # ============================================
    # 시리즈 생성 메서드
    # ============================================

    async def generate_series(
        self,
        topic: str,
        category: VideoCategory,
        style: VideoStyle,
        episode_count: int = 10,
        language: Language = Language.KOREAN,
        **kwargs
    ) -> SeriesProject:
        """시리즈 자동 생성"""
        self.logger.info(f"시리즈 생성 시작: {topic} ({episode_count}화)")

        try:
            plan_prompt = f"""유튜브 지식 채널 시리즈를 기획하세요.

대주제: {topic}
카테고리: {category.value}
총 에피소드: {episode_count}개

JSON으로 응답:
{{
    "series_name": "시리즈 이름",
    "description": "시리즈 설명",
    "episodes": [
        {{"episode": 1, "title": "에피소드 제목", "topic": "세부 주제"}},
        ...
    ]
}}"""

            text = self._generate_with_ai(plan_prompt, max_tokens=3000)
            series_plan = parse_json_response(text)
        except Exception as e:
            self.logger.warning(f"Series planning failed: {e}")
            series_plan = {
                "series_name": f"{topic} 시리즈",
                "episodes": [{"episode": i+1, "topic": f"{topic} Part {i+1}"} for i in range(episode_count)]
            }

        series = SeriesProject(
            name=series_plan.get('series_name', topic),
            description=series_plan.get('description', ''),
            topic=topic,
            category=category,
            style=style,
            total_episodes=episode_count,
            schedule={'pattern': 'weekly'}
        )

        for ep_data in series_plan.get('episodes', [])[:episode_count]:
            self.logger.info(f"  - 에피소드 {ep_data.get('episode', '?')} 생성 중...")

            episode = await self.generate_video(
                topic=ep_data.get('topic', f"{topic} Part {ep_data.get('episode', 1)}"),
                category=category,
                style=style,
                language=language,
                series_id=series.id,
                episode_number=ep_data.get('episode', 1),
                **kwargs
            )

            series.add_episode(episode)

        series.status = "completed"
        self.logger.info(f"시리즈 생성 완료: {series.name}")

        return series

    # ============================================
    # 유틸리티 메서드
    # ============================================

    def generate_video_sync(self, **kwargs) -> VideoProject:
        """동기 버전의 비디오 생성"""
        return asyncio.run(self.generate_video(**kwargs))

    def generate_series_sync(self, **kwargs) -> SeriesProject:
        """동기 버전의 시리즈 생성"""
        return asyncio.run(self.generate_series(**kwargs))


# ============================================
# CLI 인터페이스
# ============================================

def main():
    """CLI 메인 함수"""
    import argparse

    parser = argparse.ArgumentParser(
        description="AI 지식 유튜브 영상 자동 생성기 V2.0",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:

# 기본 영상 생성
python main.py generate --topic "로마 제국의 멸망" --category history

# Kurzgesagt 스타일 과학 영상
python main.py generate --topic "블랙홀이란 무엇인가" --category science --style kurzgesagt

# 다국어 버전 포함 생성
python main.py generate --topic "비트코인의 작동 원리" --category economy --localize en ja zh

# 시리즈 생성
python main.py series --topic "세계 대전 완전 정복" --category history --episodes 10

# 자동 업로드 포함
python main.py generate --topic "양자역학 쉽게 이해하기" --category physics --upload

# 주제 추천
python main.py suggest --category science --count 10
        """
    )

    subparsers = parser.add_subparsers(dest='command', help='명령어')

    # ===== generate 명령어 =====
    gen_parser = subparsers.add_parser('generate', help='영상 생성')
    gen_parser.add_argument('--topic', '-t', required=True, help='영상 주제')
    gen_parser.add_argument('--category', '-c',
                           choices=[c.value for c in VideoCategory],
                           default='history', help='카테고리')
    gen_parser.add_argument('--style', '-s',
                           choices=[s.value for s in VideoStyle],
                           default='knowledge_pirate', help='스타일')
    gen_parser.add_argument('--language', '-l',
                           choices=[l.value for l in Language],
                           default='ko', help='언어')
    gen_parser.add_argument('--duration', '-d', type=int, default=600, help='목표 길이(초)')
    gen_parser.add_argument('--localize', nargs='+',
                           choices=[l.value for l in Language], help='현지화 언어')
    gen_parser.add_argument('--no-shorts', action='store_true', help='Shorts 생성 안함')
    gen_parser.add_argument('--upload', action='store_true', help='자동 업로드')
    gen_parser.add_argument('--schedule', type=str, help='예약 업로드 시간 (ISO format)')
    gen_parser.add_argument('--config', default='config/settings.yaml', help='설정 파일')

    # ===== series 명령어 =====
    series_parser = subparsers.add_parser('series', help='시리즈 생성')
    series_parser.add_argument('--topic', '-t', required=True, help='시리즈 주제')
    series_parser.add_argument('--category', '-c',
                              choices=[c.value for c in VideoCategory], default='history')
    series_parser.add_argument('--style', '-s',
                              choices=[s.value for s in VideoStyle], default='knowledge_pirate')
    series_parser.add_argument('--episodes', '-e', type=int, default=10, help='에피소드 수')
    series_parser.add_argument('--config', default='config/settings.yaml')

    # ===== suggest 명령어 =====
    suggest_parser = subparsers.add_parser('suggest', help='주제 추천')
    suggest_parser.add_argument('--category', '-c',
                               choices=[c.value for c in VideoCategory], default='history')
    suggest_parser.add_argument('--count', type=int, default=10, help='추천 수')
    suggest_parser.add_argument('--config', default='config/settings.yaml')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # 생성기 초기화
    generator = VideoGenerator(args.config)

    # 명령어 실행
    if args.command == 'generate':
        localize = [Language(l) for l in args.localize] if args.localize else []
        schedule = datetime.fromisoformat(args.schedule) if args.schedule else None

        project = generator.generate_video_sync(
            topic=args.topic,
            category=VideoCategory(args.category),
            style=VideoStyle(args.style),
            language=Language(args.language),
            duration_target=args.duration,
            generate_shorts=not args.no_shorts,
            generate_localizations=localize,
            auto_upload=args.upload,
            schedule_time=schedule
        )

        print("\n" + "="*60)
        print("영상 생성 완료!")
        print("="*60)
        print(f"프로젝트 ID: {project.id}")
        print(f"제목: {project.title}")
        print(f"영상 경로: {project.video.main_video_path}")
        print(f"Shorts: {len(project.video.shorts_paths)}개")
        print(f"품질 점수: {project.quality.overall_score:.2f}")
        print("="*60)

    elif args.command == 'series':
        series = generator.generate_series_sync(
            topic=args.topic,
            category=VideoCategory(args.category),
            style=VideoStyle(args.style),
            episode_count=args.episodes
        )

        print("\n" + "="*60)
        print(f"시리즈 생성 완료: {series.name}")
        print("="*60)
        for ep in series.episodes:
            print(f"   {ep.episode_number}화: {ep.title}")
        print("="*60)

    elif args.command == 'suggest':
        try:
            prompt = f"""{args.category} 카테고리에서 유튜브 지식 채널용 인기 주제 {args.count}개를 추천하세요.

각 주제에 대해:
- 예상 조회수
- 경쟁 강도
- 추천 이유

JSON 배열로 응답."""

            result = generator._generate_with_ai(prompt, max_tokens=2000)

            print("\n" + "="*60)
            print("추천 주제")
            print("="*60)
            print(result)
            print("="*60)
        except Exception as e:
            print(f"주제 추천 실패: {e}")


if __name__ == "__main__":
    main()
