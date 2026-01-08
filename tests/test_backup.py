"""Tests for backup module."""
import pytest
from unittest.mock import Mock, patch, AsyncMock
from pathlib import Path


class TestBackupManager:
    """Test suite for BackupManager."""

    def test_init(self, config):
        """Test BackupManager initialization."""
        from src.backup import BackupManager

        manager = BackupManager(config)
        assert manager.config == config

    @pytest.mark.asyncio
    async def test_backup_project(self, config, temp_output_dir, sample_project_data):
        """Test project backup."""
        from src.backup import BackupManager

        config["backup"] = {
            "local": {"path": str(temp_output_dir / "backups")}
        }

        manager = BackupManager(config)

        backup_path = await manager.backup_project(
            project_id="test_001",
            project_data=sample_project_data
        )

        assert backup_path is not None
        assert Path(backup_path).exists()

    @pytest.mark.asyncio
    async def test_restore_project(self, config, temp_output_dir, sample_project_data):
        """Test project restore."""
        from src.backup import BackupManager

        config["backup"] = {
            "local": {"path": str(temp_output_dir / "backups")}
        }

        manager = BackupManager(config)

        # First backup
        backup_path = await manager.backup_project(
            project_id="test_001",
            project_data=sample_project_data
        )

        # Then restore
        restored = await manager.restore_project(backup_path)

        assert restored["id"] == sample_project_data["id"]

    @pytest.mark.asyncio
    async def test_list_backups(self, config, temp_output_dir):
        """Test listing backups."""
        from src.backup import BackupManager

        config["backup"] = {
            "local": {"path": str(temp_output_dir / "backups")}
        }

        manager = BackupManager(config)
        backups = await manager.list_backups()

        assert isinstance(backups, list)
