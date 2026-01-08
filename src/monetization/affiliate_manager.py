"""Affiliate Manager - Manage affiliate links"""
from typing import Dict, List

class AffiliateManager:
    def __init__(self, config: Dict):
        self.config = config
        self.affiliates = {}

    def add_affiliate(self, name: str, base_url: str, tag: str):
        self.affiliates[name] = {"base_url": base_url, "tag": tag}

    def generate_link(self, platform: str, product_url: str) -> str:
        if platform not in self.affiliates: return product_url
        aff = self.affiliates[platform]
        separator = "&" if "?" in product_url else "?"
        return f"{product_url}{separator}tag={aff['tag']}"

    def get_all_links(self, products: List[str], platform: str = "amazon") -> List[str]:
        return [self.generate_link(platform, p) for p in products]

    def track_click(self, link_id: str): pass
