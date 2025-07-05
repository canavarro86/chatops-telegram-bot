# bot/services/github_api.py

import requests
from config.config import SETTINGS

class GitHubAPI:
    def __init__(self):
        self.base = f"https://api.github.com/repos/{SETTINGS.github_repo}"
        self.headers = {
            "Authorization": f"token {SETTINGS.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def list_issues(self):
        url = f"{self.base}/issues"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        return resp.json()

    def comment_issue(self, issue_number: int, comment: str):
        url = f"{self.base}/issues/{issue_number}/comments"
        resp = requests.post(url, json={"body": comment}, headers=self.headers)
        resp.raise_for_status()
        return resp.json()
