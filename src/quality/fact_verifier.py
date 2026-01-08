"""Fact Verifier - Verify facts in content"""
from typing import Dict, List
import json

class FactVerifier:
    def __init__(self, config: Dict):
        self.config = config
        self.client = None
        try:
            from anthropic import Anthropic
            self.client = Anthropic()
        except: pass

    async def verify(self, claim: str) -> Dict:
        if not self.client: return {"verdict": "unverified", "confidence": 0}
        prompt = f"""다음 주장을 팩트체크: "{claim[:300]}"
JSON: {{"verdict": "true/false/partially_true/unverified", "confidence": 0-1, "explanation": "설명"}}"""
        try:
            response = self.client.messages.create(model="claude-sonnet-4-20250514", max_tokens=200, messages=[{"role": "user", "content": prompt}])
            text = response.content[0].text
            if "```" in text: text = text.split("```")[1].split("```")[0].replace("json", "")
            return json.loads(text.strip())
        except: return {"verdict": "unverified", "confidence": 0}

    async def verify_script(self, script: str) -> List[Dict]:
        sentences = [s.strip() for s in script.split('.') if len(s.strip()) > 30][:5]
        return [await self.verify(s) for s in sentences]
