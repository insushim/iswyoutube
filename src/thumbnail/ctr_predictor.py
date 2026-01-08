"""CTR Predictor - Predict click-through rate for thumbnails"""
from typing import Dict
import json

class CTRPredictor:
    def __init__(self, config: Dict):
        self.config = config
        self.client = None
        try:
            from anthropic import Anthropic
            self.client = Anthropic()
        except: pass

    async def predict(self, thumbnail_path: str, title: str) -> float:
        if not self.client: return 0.05
        prompt = f"""다음 유튜브 영상의 예상 CTR을 예측하세요.
제목: {title}
JSON으로 응답: {{"predicted_ctr": 0.05, "reasoning": "이유"}}"""
        try:
            response = self.client.messages.create(model="claude-sonnet-4-20250514", max_tokens=200, messages=[{"role": "user", "content": prompt}])
            text = response.content[0].text
            if "```json" in text: text = text.split("```json")[1].split("```")[0]
            return json.loads(text.strip()).get('predicted_ctr', 0.05)
        except: return 0.05

    async def get_improvement_suggestions(self, thumbnail_path: str) -> list:
        return ["Add contrasting colors", "Include a face with expression", "Use larger text"]
