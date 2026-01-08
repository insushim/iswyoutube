"""SEO Optimizer - Optimize video metadata for search"""
from typing import Dict, List
import json

class SEOOptimizer:
    def __init__(self, config: Dict):
        self.config = config
        self.client = None
        try:
            from anthropic import Anthropic
            self.client = Anthropic()
        except: pass

    async def optimize(self, title: str, description: str, tags: List[str], topic: str) -> Dict:
        if not self.client:
            return {"title": title, "description": description, "tags": tags}
        prompt = f"""YouTube SEO 최적화:
제목: {title}
설명: {description[:500]}
주제: {topic}
JSON으로 응답: {{"title": "최적화된 제목 (60자)", "description": "설명 (500자)", "tags": ["태그"], "hashtags": ["#해시태그"]}}"""
        try:
            response = self.client.messages.create(model="claude-sonnet-4-20250514", max_tokens=1000, messages=[{"role": "user", "content": prompt}])
            text = response.content[0].text
            if "```json" in text: text = text.split("```json")[1].split("```")[0]
            return json.loads(text.strip())
        except:
            return {"title": title, "description": description, "tags": tags}

    async def generate_timestamps(self, segments: List[Dict]) -> List[str]:
        return [f"{s.get('start_time', '0:00')} {s.get('type', 'Section')}" for s in segments]

    async def suggest_keywords(self, topic: str) -> List[str]:
        return [topic, f"{topic} 설명", f"{topic} 역사"]
