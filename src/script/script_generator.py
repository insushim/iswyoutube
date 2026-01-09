"""
Script Generator Module
=======================
AI-powered script generation for YouTube knowledge videos
Using Google Gemini 3 Flash API

10,000+ 유튜브 영상 분석 기반 자연스러운 말투 시스템 통합
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
import json
import os

# 말투 패턴 시스템 임포트
try:
    from .speech_patterns import YouTubeSpeechPatterns, get_style_prompt, humanize_script
except ImportError:
    YouTubeSpeechPatterns = None
    get_style_prompt = None
    humanize_script = None


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
            "tone": "철학적이고 넓은 시야, 따뜻하면서도 진지한",
            "opening": "우리 모두가 공유하는 거대한 질문으로 시작",
            "structure": "큰 그림에서 시작해 구체적으로, 마지막엔 희망과 가능성",
            "language_style": "시각적 은유 활용, '당신'과 '우리'로 친밀감, 감정을 자극하는 문장",
            "human_touch": "개인적 경험이나 감정 공유, 청중의 고민에 공감, 때론 유머러스한 비유",
        },
        "knowledge_pirate": {
            "tone": "친근하고 수다스러운, 옆자리 친구가 얘기하듯",
            "opening": "일상에서 겪는 궁금증이나 흥미로운 일화로 시작",
            "structure": "이야기 → 배경 → 핵심 → 반전 또는 인사이트",
            "language_style": "완전 구어체, '근데 말이야', '솔직히', '진짜' 같은 표현 자연스럽게",
            "human_touch": "실수담이나 개인 의견 공유, 청중에게 질문 던지기, 가끔 엉뚱한 상상",
        },
        "veritasium": {
            "tone": "호기심 가득, 탐정처럼 파헤치는",
            "opening": "대부분 사람들이 잘못 알고 있는 것으로 시작",
            "structure": "통념 제시 → 의문 제기 → 탐구 → 진실 공개",
            "language_style": "계속 질문 던지기, '왜 그럴까요?', '정말 그럴까요?'",
            "human_touch": "직접 실험하거나 경험한 것처럼 서술, 틀렸던 자신의 과거 인정",
        },
        "infographic": {
            "tone": "정보 전달 중심이지만 지루하지 않게",
            "opening": "놀라운 숫자나 비교로 시선 끌기",
            "structure": "수치 → 의미 분석 → 우리 삶에의 영향",
            "language_style": "명확한 구분, 비교와 대조, 시각화 설명",
            "human_touch": "숫자 뒤의 인간적 이야기, '이게 뭘 의미하냐면...'",
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
                self.client = genai.GenerativeModel('gemini-3-flash')
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

        human_touch = style_info.get('human_touch', '자연스럽고 진정성 있게')

        # 말투 패턴 시스템에서 가이드 가져오기
        speech_guide = ""
        sample_hooks = []
        sample_transitions = []
        sample_closings = []

        if YouTubeSpeechPatterns:
            sample_hooks = YouTubeSpeechPatterns.get_random_hook(5)
            sample_transitions = [YouTubeSpeechPatterns.get_transition() for _ in range(5)]
            sample_closings = YouTubeSpeechPatterns.get_closing(3)
            speech_guide = get_style_prompt() if get_style_prompt else ""

        prompt = f"""당신은 {duration_target // 60}분짜리 유튜브 영상 스크립트를 작성하는 전문 작가입니다.
AI가 쓴 것 같은 딱딱한 글이 아니라, 실제 인기 유튜버가 쓴 것처럼 자연스럽고 재미있는 스크립트를 작성해주세요.

제목: {title}
주제: {topic}
카테고리: {category}

{speech_guide}

[이 영상의 스타일]
- 톤앤매너: {style_info['tone']}
- 시작 방식: {style_info['opening']}
- 흐름: {style_info['structure']}
- 말투: {style_info['language_style']}
- 인간미: {human_touch}

[실제 유튜버 후크 예시 - 이런 느낌으로!]
{chr(10).join(f'- "{h}"' for h in sample_hooks) if sample_hooks else '- "여러분 이거 진짜 미쳤어요"'}

[자연스러운 전환 표현 예시]
{chr(10).join(f'- "{t}"' for t in sample_transitions) if sample_transitions else '- "근데 여기서 재밌는 게 있어요"'}

[자연스러운 마무리 예시]
{chr(10).join(f'- "{c}"' for c in sample_closings) if sample_closings else '- "오늘 영상은 여기까지예요"'}

[핵심 지침]
1. 친구한테 신나게 얘기하듯이 써주세요 (교과서 설명체 절대 금지)
2. 종결어미 다양하게: "~거든요", "~잖아요", "~인 거죠", "~더라고요", "~ㄹ걸요"
3. 자연스러운 전환: "근데 여기서 재밌는 건요", "아 그리고", "참 이것도"
4. 감정 표현 넣기: "와 진짜 대박", "솔직히 소름 돋았어요", "이거 너무 웃긴 게"
5. 청중과 대화하기: "여러분 어떻게 생각하세요?", "이런 적 있으시죠?"
6. 개인 의견 살짝: "저는 이 부분이 제일...", "개인적으로 느끼기엔..."

[절대 금지]
- "오늘은 ~에 대해 알아보겠습니다" 시작
- "~입니다/~합니다"만 반복
- 모든 문장 같은 길이
- 로봇 설명체

목표 길이: 약 {duration_target}초 ({duration_target // 60}분)

JSON으로 응답:
{{
    "full_script": "전체 스크립트 (자연스럽고 재미있게)",
    "segments": [
        {{
            "id": 1,
            "type": "hook/intro/body/conclusion",
            "start_time": "0:00",
            "end_time": "시간",
            "text": "해당 부분 텍스트",
            "visual_note": "어울리는 화면",
            "emotion": "감정/분위기",
            "duration": 초
        }}
    ],
    "hooks": ["대안 후크 3개 (각각 다른 스타일)"],
    "key_points": ["핵심 메시지들"],
    "cta": "자연스러운 마무리"
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
        # 자연스러운 폴백 스크립트 생성
        hooks = []
        if YouTubeSpeechPatterns:
            hooks = YouTubeSpeechPatterns.get_random_hook(3)

        hook = hooks[0] if hooks else f"여러분 {topic} 이거 진짜 대박이거든요"

        text = f"""{hook}

아니 근데 진짜로, {topic} 이거 알면 알수록 빠져들어요. 저도 처음엔 그냥 '뭐 별거 있겠어?' 했는데, 찾아보니까 완전 다른 세상이더라고요.

자 그럼 처음부터 차근차근 가볼게요. 일단 {topic}이 뭔지부터 간단히 설명드릴게요.

근데 여기서 진짜 재밌는 게 있어요. 대부분 사람들이 모르는 부분인데...

솔직히 저도 이 부분에서 '와 진짜?' 했거든요. 생각보다 훨씬 깊은 내용이 있어요.

그래서 결론적으로 말씀드리면요, {topic}은 우리가 생각하는 것보다 훨씬 흥미로운 주제예요.

오늘 영상 여기까지고요, 재밌게 보셨다면 좋겠네요. 다음에 더 재밌는 거 가져올게요!"""

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
                    visual_note=f"{topic} 관련 흥미로운 이미지",
                    emotion="excited",
                    duration=duration_target
                )
            ],
            hooks=hooks if hooks else [f"여러분 {topic} 이거 진짜 미쳤어요"],
            key_points=[f"{topic}의 핵심 내용", "숨겨진 사실들"],
            cta="다음에 더 재밌는 거 가져올게요!",
            word_count=len(text),
            estimated_duration=duration_target
        )

    async def enhance_script(self, script: Script, enhancement_type: str) -> Script:
        return script

    async def add_humor(self, script: Script, humor_level: float = 0.3) -> Script:
        return script
