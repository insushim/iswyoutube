"""Social Snippet Maker - Create social media snippets"""
from typing import Dict
import json

class SocialSnippetMaker:
    def __init__(self, config: Dict):
        self.config = config
        self.client = None
        try:
            from anthropic import Anthropic
            self.client = Anthropic()
        except: pass

    async def create(self, script: str) -> Dict:
        if not self.client:
            return {"twitter": script[:280], "instagram": script[:500], "linkedin": script[:300]}
        prompt = f"""소셜 미디어 포스트 생성:
원본: {script[:500]}
JSON: {{"twitter": "280자", "instagram": "해시태그포함", "linkedin": "전문적"}}"""
        try:
            response = self.client.messages.create(model="claude-sonnet-4-20250514", max_tokens=500, messages=[{"role": "user", "content": prompt}])
            text = response.content[0].text
            if "```" in text: text = text.split("```")[1].split("```")[0].replace("json", "")
            return json.loads(text.strip())
        except: return {"twitter": script[:280], "instagram": script[:500]}
