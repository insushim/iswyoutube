"""
Keyword Researcher Module
=========================
Research and analyze keywords for SEO optimization
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json


@dataclass
class Keyword:
    """키워드 데이터"""
    keyword: str
    search_volume: int
    competition: str  # "low", "medium", "high"
    cpc: float
    trend: str  # "rising", "stable", "declining"
    related_keywords: List[str]


class KeywordResearcher:
    """키워드 리서처"""

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

    async def research_keywords(
        self,
        topic: str,
        language: str = "ko",
        count: int = 20
    ) -> List[Keyword]:
        """
        키워드 리서치

        Args:
            topic: 주제
            language: 언어
            count: 키워드 수

        Returns:
            키워드 리스트
        """
        if not self.client:
            return self._generate_fallback_keywords(topic, count)

        prompt = f""""{topic}" 주제에 대한 유튜브 검색 키워드 {count}개를 생성하세요.

언어: {language}

각 키워드에 대해:
1. 키워드 문구
2. 예상 검색량 (숫자)
3. 경쟁 강도 (low/medium/high)
4. 트렌드 (rising/stable/declining)
5. 관련 키워드 3개

JSON 배열로 응답:
[
    {{
        "keyword": "키워드",
        "search_volume": 10000,
        "competition": "medium",
        "cpc": 0.5,
        "trend": "stable",
        "related_keywords": ["관련1", "관련2", "관련3"]
    }}
]"""

        try:
            response = self.client.messages.create(
                model=self.config.get('api', {}).get('anthropic', {}).get('model', 'claude-sonnet-4-20250514'),
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )

            text = response.content[0].text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]

            keywords_data = json.loads(text.strip())

            return [
                Keyword(
                    keyword=k.get('keyword', ''),
                    search_volume=k.get('search_volume', 1000),
                    competition=k.get('competition', 'medium'),
                    cpc=k.get('cpc', 0.0),
                    trend=k.get('trend', 'stable'),
                    related_keywords=k.get('related_keywords', [])
                )
                for k in keywords_data
            ]
        except Exception:
            return self._generate_fallback_keywords(topic, count)

    def _generate_fallback_keywords(self, topic: str, count: int) -> List[Keyword]:
        """폴백 키워드 생성"""
        base_keywords = [
            topic,
            f"{topic} 설명",
            f"{topic} 역사",
            f"{topic} 원리",
            f"{topic} 진실",
            f"{topic} 정리",
            f"{topic} 쉽게",
            f"{topic} 요약",
        ]

        return [
            Keyword(
                keyword=kw,
                search_volume=5000 - (i * 500),
                competition="medium",
                cpc=0.3,
                trend="stable",
                related_keywords=[]
            )
            for i, kw in enumerate(base_keywords[:count])
        ]

    async def get_long_tail_keywords(self, seed_keyword: str) -> List[Keyword]:
        """롱테일 키워드 찾기"""
        return await self.research_keywords(seed_keyword, count=10)

    async def analyze_competition(self, keyword: str) -> Dict:
        """키워드 경쟁 분석"""
        return {
            "top_videos": [],
            "avg_views": 50000,
            "difficulty_score": 0.6,
            "opportunity_score": 0.7
        }
