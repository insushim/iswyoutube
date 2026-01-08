"""
Infographic Maker Module
========================
Create infographics for educational content
"""

from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Infographic:
    """인포그래픽"""
    path: str
    infographic_type: str
    data: Dict
    style: str


class InfographicMaker:
    """인포그래픽 제작기"""

    def __init__(self, config: Dict):
        self.config = config
        self.infographic_config = config.get('visual', {}).get('infographic', {})

    async def create(
        self,
        data: Dict,
        infographic_type: str,
        title: str = None,
        output_path: str = None
    ) -> Infographic:
        """
        인포그래픽 생성

        Args:
            data: 데이터
            infographic_type: 유형
            title: 제목
            output_path: 출력 경로

        Returns:
            인포그래픽
        """
        if not output_path:
            output_path = f"output/infographics/{infographic_type}.png"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        if infographic_type == "comparison":
            return await self._create_comparison(data, title, output_path)
        elif infographic_type == "timeline":
            return await self._create_timeline(data, title, output_path)
        elif infographic_type == "statistics":
            return await self._create_statistics(data, title, output_path)
        elif infographic_type == "process":
            return await self._create_process(data, title, output_path)
        else:
            return await self._create_generic(data, title, output_path)

    async def _create_comparison(
        self,
        data: Dict,
        title: str,
        output_path: str
    ) -> Infographic:
        """비교 인포그래픽"""
        try:
            from PIL import Image, ImageDraw, ImageFont

            # 캔버스 생성
            width, height = 1920, 1080
            img = Image.new('RGB', (width, height), color='#1A1A2E')
            draw = ImageDraw.Draw(img)

            # 제목
            if title:
                try:
                    font = ImageFont.truetype("assets/fonts/korean/Pretendard-Bold.ttf", 60)
                except:
                    font = ImageFont.load_default()

                draw.text((width // 2, 50), title, fill='white', font=font, anchor='mt')

            # 비교 항목 그리기
            items = data.get('items', [])
            if len(items) >= 2:
                # 왼쪽 vs 오른쪽
                left_x = width // 4
                right_x = 3 * width // 4

                draw.text((left_x, 150), str(items[0]), fill='#FF6B6B', font=font, anchor='mt')
                draw.text((width // 2, 150), "VS", fill='white', font=font, anchor='mt')
                draw.text((right_x, 150), str(items[1]), fill='#4ECDC4', font=font, anchor='mt')

            img.save(output_path)

            return Infographic(
                path=output_path,
                infographic_type="comparison",
                data=data,
                style="modern"
            )
        except ImportError:
            raise RuntimeError("Pillow not installed")

    async def _create_timeline(
        self,
        data: Dict,
        title: str,
        output_path: str
    ) -> Infographic:
        """타임라인 인포그래픽"""
        try:
            from PIL import Image, ImageDraw, ImageFont

            width, height = 1920, 1080
            img = Image.new('RGB', (width, height), color='#1A1A2E')
            draw = ImageDraw.Draw(img)

            # 중앙 라인
            draw.line([(100, height // 2), (width - 100, height // 2)], fill='white', width=3)

            # 이벤트 포인트
            events = data.get('events', [])
            spacing = (width - 200) // max(len(events), 1)

            for i, event in enumerate(events):
                x = 100 + i * spacing
                y = height // 2

                # 포인트
                draw.ellipse([x - 10, y - 10, x + 10, y + 10], fill='#FF6B6B')

                # 텍스트
                try:
                    font = ImageFont.truetype("assets/fonts/korean/Pretendard-Regular.ttf", 24)
                except:
                    font = ImageFont.load_default()

                text_y = y - 50 if i % 2 == 0 else y + 30
                draw.text((x, text_y), str(event.get('label', '')), fill='white', font=font, anchor='mt')

            img.save(output_path)

            return Infographic(
                path=output_path,
                infographic_type="timeline",
                data=data,
                style="modern"
            )
        except ImportError:
            raise RuntimeError("Pillow not installed")

    async def _create_statistics(
        self,
        data: Dict,
        title: str,
        output_path: str
    ) -> Infographic:
        """통계 인포그래픽"""
        try:
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')

            fig, ax = plt.subplots(figsize=(19.2, 10.8))
            fig.patch.set_facecolor('#1A1A2E')
            ax.set_facecolor('#1A1A2E')

            stats = data.get('statistics', [])
            labels = [s.get('label', '') for s in stats]
            values = [s.get('value', 0) for s in stats]

            colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']

            ax.bar(labels, values, color=colors[:len(labels)])

            if title:
                ax.set_title(title, color='white', fontsize=24, pad=20)

            ax.tick_params(colors='white')
            for spine in ax.spines.values():
                spine.set_color('white')

            plt.tight_layout()
            plt.savefig(output_path, dpi=100, facecolor='#1A1A2E')
            plt.close()

            return Infographic(
                path=output_path,
                infographic_type="statistics",
                data=data,
                style="modern"
            )
        except ImportError:
            raise RuntimeError("matplotlib not installed")

    async def _create_process(
        self,
        data: Dict,
        title: str,
        output_path: str
    ) -> Infographic:
        """프로세스 인포그래픽"""
        return await self._create_generic(data, title, output_path)

    async def _create_generic(
        self,
        data: Dict,
        title: str,
        output_path: str
    ) -> Infographic:
        """일반 인포그래픽"""
        try:
            from PIL import Image, ImageDraw

            img = Image.new('RGB', (1920, 1080), color='#1A1A2E')
            img.save(output_path)

            return Infographic(
                path=output_path,
                infographic_type="generic",
                data=data,
                style="modern"
            )
        except ImportError:
            raise RuntimeError("Pillow not installed")
