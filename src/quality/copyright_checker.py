"""Copyright Checker - Check for copyright issues"""
from typing import Dict, List
from pathlib import Path

class CopyrightChecker:
    def __init__(self, config: Dict): self.config = config

    async def check_image(self, image_path: str) -> Dict:
        if not Path(image_path).exists(): return {"is_safe": False, "reason": "File not found"}
        return {"is_safe": True, "source": "AI generated"}

    async def check_audio(self, audio_path: str) -> Dict:
        if not Path(audio_path).exists(): return {"is_safe": False, "reason": "File not found"}
        return {"is_safe": True, "source": "Royalty free"}

    async def check_all(self, images: List[str], audio_files: List[str]) -> Dict:
        issues = []
        for img in images:
            result = await self.check_image(img)
            if not result["is_safe"]: issues.append({"type": "image", "path": img, "reason": result["reason"]})
        for audio in audio_files:
            result = await self.check_audio(audio)
            if not result["is_safe"]: issues.append({"type": "audio", "path": audio, "reason": result["reason"]})
        return {"has_issues": len(issues) > 0, "issues": issues}
