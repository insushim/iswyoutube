"""Mid Roll Detector - Detect optimal mid-roll ad points"""
from typing import Dict, List

class MidRollDetector:
    TRANSITION_KEYWORDS = ["다음으로", "자, 이제", "그럼", "그런데", "한편", "정리하면"]

    def __init__(self, config: Dict): self.config = config

    async def detect(self, segments: List[Dict], min_interval: int = 120) -> List[float]:
        points = []
        current_time, last_point = 0, 60
        for seg in segments:
            text = seg.get('text', '')
            duration = seg.get('duration', 30)
            is_transition = any(kw in text for kw in self.TRANSITION_KEYWORDS)
            seg_end = current_time + duration
            if is_transition and (seg_end - last_point) >= min_interval and seg_end > 60:
                points.append(seg_end)
                last_point = seg_end
            current_time = seg_end
        return points[:4]

    def validate_point(self, point: float, duration: float) -> bool:
        return 60 < point < (duration - 60)
