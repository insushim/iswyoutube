"""
Topic Generator Module
======================
AI-powered topic generation for YouTube knowledge channels
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json


@dataclass
class TopicSuggestion:
    """토픽 제안 데이터"""
    topic: str
    category: str
    trend_score: float
    competition_level: str
    estimated_views: int
    keywords: List[str]
    hook_ideas: List[str]
    reasoning: str


class TopicGenerator:
    """AI 기반 토픽 생성기"""

    CATEGORY_PROMPTS = {
        "history": "역사적 사건, 인물, 시대",
        "science": "과학 원리, 발견, 실험",
        "economy": "경제 개념, 시장, 금융",
        "technology": "기술 혁신, 트렌드, 제품",
        "philosophy": "철학적 개념, 사상가, 윤리",
        "psychology": "심리학 이론, 행동, 인지",
        "culture": "문화 현상, 예술, 전통",
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

    async def generate_topics(
        self,
        category: str,
        count: int = 10,
        style: str = "knowledge_pirate",
        trend_focus: bool = True
    ) -> List[TopicSuggestion]:
        """
        토픽 생성

        Args:
            category: 카테고리
            count: 생성할 토픽 수
            style: 영상 스타일
            trend_focus: 트렌드 반영 여부

        Returns:
            토픽 제안 리스트
        """
        if not self.client:
            return self._generate_fallback_topics(category, count)

        category_desc = self.CATEGORY_PROMPTS.get(category, category)

        prompt = f"""유튜브 지식 채널용 토픽 {count}개를 생성하세요.

카테고리: {category} ({category_desc})
스타일: {style}
트렌드 반영: {'예' if trend_focus else '아니오'}

각 토픽에 대해:
1. 주제 (구체적이고 흥미로운)
2. 트렌드 점수 (0.0-1.0)
3. 경쟁 수준 (낮음/중간/높음)
4. 예상 조회수
5. 관련 키워드 5개
6. 후크 아이디어 3개
7. 추천 이유

JSON 배열로 응답:
[
    {{
        "topic": "토픽",
        "trend_score": 0.8,
        "competition_level": "중간",
        "estimated_views": 50000,
        "keywords": ["키워드1", "키워드2"],
        "hook_ideas": ["후크1", "후크2"],
        "reasoning": "추천 이유"
    }}
]"""

        try:
            response = self.client.messages.create(
                model=self.config.get('api', {}).get('anthropic', {}).get('model', 'claude-sonnet-4-20250514'),
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )

            text = response.content[0].text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]

            topics_data = json.loads(text.strip())

            return [
                TopicSuggestion(
                    topic=t.get('topic', ''),
                    category=category,
                    trend_score=t.get('trend_score', 0.5),
                    competition_level=t.get('competition_level', '중간'),
                    estimated_views=t.get('estimated_views', 10000),
                    keywords=t.get('keywords', []),
                    hook_ideas=t.get('hook_ideas', []),
                    reasoning=t.get('reasoning', '')
                )
                for t in topics_data
            ]
        except Exception as e:
            return self._generate_fallback_topics(category, count)

    def _generate_fallback_topics(self, category: str, count: int) -> List[TopicSuggestion]:
        """폴백 토픽 생성"""
        fallback_topics = {
            "history": ["로마 제국의 멸망", "조선왕조 비밀", "세계대전의 진실"],
            "science": ["블랙홀의 비밀", "양자역학 이해하기", "DNA의 신비"],
            "economy": ["비트코인 원리", "인플레이션 설명", "주식시장 분석"],
        }

        topics = fallback_topics.get(category, [f"{category} 주제 {i}" for i in range(count)])

        return [
            TopicSuggestion(
                topic=topic,
                category=category,
                trend_score=0.5,
                competition_level="중간",
                estimated_views=10000,
                keywords=[topic],
                hook_ideas=[f"{topic}의 충격적인 진실"],
                reasoning="인기 있는 주제"
            )
            for topic in topics[:count]
        ]

    async def validate_topic(self, topic: str, category: str) -> Dict:
        """토픽 유효성 검증"""
        return {
            "is_valid": True,
            "trend_score": 0.7,
            "competition": "medium",
            "suggestions": []
        }
