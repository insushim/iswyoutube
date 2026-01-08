"""
Source Collector Module
=======================
Collect and validate sources for content creation
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json


@dataclass
class Source:
    """소스 데이터"""
    url: str
    title: str
    source_type: str  # "academic", "news", "wikipedia", "official", "other"
    reliability_score: float
    summary: str
    key_points: List[str]
    last_updated: Optional[str] = None


class SourceCollector:
    """소스 수집기"""

    RELIABILITY_SCORES = {
        "academic": 0.95,
        "official": 0.90,
        "wikipedia": 0.80,
        "news": 0.70,
        "blog": 0.50,
        "other": 0.40,
    }

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

    async def collect_sources(
        self,
        topic: str,
        min_sources: int = 3,
        source_types: List[str] = None
    ) -> List[Source]:
        """
        소스 수집

        Args:
            topic: 주제
            min_sources: 최소 소스 수
            source_types: 수집할 소스 유형

        Returns:
            소스 리스트
        """
        # 실제로는 웹 검색 API (Google Custom Search, Bing 등) 사용
        # 여기서는 AI를 활용한 시뮬레이션

        if not self.client:
            return self._generate_fallback_sources(topic, min_sources)

        prompt = f""""{topic}" 주제에 대한 신뢰할 수 있는 소스 {min_sources}개를 제안하세요.

각 소스에 대해:
1. URL (실제 존재하는 유형의 URL)
2. 제목
3. 소스 유형 (academic/news/wikipedia/official/other)
4. 핵심 포인트 3개

JSON 배열로 응답:
[
    {{
        "url": "https://example.com/...",
        "title": "소스 제목",
        "source_type": "academic",
        "summary": "간단한 요약",
        "key_points": ["포인트1", "포인트2", "포인트3"]
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

            sources_data = json.loads(text.strip())

            return [
                Source(
                    url=s.get('url', ''),
                    title=s.get('title', ''),
                    source_type=s.get('source_type', 'other'),
                    reliability_score=self.RELIABILITY_SCORES.get(s.get('source_type', 'other'), 0.5),
                    summary=s.get('summary', ''),
                    key_points=s.get('key_points', [])
                )
                for s in sources_data
            ]
        except Exception:
            return self._generate_fallback_sources(topic, min_sources)

    def _generate_fallback_sources(self, topic: str, count: int) -> List[Source]:
        """폴백 소스 생성"""
        return [
            Source(
                url=f"https://example.com/{topic.replace(' ', '-')}-{i}",
                title=f"{topic} 관련 자료 {i+1}",
                source_type="other",
                reliability_score=0.5,
                summary=f"{topic}에 대한 참고 자료",
                key_points=[]
            )
            for i in range(count)
        ]

    async def validate_source(self, url: str) -> Dict:
        """소스 유효성 검증"""
        # 실제로는 URL 접근 및 내용 분석
        return {
            "is_valid": True,
            "is_accessible": True,
            "last_updated": None,
            "reliability_score": 0.7
        }

    async def extract_key_info(self, url: str) -> Dict:
        """소스에서 핵심 정보 추출"""
        return {
            "title": "",
            "summary": "",
            "key_points": [],
            "statistics": [],
            "quotes": []
        }
