"""Upload Scheduler - Schedule video uploads"""
from typing import Dict, List
from datetime import datetime, timedelta
from dataclasses import dataclass

@dataclass
class ScheduledUpload:
    video_path: str
    scheduled_time: datetime
    platform: str
    metadata: Dict
    status: str = "pending"

class UploadScheduler:
    def __init__(self, config: Dict):
        self.config = config
        self.scheduling_config = config.get('upload', {}).get('scheduling', {})
        self.scheduled_uploads = []

    def schedule(self, video_path: str, metadata: Dict, scheduled_time: datetime = None, platform: str = "youtube") -> ScheduledUpload:
        if not scheduled_time:
            scheduled_time = self._get_optimal_time()
        upload = ScheduledUpload(video_path=video_path, scheduled_time=scheduled_time, platform=platform, metadata=metadata)
        self.scheduled_uploads.append(upload)
        return upload

    def _get_optimal_time(self) -> datetime:
        now = datetime.now()
        day = now.weekday()
        if day < 5:  # Weekday
            target_time = datetime.strptime(self.scheduling_config.get('default_times', {}).get('weekday', '18:00'), '%H:%M')
        else:  # Weekend
            target_time = datetime.strptime(self.scheduling_config.get('default_times', {}).get('weekend', '14:00'), '%H:%M')
        return now.replace(hour=target_time.hour, minute=target_time.minute, second=0) + timedelta(days=1)

    def get_pending_uploads(self) -> List[ScheduledUpload]:
        return [u for u in self.scheduled_uploads if u.status == "pending"]

    async def process_scheduled(self):
        now = datetime.now()
        for upload in self.scheduled_uploads:
            if upload.status == "pending" and upload.scheduled_time <= now:
                upload.status = "processing"
