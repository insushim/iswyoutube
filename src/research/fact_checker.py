"""
Fact Checker Module
===================
Verify facts and claims for content accuracy
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json


@dataclass
class FactCheckResult:
    """팩트 체크 결과"""
    claim: str
    verdict: str  # "true", "false", "partially_true", "unverified"
    confidence: float
    sources: List[Dict]
    explanation: str
    suggested_correction: Optional[str] = None


class FactChecker:
    """팩트 체커"""

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

    async def check_claim(self, claim: str, context: str = None) -> FactCheckResult:
        """
        주장 검증

        Args:
            claim: 검증할 주장
            context: 추가 컨텍스트

        Returns:
            팩트 체크 결과
        """
        if not self.client:
            return FactCheckResult(
                claim=claim,
                verdict="unverified",
                confidence=0.0,
                sources=[],
                explanation="AI 클라이언트 없음"
            )

        prompt = f"""다음 주장을 팩트체크하세요:

주장: "{claim}"
{f'컨텍스트: {context}' if context else ''}

JSON으로 응답:
{{
    "verdict": "true/false/partially_true/unverified",
    "confidence": 0.0-1.0,
    "explanation": "판정 근거",
    "sources": ["참고 출처"],
    "suggested_correction": "수정 제안 (필요시)"
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

            return FactCheckResult(
                claim=claim,
                verdict=data.get('verdict', 'unverified'),
                confidence=data.get('confidence', 0.5),
                sources=[{"source": s} for s in data.get('sources', [])],
                explanation=data.get('explanation', ''),
                suggested_correction=data.get('suggested_correction')
            )
        except Exception as e:
            return FactCheckResult(
                claim=claim,
                verdict="unverified",
                confidence=0.0,
                sources=[],
                explanation=f"검증 실패: {str(e)}"
            )

    async def check_script(self, script: str) -> List[FactCheckResult]:
        """스크립트 전체 팩트체크"""
        # 스크립트에서 주요 주장 추출 후 각각 검증
        results = []

        # 간단한 구현: 문장별 체크 (실제로는 더 정교한 추출 필요)
        sentences = script.split('.')[:5]  # 처음 5문장만

        for sentence in sentences:
            if len(sentence.strip()) > 20:  # 충분히 긴 문장만
                result = await self.check_claim(sentence.strip())
                results.append(result)

        return results

    async def verify_statistics(self, stat: str, source: str = None) -> FactCheckResult:
        """통계 데이터 검증"""
        return await self.check_claim(f"통계: {stat}", source)
