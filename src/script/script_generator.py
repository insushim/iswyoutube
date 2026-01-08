"""
Script Generator Module
=======================
AI-powered script generation for YouTube knowledge videos
Using Google Gemini API
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json
import os


@dataclass
class ScriptSegment:
    """스크립트 세그먼트"""
    id: int
    segment_type: str  # hook, intro, body, conclusion, cta
    start_time: str
    end_time: str
    text: str
    visual_note: str
    emotion: str
    duration: int


@dataclass
class Script:
    """완성된 스크립트"""
    title: str
    full_text: str
    segments: List[ScriptSegment]
    hooks: List[str]
    key_points: List[str]
    cta: str
    word_count: int
    estimated_duration: int


class ScriptGenerator:
    """AI 기반 스크립트 생성기 - Gemini API"""

    STYLE_TEMPLATES = {
        "kurzgesagt": {
            "tone": "philosophical, cosmic perspective",
            "opening": "우주적 관점에서 시작",
            "structure": "big picture → details → hope",
            "language_style": "시각적 은유, 개인화된 '당신'",
        },
        "knowledge_pirate": {
            "tone": "friendly, conversational",
            "opening": "흥미로운 질문이나 사실",
            "structure": "story → context → details → twist",
            "language_style": "구어체, 재미있는 비유",
        },
        "veritasium": {
            "tone": "curious, investigative",
            "opening": "일반적인 오해 제시",
            "structure": "myth → investigation → truth",
            "language_style": "질문형, 실험적",
        },
        "infographic": {
            "tone": "informative, data-driven",
            "opening": "충격적인 통계",
            "structure": "numbers → analysis → insights",
            "language_style": "명확한 구분, 리스트",
        },
    }

    def __init__(self, config: Dict):
        self.config = config
        self.client = None
        self._init_client()

    def _init_client(self):
        """AI 클라이언트 초기화 - Gemini 사용"""
        try:
            import google.generativeai as genai
            from dotenv import load_dotenv

            load_dotenv('config/api_keys.env')
            api_key = os.getenv('GEMINI_API_KEY')

            if api_key:
                genai.configure(api_key=api_key)
                self.client = genai.GenerativeModel('gemini-2.5-flash-preview-05-20')
            else:
                self.client = None
        except ImportError:
            self.client = None

    async def generate(
        self,
        topic: str,
        title: str,
        category: str,
        style: str,
        duration_target: int = 600,
        language: str = "ko",
        research_data: Dict = None
    ) -> Script:
        if not self.client:
            return self._generate_fallback_script(topic, title, duration_target)

        style_info = self.STYLE_TEMPLATES.get(style, self.STYLE_TEMPLATES["knowledge_pirate"])

        prompt = f"""유튜브 지식 채널 스크립트를 작성하세요.

제목: {title}
주제: {topic}
카테고리: {category}
스타일: {style}
목표 길이: {duration_target}초 (약 {duration_target // 60}분)
언어: {language}

스타일 가이드:
- 톤: {style_info['tone']}
- 오프닝: {style_info['opening']}
- 구조: {style_info['structure']}
- 언어 스타일: {style_info['language_style']}

필수 구조:
1. [0:00-0:15] 후크 - 충격적인 질문이나 사실로 시작
2. [0:15-0:45] 도입 - 왜 이게 중요한지 설명
3. [0:45-중반] 본론1 - 배경/역사/원인
4. [중반-후반] 본론2 - 핵심 내용/메커니즘
5. [후반-끝30초전] 본론3 - 영향/결과/미래
6. [마지막 30초] 결론 + CTA

JSON 형식으로 응답:
{{
    "full_script": "전체 스크립트 텍스트",
    "segments": [
        {{
            "id": 1,
            "type": "hook",
            "start_time": "0:00",
            "end_time": "0:15",
            "text": "세그먼트 텍스트",
            "visual_note": "비주얼 설명",
            "emotion": "호기심",
            "duration": 15
        }}
    ],
    "hooks": ["후크1", "후크2", "후크3"],
    "key_points": ["핵심 포인트1", "핵심 포인트2"],
    "cta": "구독과 좋아요 부탁드려요!"
}}"""

        try:
            response = self.client.generate_content(prompt)
            text = response.text

            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            elif "```" in text:
                text = text.split("```")[1].split("```")[0]

            data = json.loads(text.strip())

            segments = [
                ScriptSegment(
                    id=s.get('id', i),
                    segment_type=s.get('type', 'body'),
                    start_time=s.get('start_time', '0:00'),
                    end_time=s.get('end_time', '0:30'),
                    text=s.get('text', ''),
                    visual_note=s.get('visual_note', ''),
                    emotion=s.get('emotion', 'neutral'),
                    duration=s.get('duration', 30)
                )
                for i, s in enumerate(data.get('segments', []))
            ]

            return Script(
                title=title,
                full_text=data.get('full_script', ''),
                segments=segments,
                hooks=data.get('hooks', []),
                key_points=data.get('key_points', []),
                cta=data.get('cta', ''),
                word_count=len(data.get('full_script', '')),
                estimated_duration=duration_target
            )
        except Exception as e:
            print(f"Gemini API error: {e}")
            return self._generate_fallback_script(topic, title, duration_target)

    def _generate_fallback_script(self, topic: str, title: str, duration_target: int) -> Script:
        text = f"""안녕하세요, 오늘은 {topic}에 대해 알아보겠습니다.

{topic}은 정말 흥미로운 주제인데요, 많은 분들이 궁금해하시는 내용입니다.

먼저 기본적인 내용부터 살펴보면...

다음으로 중요한 점은...

마지막으로 정리하자면...

오늘 영상이 도움이 되셨다면 구독과 좋아요 부탁드립니다!"""

        return Script(
            title=title,
            full_text=text,
            segments=[
                ScriptSegment(
                    id=1,
                    segment_type="full",
                    start_time="0:00",
                    end_time=f"{duration_target // 60}:00",
                    text=text,
                    visual_note=f"{topic} 관련 이미지",
                    emotion="neutral",
                    duration=duration_target
                )
            ],
            hooks=[f"{topic}의 숨겨진 진실"],
            key_points=[topic],
            cta="구독과 좋아요 부탁드립니다!",
            word_count=len(text),
            estimated_duration=duration_target
        )

    async def enhance_script(self, script: Script, enhancement_type: str) -> Script:
        return script

    async def add_humor(self, script: Script, humor_level: float = 0.3) -> Script:
        return script
