"""Series Planner - Plan video series"""
from typing import Dict, List
import json

class SeriesPlanner:
    def __init__(self, config: Dict):
        self.config = config
        self.client = None
        try:
            from anthropic import Anthropic
            self.client = Anthropic()
        except: pass

    async def plan(self, topic: str, episode_count: int, category: str) -> Dict:
        if not self.client:
            return {"series_name": f"{topic} 시리즈", "episodes": [{"episode": i+1, "topic": f"{topic} Part {i+1}"} for i in range(episode_count)]}
        prompt = f"""유튜브 시리즈 기획:
주제: {topic}, 에피소드: {episode_count}개, 카테고리: {category}
JSON: {{"series_name": "이름", "description": "설명", "episodes": [{{"episode": 1, "title": "제목", "topic": "세부주제"}}]}}"""
        try:
            response = self.client.messages.create(model="claude-sonnet-4-20250514", max_tokens=2000, messages=[{"role": "user", "content": prompt}])
            text = response.content[0].text
            if "```json" in text: text = text.split("```json")[1].split("```")[0]
            return json.loads(text.strip())
        except:
            return {"series_name": f"{topic} 시리즈", "episodes": [{"episode": i+1, "topic": f"{topic} Part {i+1}"} for i in range(episode_count)]}
