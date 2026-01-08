"""Comment Analyzer - Analyze comments for insights"""
from typing import Dict, List
import json

class CommentAnalyzer:
    def __init__(self, config: Dict):
        self.config = config
        self.client = None
        try:
            from anthropic import Anthropic
            self.client = Anthropic()
        except: pass

    async def analyze(self, comment: str) -> Dict:
        if not self.client:
            return {"sentiment": 0, "type": "neutral", "is_question": False}
        prompt = f"""댓글 분석: "{comment[:200]}"
JSON: {{"sentiment": -1~1, "type": "positive/negative/question/suggestion/neutral", "is_question": bool}}"""
        try:
            response = self.client.messages.create(model="claude-sonnet-4-20250514", max_tokens=150, messages=[{"role": "user", "content": prompt}])
            text = response.content[0].text
            if "```" in text: text = text.split("```")[1].split("```")[0].replace("json", "")
            return json.loads(text.strip())
        except:
            return {"sentiment": 0, "type": "neutral", "is_question": False}

    async def batch_analyze(self, comments: List[str]) -> List[Dict]:
        return [await self.analyze(c) for c in comments[:10]]

    async def get_insights(self, analyses: List[Dict]) -> Dict:
        positive = sum(1 for a in analyses if a.get('sentiment', 0) > 0.3)
        questions = sum(1 for a in analyses if a.get('is_question'))
        return {"total": len(analyses), "positive_ratio": positive / max(len(analyses), 1), "questions": questions}
