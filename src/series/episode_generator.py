"""Episode Generator - Generate series episodes"""
from typing import Dict

class EpisodeGenerator:
    def __init__(self, config: Dict): self.config = config

    async def generate_recap(self, previous_episodes: list) -> str:
        if not previous_episodes: return ""
        last = previous_episodes[-1]
        return f"지난 시간에 우리는 {last.get('title', '')}에 대해 알아봤습니다. 오늘은..."

    async def generate_cliffhanger(self, next_episode: Dict) -> str:
        if not next_episode: return ""
        return f"다음 시간에는 {next_episode.get('topic', '')}에 대해 더 자세히 알아보겠습니다!"

    async def add_cross_references(self, script: str, related_episodes: list) -> str:
        return script
