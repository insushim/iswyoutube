"""
Structure Builder Module
========================
Build optimal script structure for engagement
"""

from typing import Dict, List
from dataclasses import dataclass


@dataclass
class StructureSection:
    """구조 섹션"""
    name: str
    purpose: str
    duration_ratio: float  # 전체 영상 대비 비율
    key_elements: List[str]
    transition_to_next: str


@dataclass
class ScriptStructure:
    """스크립트 구조"""
    sections: List[StructureSection]
    total_duration: int
    style: str
    engagement_curve: List[float]


class StructureBuilder:
    """구조 빌더"""

    STRUCTURE_TEMPLATES = {
        "standard": [
            StructureSection("hook", "시청자 마음 사로잡기", 0.03, ["호기심 자극", "공감"], "근데 이게 왜 중요하냐면..."),
            StructureSection("intro", "왜 이게 중요한지", 0.07, ["맥락 설명", "공감대 형성"], "자 그럼 처음부터 볼까요?"),
            StructureSection("body1", "배경 이야기", 0.25, ["역사적 맥락", "기본 개념"], "근데 여기서 진짜 재밌는 건요..."),
            StructureSection("body2", "핵심 내용", 0.30, ["핵심 정보", "구체적 예시"], "그래서 이게 뭘 의미하냐면..."),
            StructureSection("body3", "그래서 어떻게 됐냐면", 0.20, ["결과", "현재 상황"], "자, 정리하자면..."),
            StructureSection("conclusion", "마무리", 0.15, ["핵심 요약", "다음 얘기 예고"], ""),
        ],
        "storytelling": [
            StructureSection("hook", "이야기 시작", 0.05, ["호기심 유발", "긴장감"], "잠깐, 여기서 배경을 좀 알아야 해요"),
            StructureSection("setup", "배경 깔기", 0.15, ["상황 설명", "인물 소개"], "그런데 문제가 생겼어요"),
            StructureSection("conflict", "반전과 갈등", 0.35, ["문제 상황", "긴장 고조"], "그리고 결정적 순간이 왔죠"),
            StructureSection("climax", "클라이맥스", 0.20, ["결정적 순간", "감정 폭발"], "결국 어떻게 됐을까요?"),
            StructureSection("resolution", "결말과 교훈", 0.25, ["해결", "우리가 배울 점"], ""),
        ],
        "listicle": [
            StructureSection("hook", "리스트 티저", 0.05, ["숫자 언급", "기대감 조성"], "자 첫 번째부터 가볼게요"),
            StructureSection("items", "본론", 0.80, ["각 아이템", "설명", "예시"], "다음 거 진짜 재밌어요"),
            StructureSection("conclusion", "마무리", 0.15, ["베스트 픽", "다음 영상 힌트"], ""),
        ],
        "myth_busting": [
            StructureSection("myth", "흔한 오해", 0.10, ["일반적 믿음"], "근데 이게 정말 맞을까요?"),
            StructureSection("question", "의문 제기", 0.10, ["왜 틀렸을까"], "제가 직접 찾아봤어요"),
            StructureSection("evidence", "증거 제시", 0.40, ["연구", "실험", "데이터"], "그래서 진실은요..."),
            StructureSection("truth", "진짜 진실", 0.25, ["실제 사실", "이유"], "이게 우리한테 의미하는 건..."),
            StructureSection("implications", "그래서 뭐?", 0.15, ["의미", "적용"], ""),
        ],
    }

    def __init__(self, config: Dict):
        self.config = config

    def build_structure(
        self,
        style: str,
        duration_target: int,
        custom_sections: List[Dict] = None
    ) -> ScriptStructure:
        """
        스크립트 구조 빌드

        Args:
            style: 스타일
            duration_target: 목표 길이 (초)
            custom_sections: 커스텀 섹션

        Returns:
            스크립트 구조
        """
        if custom_sections:
            sections = [
                StructureSection(
                    name=s.get('name', 'section'),
                    purpose=s.get('purpose', ''),
                    duration_ratio=s.get('duration_ratio', 0.2),
                    key_elements=s.get('key_elements', []),
                    transition_to_next=s.get('transition', '')
                )
                for s in custom_sections
            ]
        else:
            template_name = self._get_template_for_style(style)
            sections = self.STRUCTURE_TEMPLATES.get(
                template_name,
                self.STRUCTURE_TEMPLATES["standard"]
            )

        # 참여도 곡선 계산
        engagement_curve = self._calculate_engagement_curve(sections)

        return ScriptStructure(
            sections=sections,
            total_duration=duration_target,
            style=style,
            engagement_curve=engagement_curve
        )

    def _get_template_for_style(self, style: str) -> str:
        """스타일에 맞는 템플릿 선택"""
        style_to_template = {
            "kurzgesagt": "standard",
            "knowledge_pirate": "storytelling",
            "veritasium": "myth_busting",
            "infographic": "listicle",
            "crash_course": "standard",
            "oversimplified": "storytelling",
        }
        return style_to_template.get(style, "standard")

    def _calculate_engagement_curve(
        self,
        sections: List[StructureSection]
    ) -> List[float]:
        """참여도 곡선 계산"""
        # 간단한 참여도 모델
        curve = []
        for section in sections:
            if section.name == "hook":
                curve.append(1.0)
            elif section.name in ["climax", "truth"]:
                curve.append(0.9)
            elif section.name == "conclusion":
                curve.append(0.7)
            else:
                curve.append(0.8)
        return curve

    def get_section_duration(
        self,
        structure: ScriptStructure,
        section_name: str
    ) -> int:
        """섹션 길이 계산"""
        for section in structure.sections:
            if section.name == section_name:
                return int(structure.total_duration * section.duration_ratio)
        return 0

    def suggest_improvements(self, structure: ScriptStructure) -> List[str]:
        """구조 개선 제안"""
        suggestions = []

        # 후크가 너무 길면
        hook = next((s for s in structure.sections if s.name == "hook"), None)
        if hook and hook.duration_ratio > 0.1:
            suggestions.append("후크가 너무 깁니다. 15초 이내로 줄이세요.")

        # 결론이 너무 짧으면
        conclusion = next((s for s in structure.sections if s.name == "conclusion"), None)
        if conclusion and conclusion.duration_ratio < 0.1:
            suggestions.append("결론 부분을 늘려 CTA를 효과적으로 전달하세요.")

        return suggestions
