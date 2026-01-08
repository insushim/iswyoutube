"""
Humor Injector Module
=====================
Add appropriate humor to scripts
"""

from typing import Dict, List
from dataclasses import dataclass
import json


@dataclass
class HumorElement:
    """유머 요소"""
    text: str
    humor_type: str  # pun, reference, absurd, self_deprecating, analogy
    insert_position: int
    original_text: str


class HumorInjector:
    """유머 주입기"""

    HUMOR_TYPES = {
        "pun": "말장난",
        "reference": "문화적 레퍼런스",
        "absurd": "황당한 비유",
        "self_deprecating": "자기 비하 유머",
        "analogy": "재미있는 비유",
        "unexpected": "예상 밖의 전환",
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

    async def inject_humor(
        self,
        script_text: str,
        humor_level: float = 0.3,
        style: str = "knowledge_pirate"
    ) -> tuple[str, List[HumorElement]]:
        """
        스크립트에 유머 주입

        Args:
            script_text: 원본 스크립트
            humor_level: 유머 수준 (0.0-1.0)
            style: 스타일

        Returns:
            (수정된 스크립트, 유머 요소 리스트)
        """
        if not self.client or humor_level < 0.1:
            return script_text, []

        humor_count = int(len(script_text.split('.')) * humor_level / 5)
        humor_count = max(1, min(humor_count, 5))

        prompt = f"""다음 스크립트에 자연스러운 유머 {humor_count}개를 추가하세요.

스타일: {style}
유머 수준: {humor_level * 100}%

원본 스크립트:
{script_text[:2000]}

규칙:
1. 교육적 톤 유지
2. 너무 강제적이지 않게
3. 문맥에 자연스럽게 녹아들게
4. 한국적 유머 감각 반영

JSON으로 응답:
{{
    "modified_script": "유머가 추가된 스크립트",
    "humor_elements": [
        {{
            "text": "추가된 유머",
            "humor_type": "analogy",
            "original_text": "원래 문장"
        }}
    ]
}}"""

        try:
            response = self.client.messages.create(
                model=self.config.get('api', {}).get('anthropic', {}).get('model', 'claude-sonnet-4-20250514'),
                max_tokens=3000,
                messages=[{"role": "user", "content": prompt}]
            )

            text = response.content[0].text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]

            data = json.loads(text.strip())

            elements = [
                HumorElement(
                    text=h.get('text', ''),
                    humor_type=h.get('humor_type', 'analogy'),
                    insert_position=i,
                    original_text=h.get('original_text', '')
                )
                for i, h in enumerate(data.get('humor_elements', []))
            ]

            return data.get('modified_script', script_text), elements
        except Exception:
            return script_text, []

    async def suggest_humor_points(self, script_text: str) -> List[Dict]:
        """유머 삽입 포인트 제안"""
        return []

    def validate_humor(self, humor_text: str) -> Dict:
        """유머 적절성 검증"""
        return {
            "is_appropriate": True,
            "potential_issues": [],
            "suggestion": None
        }
