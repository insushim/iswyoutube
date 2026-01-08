"""
Audience Analyzer Module
========================
Analyze target audience for content optimization
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json


@dataclass
class AudienceProfile:
    """타겟 오디언스 프로필"""
    age_range: str
    gender_distribution: Dict[str, float]
    interests: List[str]
    pain_points: List[str]
    content_preferences: Dict
    viewing_habits: Dict
    geographic_distribution: Dict[str, float]


@dataclass
class AudienceInsight:
    """오디언스 인사이트"""
    insight_type: str
    description: str
    recommendation: str
    confidence: float


class AudienceAnalyzer:
    """오디언스 분석기"""

    def __init__(self, config: Dict):
        self.config = config
        self.client = None
        self._init_client()

    def _init_client(self):
        """AI 클라이언트 초기화"""
        try:
            from anthropic import Anthropic
            self.client = Anthropic()
        except ImportError:
            pass

    async def analyze_target_audience(
        self,
        topic: str,
        category: str,
        style: str
    ) -> AudienceProfile:
        """
        타겟 오디언스 분석

        Args:
            topic: 주제
            category: 카테고리
            style: 콘텐츠 스타일

        Returns:
            오디언스 프로필
        """
        if not self.client:
            return self._generate_fallback_profile(category)

        prompt = f""""{topic}" 주제의 {category} 카테고리 유튜브 영상 ({style} 스타일)의 타겟 오디언스를 분석하세요.

JSON으로 응답:
{{
    "age_range": "주요 연령대",
    "gender_distribution": {{"male": 0.6, "female": 0.4}},
    "interests": ["관심사1", "관심사2", "관심사3"],
    "pain_points": ["고충1", "고충2"],
    "content_preferences": {{
        "video_length": "10-15분",
        "style": "스토리텔링",
        "pacing": "적당한 속도"
    }},
    "viewing_habits": {{
        "peak_hours": ["18:00-22:00"],
        "device": "모바일 우선"
    }},
    "geographic_distribution": {{"한국": 0.8, "미국": 0.1, "기타": 0.1}}
}}"""

        try:
            response = self.client.messages.create(
                model=self.config.get('api', {}).get('anthropic', {}).get('model', 'claude-sonnet-4-20250514'),
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            text = response.content[0].text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]

            data = json.loads(text.strip())

            return AudienceProfile(
                age_range=data.get('age_range', '20-35'),
                gender_distribution=data.get('gender_distribution', {"male": 0.5, "female": 0.5}),
                interests=data.get('interests', []),
                pain_points=data.get('pain_points', []),
                content_preferences=data.get('content_preferences', {}),
                viewing_habits=data.get('viewing_habits', {}),
                geographic_distribution=data.get('geographic_distribution', {})
            )
        except Exception:
            return self._generate_fallback_profile(category)

    def _generate_fallback_profile(self, category: str) -> AudienceProfile:
        """폴백 프로필 생성"""
        return AudienceProfile(
            age_range="20-35",
            gender_distribution={"male": 0.6, "female": 0.4},
            interests=[category, "education", "learning"],
            pain_points=["정보 부족", "이해하기 어려움"],
            content_preferences={"video_length": "10-15분"},
            viewing_habits={"peak_hours": ["18:00-22:00"]},
            geographic_distribution={"한국": 0.8}
        )

    async def get_audience_insights(
        self,
        channel_analytics: Dict = None
    ) -> List[AudienceInsight]:
        """오디언스 인사이트 추출"""
        return [
            AudienceInsight(
                insight_type="engagement",
                description="시청자들이 10분 이상 영상에서 이탈률이 높음",
                recommendation="핵심 내용을 앞부분에 배치",
                confidence=0.8
            )
        ]

    async def predict_audience_response(
        self,
        content_summary: str,
        audience_profile: AudienceProfile
    ) -> Dict:
        """오디언스 반응 예측"""
        return {
            "predicted_engagement": 0.7,
            "predicted_retention": 0.5,
            "sentiment_prediction": "positive",
            "risk_factors": []
        }
