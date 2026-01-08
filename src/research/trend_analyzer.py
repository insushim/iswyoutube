"""
Trend Analyzer Module
=====================
Analyze current trends for content creation
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import json


@dataclass
class TrendData:
    """트렌드 데이터"""
    keyword: str
    trend_score: float
    search_volume: str
    growth_rate: float
    peak_time: Optional[str]
    related_topics: List[str]
    seasonality: bool


class TrendAnalyzer:
    """트렌드 분석기"""

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

    async def analyze_topic_trend(self, topic: str, category: str = None) -> TrendData:
        """
        토픽 트렌드 분석

        Args:
            topic: 분석할 토픽
            category: 카테고리

        Returns:
            트렌드 데이터
        """
        if not self.client:
            return self._generate_fallback_trend(topic)

        prompt = f""""{topic}" 주제의 트렌드를 분석하세요.

JSON으로 응답:
{{
    "trend_score": 0.0-1.0,
    "search_volume": "높음/중간/낮음",
    "growth_rate": 0.0-1.0,
    "peak_time": "언제 가장 인기있는지",
    "related_topics": ["관련 토픽1", "관련 토픽2"],
    "seasonality": true/false,
    "reasoning": "분석 근거"
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

            return TrendData(
                keyword=topic,
                trend_score=data.get('trend_score', 0.5),
                search_volume=data.get('search_volume', '중간'),
                growth_rate=data.get('growth_rate', 0.0),
                peak_time=data.get('peak_time'),
                related_topics=data.get('related_topics', []),
                seasonality=data.get('seasonality', False)
            )
        except Exception:
            return self._generate_fallback_trend(topic)

    def _generate_fallback_trend(self, topic: str) -> TrendData:
        """폴백 트렌드 데이터"""
        return TrendData(
            keyword=topic,
            trend_score=0.5,
            search_volume="중간",
            growth_rate=0.1,
            peak_time=None,
            related_topics=[],
            seasonality=False
        )

    async def get_trending_topics(self, category: str, count: int = 10) -> List[TrendData]:
        """현재 트렌딩 토픽 조회"""
        # 실제로는 YouTube Trending API 또는 Google Trends API 사용
        return [
            TrendData(
                keyword=f"{category} 트렌딩 주제 {i}",
                trend_score=0.8 - (i * 0.05),
                search_volume="높음" if i < 3 else "중간",
                growth_rate=0.2,
                peak_time=None,
                related_topics=[],
                seasonality=False
            )
            for i in range(count)
        ]

    async def compare_trends(self, topics: List[str]) -> Dict[str, TrendData]:
        """여러 토픽 트렌드 비교"""
        results = {}
        for topic in topics:
            results[topic] = await self.analyze_topic_trend(topic)
        return results
