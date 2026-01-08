"""Transition Handler Module - Handle video transitions"""
from typing import Dict

class TransitionHandler:
    TRANSITIONS = {"crossfade": "크로스페이드", "fade": "페이드", "wipe": "와이프", "slide": "슬라이드"}
    def __init__(self, config: Dict): self.config = config
    def get_transition(self, transition_type: str) -> Dict:
        return {"type": transition_type, "duration": 0.5}
    def apply_transition(self, clip1, clip2, transition_type: str = "crossfade"):
        try:
            from moviepy.editor import concatenate_videoclips
            clip1 = clip1.crossfadeout(0.5)
            clip2 = clip2.crossfadein(0.5)
            return concatenate_videoclips([clip1, clip2], method='compose')
        except: return clip1
