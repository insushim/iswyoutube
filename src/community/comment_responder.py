"""Comment Responder - Auto-respond to comments"""
from typing import Dict, List
import random

TEMPLATES = {
    "positive": ["감사합니다! 앞으로도 좋은 영상으로 찾아뵐게요", "좋게 봐주셔서 감사합니다!"],
    "question": ["좋은 질문이에요! {answer}", "궁금하셨군요! {answer}"],
    "suggestion": ["좋은 아이디어예요! 다음 영상에서 다뤄볼게요", "의견 감사합니다! 참고할게요"],
}

class CommentResponder:
    def __init__(self, config: Dict):
        self.config = config
        self.client = None
        try:
            from anthropic import Anthropic
            self.client = Anthropic()
        except: pass

    async def respond(self, comment: str, analysis: Dict, video_context: Dict = None) -> str:
        if not analysis.get('requires_response', True): return ""
        comment_type = analysis.get('type', 'neutral')
        if analysis.get('is_question') and self.client:
            prompt = f"""질문에 짧게 답변: "{comment[:200]}"
영상 주제: {video_context.get('topic', '') if video_context else ''}
1-2문장으로:"""
            try:
                response = self.client.messages.create(model="claude-sonnet-4-20250514", max_tokens=100, messages=[{"role": "user", "content": prompt}])
                return response.content[0].text.strip()
            except: pass
        if comment_type in TEMPLATES:
            return random.choice(TEMPLATES[comment_type]).format(answer="영상에서 확인해주세요!")
        return ""

    async def batch_respond(self, comments: List[Dict], video_context: Dict = None) -> List[Dict]:
        results = []
        for c in comments[:10]:
            response = await self.respond(c.get('text', ''), c.get('analysis', {}), video_context)
            if response: results.append({"comment_id": c.get('id'), "response": response})
        return results
