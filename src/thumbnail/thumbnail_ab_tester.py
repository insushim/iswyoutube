"""Thumbnail A/B Tester - Manage A/B tests for thumbnails"""
from typing import Dict, List
from dataclasses import dataclass
import uuid

@dataclass
class ABTest:
    test_id: str
    thumbnails: List[str]
    impressions: Dict[str, int]
    clicks: Dict[str, int]
    winner: str = None

class ThumbnailABTester:
    def __init__(self, config: Dict):
        self.config = config
        self.tests = {}

    def create_test(self, thumbnails: List[str]) -> ABTest:
        test = ABTest(
            test_id=f"test_{uuid.uuid4().hex[:8]}",
            thumbnails=thumbnails,
            impressions={t: 0 for t in thumbnails},
            clicks={t: 0 for t in thumbnails}
        )
        self.tests[test.test_id] = test
        return test

    def record_impression(self, test_id: str, thumbnail: str):
        if test_id in self.tests: self.tests[test_id].impressions[thumbnail] += 1

    def record_click(self, test_id: str, thumbnail: str):
        if test_id in self.tests: self.tests[test_id].clicks[thumbnail] += 1

    def get_winner(self, test_id: str) -> str:
        if test_id not in self.tests: return None
        test = self.tests[test_id]
        best_ctr, winner = 0, None
        for thumb in test.thumbnails:
            imp = test.impressions.get(thumb, 0)
            if imp > 0:
                ctr = test.clicks.get(thumb, 0) / imp
                if ctr > best_ctr: best_ctr, winner = ctr, thumb
        return winner
