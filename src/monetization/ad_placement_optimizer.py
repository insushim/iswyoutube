"""Ad Placement Optimizer - Optimize ad placements"""
from typing import Dict, List

NATURAL_BREAKS = ["다음으로", "한편", "그런데", "자, 이제", "정리하자면"]

class AdPlacementOptimizer:
    def __init__(self, config: Dict):
        self.config = config
        self.ad_config = config.get('monetization', {}).get('ads', {})

    async def optimize(self, segments: List[Dict], duration: float) -> List[Dict]:
        placements = [{"timestamp": 0, "type": "pre_roll"}]
        if duration >= self.ad_config.get('mid_roll', {}).get('min_video_length', 480):
            min_interval = self.ad_config.get('mid_roll', {}).get('min_interval', 120)
            max_ads = self.ad_config.get('mid_roll', {}).get('max_ads', 4)
            current_time, last_ad = 0, 60
            for seg in segments:
                seg_duration = seg.get('duration', 30)
                text = seg.get('text', '')[:50]
                is_break = any(kw in text for kw in NATURAL_BREAKS)
                if is_break and (current_time - last_ad) >= min_interval and current_time > 60:
                    placements.append({"timestamp": current_time, "type": "mid_roll"})
                    last_ad = current_time
                    if len([p for p in placements if p['type'] == 'mid_roll']) >= max_ads: break
                current_time += seg_duration
        placements.append({"timestamp": duration, "type": "post_roll"})
        return placements

    def estimate_revenue(self, placements: List[Dict], views: int, category: str) -> float:
        cpm = {"history": 1.5, "science": 2.0, "economy": 3.0}.get(category, 1.5)
        mid_rolls = len([p for p in placements if p['type'] == 'mid_roll'])
        return (views / 1000) * cpm * (1 + mid_rolls * 0.3)
