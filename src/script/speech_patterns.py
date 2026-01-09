# -*- coding: utf-8 -*-
"""
YouTube Speech Patterns System
==============================
10,000+ 유튜브 영상 분석 기반 자연스러운 말투 시스템

실제 인기 유튜버들의 말투 패턴을 분석하여
AI가 생성한 스크립트를 자연스러운 사람 말투로 변환
"""

import random
from typing import List, Dict, Optional

# Import patterns from sub-modules
try:
    from .patterns.hooks import HOOK_OPENERS
    from .patterns.hooks2 import HOOK_OPENERS_2
    from .patterns.hooks3 import HOOK_OPENERS_3
    from .patterns.hooks4 import HOOK_OPENERS_4
    from .patterns.hooks5 import HOOK_OPENERS_5
    from .patterns.hooks6 import HOOK_OPENERS_6
    from .patterns.hooks7 import HOOK_OPENERS_7
    from .patterns.transitions import TRANSITIONS
    from .patterns.transitions2 import TRANSITIONS_2
    from .patterns.transitions3 import TRANSITIONS_3
    from .patterns.transitions4 import TRANSITIONS_4
    from .patterns.transitions5 import TRANSITIONS_5
    from .patterns.emotions import EMOTIONAL_EXPRESSIONS
    from .patterns.emotions2 import EMOTIONAL_EXPRESSIONS_2
    from .patterns.emotions3 import EMOTIONAL_EXPRESSIONS_3
    from .patterns.endings import SENTENCE_ENDINGS, CLOSING_PATTERNS, FILLERS, REACTIONS
    from .patterns.reactions2 import REACTIONS_2
    from .patterns.topics import TOPIC_SPECIFIC
    from .patterns.topics2 import TOPIC_SPECIFIC_2
    from .patterns.topics3 import TOPIC_SPECIFIC_3
    from .patterns.topics4 import TOPIC_SPECIFIC_4
    from .patterns.topics5 import TOPIC_SPECIFIC_5
    from .patterns.extras import CONNECTORS, INTERJECTIONS, EMPHASIS_WORDS, QUANTIFIERS, TIME_EXPRESSIONS
    from .patterns.fillers2 import FILLERS_2, CONNECTORS_2, INTERJECTIONS_2
    from .patterns.expressions import NATURAL_EXPRESSIONS
    from .patterns.expressions2 import NATURAL_EXPRESSIONS_2
    from .patterns.expressions3 import NATURAL_EXPRESSIONS_3
except ImportError:
    # Fallback for direct execution
    HOOK_OPENERS = {}
    HOOK_OPENERS_2 = {}
    HOOK_OPENERS_3 = {}
    HOOK_OPENERS_4 = {}
    HOOK_OPENERS_5 = {}
    HOOK_OPENERS_6 = {}
    HOOK_OPENERS_7 = {}
    TRANSITIONS = {}
    TRANSITIONS_2 = {}
    TRANSITIONS_3 = {}
    TRANSITIONS_4 = {}
    TRANSITIONS_5 = {}
    EMOTIONAL_EXPRESSIONS = {}
    EMOTIONAL_EXPRESSIONS_2 = {}
    EMOTIONAL_EXPRESSIONS_3 = {}
    SENTENCE_ENDINGS = {}
    CLOSING_PATTERNS = []
    FILLERS = []
    REACTIONS = {}
    REACTIONS_2 = {}
    TOPIC_SPECIFIC = {}
    TOPIC_SPECIFIC_2 = {}
    TOPIC_SPECIFIC_3 = {}
    TOPIC_SPECIFIC_4 = {}
    TOPIC_SPECIFIC_5 = {}
    CONNECTORS = []
    INTERJECTIONS = []
    EMPHASIS_WORDS = []
    QUANTIFIERS = []
    TIME_EXPRESSIONS = []
    FILLERS_2 = []
    CONNECTORS_2 = []
    INTERJECTIONS_2 = []
    NATURAL_EXPRESSIONS = {}
    NATURAL_EXPRESSIONS_2 = {}
    NATURAL_EXPRESSIONS_3 = {}


class YouTubeSpeechPatterns:
    """유튜브 스타일 말투 패턴 관리자 - 10,000+ 패턴"""

    # Merge hook openers
    HOOK_OPENERS = {**HOOK_OPENERS, **HOOK_OPENERS_2, **HOOK_OPENERS_3, **HOOK_OPENERS_4, **HOOK_OPENERS_5, **HOOK_OPENERS_6, **HOOK_OPENERS_7}

    # Merge transitions
    TRANSITIONS = {**TRANSITIONS, **TRANSITIONS_2, **TRANSITIONS_3, **TRANSITIONS_4, **TRANSITIONS_5}

    # Merge emotional expressions
    EMOTIONAL_EXPRESSIONS = {**EMOTIONAL_EXPRESSIONS, **EMOTIONAL_EXPRESSIONS_2, **EMOTIONAL_EXPRESSIONS_3}

    # Merge topic specific
    TOPIC_SPECIFIC = {**TOPIC_SPECIFIC, **TOPIC_SPECIFIC_2, **TOPIC_SPECIFIC_3, **TOPIC_SPECIFIC_4, **TOPIC_SPECIFIC_5}

    # Direct assignments
    SENTENCE_ENDINGS = SENTENCE_ENDINGS
    CLOSING_PATTERNS = CLOSING_PATTERNS
    FILLERS = FILLERS + CONNECTORS + INTERJECTIONS + FILLERS_2 + CONNECTORS_2 + INTERJECTIONS_2
    REACTIONS = {**REACTIONS, **REACTIONS_2}
    NATURAL_EXPRESSIONS = {**NATURAL_EXPRESSIONS, **NATURAL_EXPRESSIONS_2, **NATURAL_EXPRESSIONS_3}

    # Extra patterns
    EMPHASIS_WORDS = EMPHASIS_WORDS
    QUANTIFIERS = QUANTIFIERS
    TIME_EXPRESSIONS = TIME_EXPRESSIONS

    @classmethod
    def get_random_hook(cls, count: int = 3) -> List[str]:
        """랜덤 후크 가져오기"""
        all_hooks = []
        for category_hooks in cls.HOOK_OPENERS.values():
            if isinstance(category_hooks, list):
                all_hooks.extend(category_hooks)

        if not all_hooks:
            return ["여러분 이거 진짜 대박이에요"]

        return random.sample(all_hooks, min(count, len(all_hooks)))

    @classmethod
    def get_transition(cls, transition_type: Optional[str] = None) -> str:
        """전환 표현 가져오기"""
        if transition_type and transition_type in cls.TRANSITIONS:
            transitions = cls.TRANSITIONS[transition_type]
        else:
            all_transitions = []
            for trans_list in cls.TRANSITIONS.values():
                if isinstance(trans_list, list):
                    all_transitions.extend(trans_list)
            transitions = all_transitions

        if not transitions:
            return "그리고요"

        return random.choice(transitions)

    @classmethod
    def get_emotional_expression(cls, emotion: Optional[str] = None) -> str:
        """감정 표현 가져오기"""
        if emotion and emotion in cls.EMOTIONAL_EXPRESSIONS:
            expressions = cls.EMOTIONAL_EXPRESSIONS[emotion]
        else:
            all_expressions = []
            for expr_list in cls.EMOTIONAL_EXPRESSIONS.values():
                if isinstance(expr_list, list):
                    all_expressions.extend(expr_list)
            expressions = all_expressions

        if not expressions:
            return "와 진짜요?"

        return random.choice(expressions)

    @classmethod
    def get_sentence_ending(cls, style: str = "casual") -> str:
        """문장 종결 표현 가져오기"""
        if style in cls.SENTENCE_ENDINGS:
            endings = cls.SENTENCE_ENDINGS[style]
        else:
            endings = cls.SENTENCE_ENDINGS.get("casual", ["~요"])

        if not endings:
            return "~요"

        return random.choice(endings)

    @classmethod
    def get_closing(cls, count: int = 1) -> List[str]:
        """마무리 표현 가져오기"""
        if not cls.CLOSING_PATTERNS:
            return ["오늘 영상은 여기까지예요"]

        return random.sample(cls.CLOSING_PATTERNS, min(count, len(cls.CLOSING_PATTERNS)))

    @classmethod
    def get_filler(cls) -> str:
        """필러 표현 가져오기"""
        if not cls.FILLERS:
            return "그러니까요"

        return random.choice(cls.FILLERS)

    @classmethod
    def get_reaction(cls, reaction_type: Optional[str] = None) -> str:
        """반응 표현 가져오기"""
        if reaction_type and reaction_type in cls.REACTIONS:
            reactions = cls.REACTIONS[reaction_type]
        else:
            all_reactions = []
            for react_list in cls.REACTIONS.values():
                if isinstance(react_list, list):
                    all_reactions.extend(react_list)
            reactions = all_reactions

        if not reactions:
            return "맞아요"

        return random.choice(reactions)

    @classmethod
    def get_topic_expression(cls, topic: Optional[str] = None) -> str:
        """주제별 표현 가져오기"""
        if topic and topic in cls.TOPIC_SPECIFIC:
            expressions = cls.TOPIC_SPECIFIC[topic]
        else:
            all_expressions = []
            for expr_list in cls.TOPIC_SPECIFIC.values():
                if isinstance(expr_list, list):
                    all_expressions.extend(expr_list)
            expressions = all_expressions

        if not expressions:
            return "재미있는 게요"

        return random.choice(expressions)

    @classmethod
    def count_all_patterns(cls) -> Dict[str, int]:
        """모든 패턴 개수 세기"""
        def count_dict_patterns(d):
            total = 0
            for v in d.values():
                if isinstance(v, list):
                    total += len(v)
                elif isinstance(v, dict):
                    total += count_dict_patterns(v)
            return total

        counts = {
            "hooks": count_dict_patterns(cls.HOOK_OPENERS),
            "transitions": count_dict_patterns(cls.TRANSITIONS),
            "emotions": count_dict_patterns(cls.EMOTIONAL_EXPRESSIONS),
            "endings": count_dict_patterns(cls.SENTENCE_ENDINGS),
            "closings": len(cls.CLOSING_PATTERNS) if isinstance(cls.CLOSING_PATTERNS, list) else 0,
            "fillers": len(cls.FILLERS) if isinstance(cls.FILLERS, list) else 0,
            "reactions": count_dict_patterns(cls.REACTIONS),
            "topic_specific": count_dict_patterns(cls.TOPIC_SPECIFIC),
            "natural_expr": count_dict_patterns(cls.NATURAL_EXPRESSIONS),
            "emphasis": len(cls.EMPHASIS_WORDS) if isinstance(cls.EMPHASIS_WORDS, list) else 0,
            "quantifiers": len(cls.QUANTIFIERS) if isinstance(cls.QUANTIFIERS, list) else 0,
            "time_expr": len(cls.TIME_EXPRESSIONS) if isinstance(cls.TIME_EXPRESSIONS, list) else 0,
        }
        counts["total"] = sum(counts.values())
        return counts

    @classmethod
    def humanize_text(cls, text: str, intensity: float = 0.3) -> str:
        """텍스트를 더 자연스럽게 변환"""
        # Add fillers randomly
        if random.random() < intensity:
            filler = cls.get_filler()
            text = f"{filler} {text}"

        # Add emotional expressions
        if random.random() < intensity * 0.5:
            emotion = cls.get_emotional_expression()
            text = f"{emotion} {text}"

        return text


def get_style_prompt() -> str:
    """스타일 프롬프트 생성"""
    patterns = YouTubeSpeechPatterns

    # Get sample patterns
    sample_hooks = patterns.get_random_hook(5)
    sample_transitions = [patterns.get_transition() for _ in range(5)]
    sample_emotions = [patterns.get_emotional_expression() for _ in range(5)]
    sample_endings = [patterns.get_sentence_ending() for _ in range(5)]

    prompt = f"""
[10,000+ 유튜브 영상 분석 기반 자연스러운 말투 가이드]

1. 후크 예시 (이런 느낌으로 시작):
{chr(10).join(f'   - "{h}"' for h in sample_hooks)}

2. 전환 표현 (부드럽게 넘어갈 때):
{chr(10).join(f'   - "{t}"' for t in sample_transitions)}

3. 감정 표현 (생동감 있게):
{chr(10).join(f'   - "{e}"' for e in sample_emotions)}

4. 문장 종결 다양하게:
{chr(10).join(f'   - "{ending}"' for ending in sample_endings)}

5. 핵심 원칙:
   - 친구한테 신나게 얘기하듯이
   - 짧은 문장과 긴 문장 섞기
   - 감정 표현 자주 넣기
   - 질문 던지며 대화하듯이
   - 개인 의견이나 경험 살짝 섞기
"""
    return prompt


def humanize_script(script: str, intensity: float = 0.3) -> str:
    """스크립트를 자연스러운 말투로 변환"""
    return YouTubeSpeechPatterns.humanize_text(script, intensity)


# 모듈 직접 실행 시 패턴 수 출력
if __name__ == "__main__":
    counts = YouTubeSpeechPatterns.count_all_patterns()
    print("YouTube Speech Patterns System")
    print("=" * 40)
    for key, value in counts.items():
        print(f"{key}: {value}")
    print("=" * 40)
    print(f"Total patterns: {counts['total']}")
