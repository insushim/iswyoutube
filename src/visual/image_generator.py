"""
Image Generator Module
======================
Generate images using Gemini for prompts + placeholder/stock images
Firebase Storage 연동
"""

from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass
import httpx
import os
import uuid


@dataclass
class GeneratedImage:
    """생성된 이미지"""
    path: str
    prompt: str
    model: str
    size: str
    style: str


class ImageGenerator:
    """이미지 생성기 - Gemini + Stock Images"""

    STYLE_MODIFIERS = {
        "kurzgesagt": "flat design, minimal, pastel colors, geometric shapes, educational infographic style, no text",
        "knowledge_pirate": "warm colors, illustrated style, friendly cartoon, educational, engaging",
        "veritasium": "realistic, documentary style, scientific, clean, professional",
        "infographic": "data visualization, clean design, vibrant colors, modern infographic",
        "oversimplified": "simple stick figures, minimal, muted colors, comedic style",
        "crash_course": "colorful, educational, energetic, modern illustration",
    }

    # 무료 이미지 API (Unsplash, Pexels 등)
    FREE_IMAGE_APIS = {
        "unsplash": "https://source.unsplash.com/1920x1080/?",
        "placeholder": "https://via.placeholder.com/1920x1080.png?text=",
    }

    def __init__(self, config: Dict):
        self.config = config
        self.visual_config = config.get('visual', {}).get('image_generation', {})
        self.gemini_client = None
        self._init_gemini()

    def _init_gemini(self):
        """Gemini 클라이언트 초기화 (프롬프트 생성용)"""
        try:
            import google.generativeai as genai
            from dotenv import load_dotenv

            load_dotenv('config/api_keys.env')
            api_key = os.getenv('GEMINI_API_KEY')

            if api_key:
                genai.configure(api_key=api_key)
                self.gemini_client = genai.GenerativeModel('gemini-1.5-flash')
        except ImportError:
            pass

    async def generate(
        self,
        prompt: str,
        style: str = None,
        size: str = None,
        output_path: str = None
    ) -> GeneratedImage:
        """
        이미지 생성 - Unsplash 무료 이미지 다운로드

        Args:
            prompt: 이미지 프롬프트
            style: 스타일
            size: 크기
            output_path: 출력 경로

        Returns:
            생성된 이미지
        """
        size = size or '1920x1080'

        if not output_path:
            output_path = f"output/images/generated_{uuid.uuid4().hex[:8]}.png"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        # 키워드 추출 (간단한 처리)
        keywords = prompt.replace(',', ' ').split()[:3]
        search_term = '+'.join(keywords)

        try:
            # Unsplash에서 관련 이미지 가져오기
            image_url = f"{self.FREE_IMAGE_APIS['unsplash']}{search_term}"
            
            async with httpx.AsyncClient(follow_redirects=True) as client:
                response = await client.get(image_url, timeout=30.0)
                
                if response.status_code == 200:
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                else:
                    # 실패 시 placeholder 사용
                    await self._create_placeholder(output_path, prompt)

            return GeneratedImage(
                path=output_path,
                prompt=prompt,
                model='unsplash',
                size=size,
                style=style or 'default'
            )
        except Exception as e:
            print(f"Image generation error: {e}")
            await self._create_placeholder(output_path, prompt)
            return GeneratedImage(
                path=output_path,
                prompt=prompt,
                model='placeholder',
                size=size,
                style=style or 'default'
            )

    async def _create_placeholder(self, output_path: str, text: str):
        """플레이스홀더 이미지 생성"""
        try:
            from PIL import Image, ImageDraw, ImageFont

            # 이미지 생성
            img = Image.new('RGB', (1920, 1080), color=(50, 50, 80))
            draw = ImageDraw.Draw(img)

            # 텍스트 추가
            try:
                font = ImageFont.truetype("arial.ttf", 40)
            except:
                font = ImageFont.load_default()

            # 텍스트 중앙 배치
            text_short = text[:50] + "..." if len(text) > 50 else text
            bbox = draw.textbbox((0, 0), text_short, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            x = (1920 - text_width) // 2
            y = (1080 - text_height) // 2
            draw.text((x, y), text_short, fill=(255, 255, 255), font=font)

            img.save(output_path)
        except Exception as e:
            # PIL 실패 시 빈 파일 생성
            Path(output_path).touch()

    async def generate_batch(
        self,
        prompts: List[str],
        style: str = None,
        output_dir: str = None
    ) -> List[GeneratedImage]:
        """배치 이미지 생성"""
        output_dir = Path(output_dir or "output/images")
        output_dir.mkdir(parents=True, exist_ok=True)

        results = []
        for i, prompt in enumerate(prompts):
            output_path = str(output_dir / f"image_{i:03d}.png")
            try:
                result = await self.generate(prompt, style, output_path=output_path)
                results.append(result)
            except Exception as e:
                print(f"Image {i} generation failed: {e}")

        return results

    def get_style_modifier(self, style: str) -> str:
        """스타일 수정자 가져오기"""
        return self.STYLE_MODIFIERS.get(style, "")
