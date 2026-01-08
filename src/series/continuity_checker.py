"""Continuity Checker - Check series continuity"""
from typing import Dict, List

class ContinuityChecker:
    def __init__(self, config: Dict): self.config = config

    async def check(self, episodes: List[Dict]) -> Dict:
        issues = []
        for i, ep in enumerate(episodes[1:], 1):
            prev = episodes[i-1]
            if ep.get('topic') == prev.get('topic'):
                issues.append(f"Episode {i+1} has same topic as {i}")
        return {"has_issues": len(issues) > 0, "issues": issues}

    async def suggest_order(self, episodes: List[Dict]) -> List[Dict]:
        return episodes
