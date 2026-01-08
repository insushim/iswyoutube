"""Backup Manager - Manage project backups"""
from typing import Dict
from pathlib import Path
import shutil
import json
from datetime import datetime

class BackupManager:
    def __init__(self, config: Dict):
        self.config = config
        self.backup_config = config.get('backup', {})
        self.backup_path = Path(self.backup_config.get('local', {}).get('path', './backups'))

    async def backup_project(self, project_id: str, project_data: Dict, files: list = None) -> str:
        backup_dir = self.backup_path / project_id / datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_dir.mkdir(parents=True, exist_ok=True)
        with open(backup_dir / "project.json", 'w', encoding='utf-8') as f:
            json.dump(project_data, f, ensure_ascii=False, indent=2, default=str)
        if files:
            for file_path in files:
                if Path(file_path).exists():
                    shutil.copy2(file_path, backup_dir / Path(file_path).name)
        return str(backup_dir)

    async def restore_project(self, backup_path: str) -> Dict:
        project_file = Path(backup_path) / "project.json"
        if project_file.exists():
            with open(project_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    async def list_backups(self, project_id: str = None) -> list:
        if project_id:
            project_dir = self.backup_path / project_id
            if project_dir.exists():
                return [str(d) for d in project_dir.iterdir() if d.is_dir()]
        return [str(d) for d in self.backup_path.iterdir() if d.is_dir()]

    async def cleanup_old_backups(self, days: int = 30):
        retention = self.backup_config.get('local', {}).get('retention_days', days)
        # 구현: 오래된 백업 삭제
        pass
