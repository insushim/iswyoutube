"""Translator Module - Multi-language translation"""
from typing import Dict, List
import json

LANGUAGE_INFO = {
    "ko": {"name": "한국어", "formality": "formal"},
    "en": {"name": "English", "formality": "neutral"},
    "ja": {"name": "日本語", "formality": "polite"},
    "zh": {"name": "中文", "formality": "neutral"},
    "es": {"name": "Español", "formality": "formal"},
}

class Translator:
    def __init__(self, config: Dict):
        self.config = config
        self.client = None
        try:
            from anthropic import Anthropic
            self.client = Anthropic()
        except: pass

    async def translate(self, text: str, source_lang: str, target_lang: str) -> str:
        if not self.client: return text
        target_info = LANGUAGE_INFO.get(target_lang, {})
        prompt = f"""번역하세요.
원본 ({source_lang}): {text[:3000]}
대상 언어: {target_info.get('name', target_lang)}
문체: {target_info.get('formality', 'neutral')}
번역만 출력:"""
        try:
            response = self.client.messages.create(model="claude-sonnet-4-20250514", max_tokens=len(text) * 3, messages=[{"role": "user", "content": prompt}])
            return response.content[0].text.strip()
        except: return text

    async def translate_seo(self, seo_data: Dict, source_lang: str, target_lang: str) -> Dict:
        result = {}
        if seo_data.get('title'): result['title'] = await self.translate(seo_data['title'], source_lang, target_lang)
        if seo_data.get('description'): result['description'] = await self.translate(seo_data['description'], source_lang, target_lang)
        if seo_data.get('tags'): result['tags'] = [await self.translate(t, source_lang, target_lang) for t in seo_data['tags'][:5]]
        return result
