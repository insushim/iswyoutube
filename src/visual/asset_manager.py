"""
Asset Manager Module
====================
Manage visual assets
"""

from typing import Dict, List, Optional
from pathlib import Path
from dataclasses import dataclass


@dataclass
class Asset:
    """에셋"""
    path: str
    asset_type: str
    name: str
    category: str


class AssetManager:
    """에셋 관리자"""

    ASSET_TYPES = {
        "image": [".png", ".jpg", ".jpeg", ".webp"],
        "video": [".mp4", ".mov", ".avi"],
        "audio": [".mp3", ".wav", ".ogg"],
        "font": [".ttf", ".otf"],
    }

    def __init__(self, config: Dict):
        self.config = config
        self.assets_path = Path("assets")

    def get_asset(
        self,
        asset_type: str,
        category: str,
        name: str = None
    ) -> Optional[Asset]:
        """
        에셋 가져오기

        Args:
            asset_type: 에셋 유형
            category: 카테고리
            name: 이름

        Returns:
            에셋
        """
        category_path = self.assets_path / asset_type / category

        if not category_path.exists():
            return None

        extensions = self.ASSET_TYPES.get(asset_type, [])

        if name:
            for ext in extensions:
                file_path = category_path / f"{name}{ext}"
                if file_path.exists():
                    return Asset(
                        path=str(file_path),
                        asset_type=asset_type,
                        name=name,
                        category=category
                    )
        else:
            # 첫 번째 파일 반환
            for file_path in category_path.iterdir():
                if file_path.suffix in extensions:
                    return Asset(
                        path=str(file_path),
                        asset_type=asset_type,
                        name=file_path.stem,
                        category=category
                    )

        return None

    def list_assets(
        self,
        asset_type: str = None,
        category: str = None
    ) -> List[Asset]:
        """에셋 목록"""
        assets = []

        if asset_type:
            type_path = self.assets_path / asset_type
            if type_path.exists():
                if category:
                    cat_path = type_path / category
                    if cat_path.exists():
                        assets.extend(self._list_directory(cat_path, asset_type, category))
                else:
                    for cat_dir in type_path.iterdir():
                        if cat_dir.is_dir():
                            assets.extend(self._list_directory(cat_dir, asset_type, cat_dir.name))
        else:
            for type_name in self.ASSET_TYPES.keys():
                assets.extend(self.list_assets(type_name, category))

        return assets

    def _list_directory(
        self,
        directory: Path,
        asset_type: str,
        category: str
    ) -> List[Asset]:
        """디렉토리 내 에셋 목록"""
        assets = []
        extensions = self.ASSET_TYPES.get(asset_type, [])

        for file_path in directory.iterdir():
            if file_path.suffix in extensions:
                assets.append(Asset(
                    path=str(file_path),
                    asset_type=asset_type,
                    name=file_path.stem,
                    category=category
                ))

        return assets

    def add_asset(
        self,
        source_path: str,
        asset_type: str,
        category: str,
        name: str = None
    ) -> Asset:
        """에셋 추가"""
        source = Path(source_path)
        if not source.exists():
            raise FileNotFoundError(f"Source not found: {source_path}")

        target_dir = self.assets_path / asset_type / category
        target_dir.mkdir(parents=True, exist_ok=True)

        name = name or source.stem
        target_path = target_dir / f"{name}{source.suffix}"

        import shutil
        shutil.copy2(source, target_path)

        return Asset(
            path=str(target_path),
            asset_type=asset_type,
            name=name,
            category=category
        )

    def delete_asset(self, asset: Asset) -> bool:
        """에셋 삭제"""
        try:
            Path(asset.path).unlink()
            return True
        except Exception:
            return False
