"""Thumbnail Generator - Generate YouTube thumbnails"""
from typing import Dict, List
from pathlib import Path
import httpx

class ThumbnailGenerator:
    STYLES = {
        "dramatic": "dramatic cinematic, dark background, spotlight, epic",
        "clean": "clean minimal, white background, simple, modern",
        "colorful": "vibrant colorful, bold colors, eye-catching, pop art",
    }
    def __init__(self, config: Dict):
        self.config = config
        self.thumbnail_config = config.get('thumbnail', {})

    async def generate(self, topic: str, title: str, style: str = "dramatic", output_path: str = None) -> str:
        if not output_path:
            output_path = f"output/thumbnails/{style}.png"
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        try:
            from openai import OpenAI
            from PIL import Image, ImageDraw, ImageFont
            from io import BytesIO
            client = OpenAI()
            prompt = f"{topic}, {self.STYLES.get(style, self.STYLES['dramatic'])}, thumbnail style"
            response = client.images.generate(model="dall-e-3", prompt=prompt, size="1792x1024", quality="standard", n=1)
            img_data = httpx.get(response.data[0].url).content
            img = Image.open(BytesIO(img_data)).resize((1280, 720), Image.LANCZOS)
            draw = ImageDraw.Draw(img)
            text = title[:10]
            try: font = ImageFont.truetype("assets/fonts/korean/Pretendard-Bold.ttf", 80)
            except: font = ImageFont.load_default()
            bbox = draw.textbbox((0, 0), text, font=font)
            x, y = (1280 - (bbox[2] - bbox[0])) // 2, 720 - 150
            for dx, dy in [(-3, -3), (-3, 3), (3, -3), (3, 3)]:
                draw.text((x + dx, y + dy), text, font=font, fill='black')
            draw.text((x, y), text, font=font, fill='white')
            img.save(output_path, quality=self.thumbnail_config.get('quality', 95))
            return output_path
        except Exception as e:
            from PIL import Image
            img = Image.new('RGB', (1280, 720), color='#1A1A2E')
            img.save(output_path)
            return output_path

    async def generate_batch(self, topic: str, title: str, output_dir: str) -> List[str]:
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        results = []
        for style in self.thumbnail_config.get('generation', {}).get('styles', ['dramatic', 'clean', 'colorful']):
            path = str(Path(output_dir) / f"thumbnail_{style}.png")
            try:
                results.append(await self.generate(topic, title, style, path))
            except: pass
        return results
