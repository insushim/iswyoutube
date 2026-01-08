"""
Hook Creator Module
===================
Create engaging hooks for video openings
"""

from typing import Dict, List
from dataclasses import dataclass
import json


@dataclass
class Hook:
    """후크 데이터"""
    text: str
    hook_type: str  # question, statistic, story, contrast, promise
    predicted_retention: float
    visual_suggestion: str


class HookCreator:
    """후크 생성기"""

    HOOK_TYPES = {
        "question": "의문을 유발하는 질문",
        "statistic": "충격적인 통계/숫자",
        "story": "짧은 스토리/일화",
        "contrast": "의외의 대비/반전",
        "promise": "가치 약속/혜택 제시",
        "mystery": "미스터리/수수께끼",
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

    async def create_hooks(
        self,
        topic: str,
        style: str,
        count: int = 5
    ) -> List[Hook]:
        """
        후크 생성

        Args:
            topic: 주제
            style: 스타일
            count: 생성할 후크 수

        Returns:
            후크 리스트
        """
        if not self.client:
            return self._generate_fallback_hooks(topic, count)

        prompt = f""""{topic}" 주제의 유튜브 영상 오프닝 후크 {count}개를 생성하세요.

스타일: {style}

후크 유형 사용:
- question: 의문을 유발하는 질문
- statistic: 충격적인 통계
- story: 짧은 스토리
- contrast: 의외의 대비
- promise: 가치 약속

각 후크는 15초 이내로 읽을 수 있어야 합니다.

JSON 배열로 응답:
[
    {{
        "text": "후크 텍스트",
        "hook_type": "question",
        "predicted_retention": 0.8,
        "visual_suggestion": "비주얼 제안"
    }}
]"""

        try:
            response = self.client.messages.create(
                model=self.config.get('api', {}).get('anthropic', {}).get('model', 'claude-sonnet-4-20250514'),
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )

            text = response.content[0].text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]

            hooks_data = json.loads(text.strip())

            return [
                Hook(
                    text=h.get('text', ''),
                    hook_type=h.get('hook_type', 'question'),
                    predicted_retention=h.get('predicted_retention', 0.7),
                    visual_suggestion=h.get('visual_suggestion', '')
                )
                for h in hooks_data
            ]
        except Exception:
            return self._generate_fallback_hooks(topic, count)

    def _generate_fallback_hooks(self, topic: str, count: int) -> List[Hook]:
        """폴백 후크 생성"""
        templates = [
            (f"왜 {topic}에 대해 아무도 진실을 말하지 않을까요?", "question"),
            (f"{topic}의 충격적인 진실, 알고 계셨나요?", "mystery"),
            (f"99%의 사람들이 {topic}에 대해 잘못 알고 있습니다.", "statistic"),
            (f"{topic}을 이해하면 세상이 다르게 보입니다.", "promise"),
            (f"역사상 가장 흥미로운 {topic} 이야기를 해드릴게요.", "story"),
        ]

        return [
            Hook(
                text=t[0],
                hook_type=t[1],
                predicted_retention=0.7,
                visual_suggestion=f"{topic} 관련 드라마틱한 이미지"
            )
            for t in templates[:count]
        ]

    async def rank_hooks(self, hooks: List[Hook]) -> List[Hook]:
        """후크 순위 매기기"""
        return sorted(hooks, key=lambda h: h.predicted_retention, reverse=True)

    async def optimize_hook(self, hook: Hook, feedback: str) -> Hook:
        """후크 최적화"""
        return hook
