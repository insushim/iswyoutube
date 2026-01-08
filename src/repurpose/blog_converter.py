"""Blog Converter - Convert video script to blog post"""
from typing import Dict
from pathlib import Path

class BlogConverter:
    def __init__(self, config: Dict):
        self.config = config
        self.client = None
        try:
            from anthropic import Anthropic
            self.client = Anthropic()
        except: pass

    async def convert(self, script: str, output_path: str = None) -> str:
        if not output_path: output_path = "output/repurposed/blog.md"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        if not self.client:
            content = f"# Blog Post\n\n{script[:2000]}"
        else:
            prompt = f"""스크립트를 블로그로 변환:
{script[:3000]}
마크다운, 제목/소제목 포함, 2000자:"""
            try:
                response = self.client.messages.create(model="claude-sonnet-4-20250514", max_tokens=3000, messages=[{"role": "user", "content": prompt}])
                content = response.content[0].text
            except: content = f"# Blog Post\n\n{script[:2000]}"
        with open(output_path, 'w', encoding='utf-8') as f: f.write(content)
        return output_path
