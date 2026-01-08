"""Content Repurposer - Repurpose video content"""
from typing import Dict

class ContentRepurposer:
    def __init__(self, config: Dict): self.config = config

    async def repurpose(self, script: str, formats: list = None) -> Dict:
        formats = formats or ["blog", "social", "email"]
        results = {}
        if "blog" in formats:
            from .blog_converter import BlogConverter
            converter = BlogConverter(self.config)
            results["blog"] = await converter.convert(script)
        if "social" in formats:
            from .social_snippet_maker import SocialSnippetMaker
            maker = SocialSnippetMaker(self.config)
            results["social"] = await maker.create(script)
        return results
