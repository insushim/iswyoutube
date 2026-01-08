"""Highlight Extractor - Extract best moments for Shorts"""
from typing import Dict, List
import json

class HighlightExtractor:
    def __init__(self, config: Dict):
        self.config = config
        self.client = None
        try:
            from anthropic import Anthropic
            self.client = Anthropic()
        except: pass

    async def extract(self, script_segments: List[Dict], count: int = 3) -> List[Dict]:
        if not self.client:
            return [{"segment_index": i, "start": 0, "duration": 30} for i in range(min(count, len(script_segments)))]
        segments_text = "\n".join([f"[{s.get('start_time', '0:00')}] {s.get('text', '')[:100]}" for s in script_segments])
        prompt = f"""영상에서 Shorts로 만들기 좋은 하이라이트 {count}개를 선정하세요.
스크립트:
{segments_text[:2000]}
JSON 배열로 응답: [{{"segment_index": 0, "start_time": "0:00", "duration": 30, "hook": "후크"}}]"""
        try:
            response = self.client.messages.create(model="claude-sonnet-4-20250514", max_tokens=1000, messages=[{"role": "user", "content": prompt}])
            text = response.content[0].text
            if "```json" in text: text = text.split("```json")[1].split("```")[0]
            return json.loads(text.strip())
        except:
            return [{"segment_index": i, "start": 0, "duration": 30} for i in range(min(count, len(script_segments)))]
