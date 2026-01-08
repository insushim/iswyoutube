"""Spam Filter - Filter spam comments"""
from typing import Dict, List

SPAM_KEYWORDS = ["광고", "홍보", "링크", "http", "www", "무료", "이벤트", "당첨", "click", "subscribe to me"]

class SpamFilter:
    def __init__(self, config: Dict):
        self.config = config
        self.blacklist = config.get('community', {}).get('comments', {}).get('spam_filter', {}).get('keywords_blacklist', [])

    def is_spam(self, comment: str) -> bool:
        comment_lower = comment.lower()
        for keyword in SPAM_KEYWORDS + self.blacklist:
            if keyword.lower() in comment_lower: return True
        if comment.count('http') > 2: return True
        if len(set(comment)) < 5 and len(comment) > 10: return True
        return False

    def filter_comments(self, comments: List[str]) -> List[str]:
        return [c for c in comments if not self.is_spam(c)]

    def add_to_blacklist(self, keyword: str):
        self.blacklist.append(keyword)
