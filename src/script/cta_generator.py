"""
CTA Generator Module
====================
Generate effective Call-to-Action segments
"""

from typing import Dict, List
from dataclasses import dataclass
import json
import random


@dataclass
class CTA:
    """CTA 데이터"""
    text: str
    cta_type: str  # subscribe, like, comment, share, next_video
    position: str  # intro, middle, outro
    urgency_level: float
    personalized: bool


class CTAGenerator:
    """CTA 생성기"""

    CTA_TEMPLATES = {
        "subscribe": [
            "아직 구독 안 하셨다면 구독 버튼 눌러주세요!",
            "이런 영상 더 보고 싶으시다면 구독 부탁드려요!",
            "채널 구독하시면 새로운 영상 알림을 받으실 수 있어요!",
        ],
        "like": [
            "영상이 도움이 되셨다면 좋아요 한 번 부탁드려요!",
            "좋아요는 영상 제작에 큰 힘이 됩니다!",
            "이 영상 유익하셨나요? 그럼 좋아요!",
        ],
        "comment": [
            "궁금한 점은 댓글로 남겨주세요!",
            "여러분의 생각은 어떠신가요? 댓글로 알려주세요!",
            "다음 영상 주제 추천도 댓글로 받습니다!",
        ],
        "share": [
            "주변에 이 내용이 필요한 분께 공유해주세요!",
            "유익했다면 친구에게도 공유해주세요!",
        ],
        "next_video": [
            "다음 영상에서는 더 흥미로운 주제로 찾아뵙겠습니다!",
            "관련 영상이 화면에 표시되니 확인해보세요!",
        ],
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

    async def generate_cta(
        self,
        topic: str,
        style: str,
        position: str = "outro",
        cta_types: List[str] = None
    ) -> List[CTA]:
        """
        CTA 생성

        Args:
            topic: 주제
            style: 스타일
            position: 위치
            cta_types: CTA 유형

        Returns:
            CTA 리스트
        """
        types = cta_types or ["subscribe", "like", "comment"]

        if not self.client:
            return self._generate_template_ctas(types, position)

        prompt = f""""{topic}" 주제의 유튜브 영상 CTA를 생성하세요.

스타일: {style}
위치: {position}
필요한 CTA 유형: {', '.join(types)}

규칙:
1. 자연스럽고 강제적이지 않게
2. 시청자에게 가치 제공
3. 스타일에 맞는 톤

JSON 배열로 응답:
[
    {{
        "text": "CTA 텍스트",
        "cta_type": "subscribe",
        "urgency_level": 0.5
    }}
]"""

        try:
            response = self.client.messages.create(
                model=self.config.get('api', {}).get('anthropic', {}).get('model', 'claude-sonnet-4-20250514'),
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )

            text = response.content[0].text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]

            ctas_data = json.loads(text.strip())

            return [
                CTA(
                    text=c.get('text', ''),
                    cta_type=c.get('cta_type', 'subscribe'),
                    position=position,
                    urgency_level=c.get('urgency_level', 0.5),
                    personalized=True
                )
                for c in ctas_data
            ]
        except Exception:
            return self._generate_template_ctas(types, position)

    def _generate_template_ctas(
        self,
        cta_types: List[str],
        position: str
    ) -> List[CTA]:
        """템플릿 기반 CTA 생성"""
        ctas = []
        for cta_type in cta_types:
            templates = self.CTA_TEMPLATES.get(cta_type, [])
            if templates:
                ctas.append(CTA(
                    text=random.choice(templates),
                    cta_type=cta_type,
                    position=position,
                    urgency_level=0.5,
                    personalized=False
                ))
        return ctas

    async def create_outro_segment(
        self,
        topic: str,
        next_video_topic: str = None
    ) -> str:
        """아웃트로 세그먼트 생성"""
        outro = "오늘 영상은 여기까지입니다. "

        # 구독 CTA
        outro += "영상이 유익하셨다면 구독과 좋아요 부탁드려요. "

        # 다음 영상 예고
        if next_video_topic:
            outro += f"다음 영상에서는 '{next_video_topic}'에 대해 다룰 예정이니 기대해주세요! "

        outro += "그럼 다음 영상에서 뵙겠습니다!"

        return outro

    def get_mid_roll_cta(self) -> str:
        """중간 CTA"""
        mid_ctas = [
            "잠깐, 아직 구독 안 하셨다면 지금 바로!",
            "영상 끝까지 보시면 더 재밌는 내용이 있어요!",
        ]
        return random.choice(mid_ctas)
