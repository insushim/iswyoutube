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
    """후크 생성기 - Gemini API 사용"""

    HOOK_TYPES = {
        "question": "진짜 궁금해지는 질문",
        "story": "짧은 일화나 에피소드",
        "shock": "에?! 하게 만드는 사실",
        "contrast": "예상과 다른 반전",
        "confession": "솔직한 고백/인정",
        "promise": "가치 약속/혜택 제시",
    }

    def __init__(self, config: Dict):
        self.config = config
        self.client = None
        self._init_client()

    def _init_client(self):
        """AI 클라이언트 초기화 - Gemini 사용"""
        try:
            import os
            import google.generativeai as genai
            from dotenv import load_dotenv

            load_dotenv('config/api_keys.env')
            api_key = os.getenv('GEMINI_API_KEY')

            if api_key:
                genai.configure(api_key=api_key)
                self.client = genai.GenerativeModel('gemini-3-flash')
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

        prompt = f"""유튜브 영상의 오프닝 후크 {count}개를 만들어주세요.
주제: {topic}
스타일: {style}

[중요] AI가 쓴 것 같은 뻔한 후크 말고, 실제 인기 유튜버들이 쓸 법한 자연스러운 후크를 만들어주세요.

좋은 후크 예시:
- "솔직히 저도 이거 처음 들었을 때 '에이 설마' 했거든요"
- "자 여러분, 오늘 제가 충격적인 걸 발견했어요"
- "근데 이게 진짜 소름 돋는 게..."
- "아 이거 진짜 알면 인생이 바뀌어요"

피해야 할 후크 (너무 뻔함):
- "오늘은 ~에 대해 알아보겠습니다"
- "~가 궁금하신 적 있으신가요?"
- "여러분은 ~을 알고 계셨나요?"

후크 유형을 다양하게:
- question: 진짜 궁금해지는 질문 (뻔한 질문 X)
- story: 짧은 일화나 에피소드로 시작
- shock: "에?!" 하게 만드는 사실
- contrast: 예상과 다른 반전
- confession: 솔직한 고백/인정

각 후크는 10-15초 안에 말할 수 있어야 해요.

JSON 배열로 응답:
[
    {{
        "text": "후크 텍스트 (자연스러운 말투로)",
        "hook_type": "유형",
        "predicted_retention": 0.7~0.95 사이,
        "visual_suggestion": "어울리는 화면"
    }}
]"""

        try:
            response = self.client.generate_content(prompt)
            text = response.text

            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

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
        except Exception as e:
            print(f"Hook generation error: {e}")
            return self._generate_fallback_hooks(topic, count)

    def _generate_fallback_hooks(self, topic: str, count: int) -> List[Hook]:
        """폴백 후크 생성 - 자연스러운 말투로"""
        templates = [
            (f"솔직히 {topic} 이거 저도 처음 들었을 때 '에이 설마' 했거든요", "confession", 0.85),
            (f"자, 오늘 제가 {topic}에 대해서 진짜 충격적인 걸 발견했어요", "shock", 0.82),
            (f"근데 {topic} 이야기 하다 보면요, 진짜 소름 돋는 부분이 있어요", "story", 0.80),
            (f"여러분 혹시 {topic} 관련해서 이런 경험 있으세요?", "question", 0.78),
            (f"아 {topic} 이거 알고 나면요, 진짜 세상이 다르게 보여요", "promise", 0.75),
            (f"제가 {topic} 조사하다가 깜짝 놀랐는데요", "story", 0.77),
        ]

        import random
        selected = random.sample(templates[:min(len(templates), count+2)], min(count, len(templates)))

        return [
            Hook(
                text=t[0],
                hook_type=t[1],
                predicted_retention=t[2],
                visual_suggestion=f"{topic} 관련 흥미로운 장면"
            )
            for t in selected
        ]

    async def rank_hooks(self, hooks: List[Hook]) -> List[Hook]:
        """후크 순위 매기기"""
        return sorted(hooks, key=lambda h: h.predicted_retention, reverse=True)

    async def optimize_hook(self, hook: Hook, feedback: str) -> Hook:
        """후크 최적화"""
        return hook
