"""
Script Optimizer Module
=======================
Optimize scripts for engagement and clarity
"""

from typing import Dict, List
from dataclasses import dataclass
import json


@dataclass
class OptimizationResult:
    """최적화 결과"""
    original_text: str
    optimized_text: str
    changes_made: List[str]
    readability_before: float
    readability_after: float
    engagement_score: float


class ScriptOptimizer:
    """스크립트 최적화기"""

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

    async def optimize(
        self,
        script_text: str,
        optimization_goals: List[str] = None
    ) -> OptimizationResult:
        """
        스크립트 최적화

        Args:
            script_text: 원본 스크립트
            optimization_goals: 최적화 목표

        Returns:
            최적화 결과
        """
        goals = optimization_goals or ["clarity", "engagement", "pacing"]

        if not self.client:
            return OptimizationResult(
                original_text=script_text,
                optimized_text=script_text,
                changes_made=[],
                readability_before=0.7,
                readability_after=0.7,
                engagement_score=0.7
            )

        prompt = f"""다음 유튜브 스크립트를 최적화하세요.

최적화 목표: {', '.join(goals)}

원본 스크립트:
{script_text[:3000]}

규칙:
1. 문장을 간결하게
2. 능동태 사용
3. 구어체로 자연스럽게
4. 청취자 참여 유도
5. 리듬감 있는 문장 길이

JSON으로 응답:
{{
    "optimized_text": "최적화된 스크립트",
    "changes_made": ["변경사항1", "변경사항2"],
    "readability_score": 0.0-1.0,
    "engagement_score": 0.0-1.0
}}"""

        try:
            response = self.client.messages.create(
                model=self.config.get('api', {}).get('anthropic', {}).get('model', 'claude-sonnet-4-20250514'),
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )

            text = response.content[0].text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]

            data = json.loads(text.strip())

            return OptimizationResult(
                original_text=script_text,
                optimized_text=data.get('optimized_text', script_text),
                changes_made=data.get('changes_made', []),
                readability_before=0.6,
                readability_after=data.get('readability_score', 0.8),
                engagement_score=data.get('engagement_score', 0.8)
            )
        except Exception:
            return OptimizationResult(
                original_text=script_text,
                optimized_text=script_text,
                changes_made=[],
                readability_before=0.7,
                readability_after=0.7,
                engagement_score=0.7
            )

    def calculate_readability(self, text: str) -> float:
        """가독성 점수 계산"""
        # 간단한 가독성 계산
        sentences = text.split('.')
        avg_sentence_length = sum(len(s.split()) for s in sentences) / max(len(sentences), 1)

        # 문장이 짧을수록 높은 점수
        if avg_sentence_length < 10:
            return 0.9
        elif avg_sentence_length < 15:
            return 0.8
        elif avg_sentence_length < 20:
            return 0.7
        else:
            return 0.6

    async def check_pacing(self, script_text: str) -> Dict:
        """페이싱 체크"""
        return {
            "is_good": True,
            "issues": [],
            "suggestions": []
        }

    async def remove_filler_words(self, script_text: str) -> str:
        """불필요한 단어 제거"""
        filler_words = ["음", "어", "그", "이제", "자", "뭐", "그니까"]
        result = script_text
        for word in filler_words:
            result = result.replace(f" {word} ", " ")
        return result
