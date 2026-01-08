"""
Map Generator Module
====================
Generate maps for geographic content
"""

from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class GeneratedMap:
    """생성된 지도"""
    path: str
    map_type: str
    region: str


class MapGenerator:
    """지도 생성기"""

    def __init__(self, config: Dict):
        self.config = config

    async def create(
        self,
        region: str,
        map_type: str = "basic",
        markers: List[Dict] = None,
        output_path: str = None
    ) -> GeneratedMap:
        """
        지도 생성

        Args:
            region: 지역
            map_type: 지도 유형
            markers: 마커 리스트
            output_path: 출력 경로

        Returns:
            생성된 지도
        """
        if not output_path:
            output_path = f"output/maps/{region}.png"

        Path(output_path).parent.mkdir(parents=True, exist_ok=True)

        library = self.config.get('visual', {}).get('infographic', {}).get('map_library', 'folium')

        if library == 'folium':
            return await self._create_folium(region, markers, output_path)
        else:
            return await self._create_placeholder(region, output_path)

    async def _create_folium(
        self,
        region: str,
        markers: List[Dict],
        output_path: str
    ) -> GeneratedMap:
        """Folium 지도"""
        try:
            import folium
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options

            # 지역 좌표
            region_coords = {
                "korea": [37.5665, 126.9780],
                "japan": [35.6762, 139.6503],
                "usa": [37.0902, -95.7129],
                "europe": [50.1109, 8.6821],
                "world": [0, 0],
            }

            center = region_coords.get(region.lower(), [0, 0])
            zoom = 4 if region.lower() == "world" else 6

            m = folium.Map(location=center, zoom_start=zoom, tiles='cartodbdark_matter')

            # 마커 추가
            if markers:
                for marker in markers:
                    folium.Marker(
                        location=[marker.get('lat', 0), marker.get('lon', 0)],
                        popup=marker.get('label', ''),
                        icon=folium.Icon(color='red')
                    ).add_to(m)

            # HTML로 저장 후 스크린샷
            html_path = output_path.replace('.png', '.html')
            m.save(html_path)

            # Selenium으로 스크린샷 (선택적)
            # 간단히 HTML 경로 반환
            return GeneratedMap(
                path=html_path,
                map_type="folium",
                region=region
            )
        except ImportError:
            return await self._create_placeholder(region, output_path)

    async def _create_placeholder(
        self,
        region: str,
        output_path: str
    ) -> GeneratedMap:
        """플레이스홀더 지도"""
        try:
            from PIL import Image, ImageDraw, ImageFont

            img = Image.new('RGB', (1920, 1080), color='#1A1A2E')
            draw = ImageDraw.Draw(img)

            try:
                font = ImageFont.truetype("assets/fonts/korean/Pretendard-Bold.ttf", 48)
            except:
                font = ImageFont.load_default()

            draw.text((960, 540), f"Map: {region}", fill='white', font=font, anchor='mm')

            img.save(output_path)

            return GeneratedMap(
                path=output_path,
                map_type="placeholder",
                region=region
            )
        except ImportError:
            raise RuntimeError("Pillow not installed")

    def get_available_regions(self) -> List[str]:
        """사용 가능한 지역"""
        return ["korea", "japan", "usa", "europe", "world"]
