"""Quality Scorer - Score overall content quality"""
from typing import Dict, List

class QualityScorer:
    def __init__(self, config: Dict): self.config = config

    async def score(self, project_data: Dict) -> Dict:
        scores = {}
        # Script quality
        script = project_data.get('script', {})
        if script.get('full_script'):
            word_count = len(script['full_script'])
            target = project_data.get('duration_target', 600) * 5
            scores['script'] = min(1.0, word_count / target)
        # Visual quality
        visuals = project_data.get('visual', {})
        if visuals.get('images'):
            scores['visual'] = min(1.0, len(visuals['images']) / 10)
        # Audio quality
        audio = project_data.get('audio', {})
        scores['audio'] = 0.9 if audio.get('mixed_audio_path') else 0
        # SEO quality
        seo = project_data.get('seo', {})
        seo_score = 0
        if seo.get('title'): seo_score += 0.25
        if seo.get('description'): seo_score += 0.25
        if seo.get('tags'): seo_score += 0.25
        if seo.get('timestamps'): seo_score += 0.25
        scores['seo'] = seo_score
        overall = sum(scores.values()) / max(len(scores), 1)
        return {"overall": overall, "breakdown": scores, "passed": overall >= 0.6}

    def get_improvement_suggestions(self, scores: Dict) -> List[str]:
        suggestions = []
        breakdown = scores.get('breakdown', {})
        if breakdown.get('script', 1) < 0.7: suggestions.append("Improve script length or quality")
        if breakdown.get('visual', 1) < 0.7: suggestions.append("Add more visual assets")
        if breakdown.get('seo', 1) < 0.7: suggestions.append("Complete SEO metadata")
        return suggestions
