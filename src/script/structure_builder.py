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
            StructureSection("hook", "시청자 주의 끌기", 0.03, ["충격적 사실", "질문"], "자연스러운 전환"),
            StructureSection("intro", "주제 소개", 0.07, ["맥락 설명", "중요성"], "본론 예고"),
            StructureSection("body1", "배경/원인", 0.25, ["역사적 맥락", "기본 개념"], "다음 섹션 예고"),
            StructureSection("body2", "핵심 내용", 0.30, ["핵심 정보", "예시"], "인사이트 연결"),
            StructureSection("body3", "영향/결과", 0.20, ["결과", "현재 상황"], "결론 준비"),
            StructureSection("conclusion", "정리 및 CTA", 0.15, ["요약", "CTA", "다음 영상 예고"], ""),
        ],
        "storytelling": [
            StructureSection("hook", "긴장감 조성", 0.05, ["드라마틱 시작"], "스토리 진입"),
            StructureSection("setup", "배경 설정", 0.15, ["인물/상황 소개"], "갈등 도입"),
            StructureSection("conflict", "갈등 전개", 0.35, ["문제/도전"], "클라이맥스 준비"),
            StructureSection("climax", "클라이맥스", 0.20, ["결정적 순간"], "해결로 전환"),
            StructureSection("resolution", "해결 및 교훈", 0.25, ["결과", "교훈", "CTA"], ""),
        ],
        "listicle": [
            StructureSection("hook", "리스트 예고", 0.05, ["숫자 언급", "기대감"], "첫 아이템"),
            StructureSection("items", "아이템들", 0.80, ["각 아이템", "설명", "예시"], "다음 아이템"),
            StructureSection("conclusion", "정리", 0.15, ["요약", "CTA"], ""),
        ],
        "myth_busting": [
            StructureSection("myth", "잘못된 믿음 제시", 0.10, ["일반적 오해"], "의문 제기"),
            StructureSection("question", "의문 제기", 0.10, ["왜 이게 틀렸을까?"], "증거 제시"),
            StructureSection("evidence", "증거 제시", 0.40, ["연구", "실험", "데이터"], "진실 공개"),
            StructureSection("truth", "진실 공개", 0.25, ["실제 사실", "이유"], "함의 설명"),
            StructureSection("implications", "함의 및 결론", 0.15, ["의미", "적용", "CTA"], ""),
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
