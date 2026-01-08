"""A/B Test Manager - Manage content A/B tests"""
from typing import Dict, List
from dataclasses import dataclass
import uuid

@dataclass
class ABTestResult:
    test_id: str
    variant_a: Dict
    variant_b: Dict
    winner: str
    confidence: float

class ABTestManager:
    def __init__(self, config: Dict):
        self.config = config
        self.tests = {}

    def create_test(self, test_type: str, variants: List[Dict]) -> str:
        test_id = f"ab_{uuid.uuid4().hex[:8]}"
        self.tests[test_id] = {"type": test_type, "variants": variants, "results": {}}
        return test_id

    def record_result(self, test_id: str, variant_id: str, metric: str, value: float):
        if test_id in self.tests:
            if variant_id not in self.tests[test_id]["results"]:
                self.tests[test_id]["results"][variant_id] = {}
            self.tests[test_id]["results"][variant_id][metric] = value

    def get_winner(self, test_id: str) -> ABTestResult:
        if test_id not in self.tests:
            return None
        test = self.tests[test_id]
        results = test.get("results", {})
        if len(results) < 2:
            return None
        variants = list(results.keys())
        winner = max(variants, key=lambda v: results[v].get("ctr", 0))
        return ABTestResult(test_id=test_id, variant_a=results.get(variants[0], {}), variant_b=results.get(variants[1], {}), winner=winner, confidence=0.8)
