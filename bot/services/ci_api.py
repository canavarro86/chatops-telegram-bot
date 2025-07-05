# bot/services/ci_api.py
import requests
from config.config import SETTINGS

class CIAPI:
    def __init__(self):
        self.base = f"https://api.github.com/repos/{SETTINGS.github_repo}/actions"
        self.headers = {
            "Authorization": f"token {SETTINGS.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def trigger_build(self, workflow_id: str, ref: str = "main"):
        """
        Запускает workflow по его ID или имени файла (например, 'ci.yml') на ветке ref.
        """
        url = f"{self.base}/workflows/{workflow_id}/dispatches"
        payload = {"ref": ref}
        resp = requests.post(url, json=payload, headers=self.headers)
        resp.raise_for_status()
        return {"status": resp.status_code, "workflow": workflow_id}

    def get_last_run(self, workflow_id: str):
        url = f"{self.base}/workflows/{workflow_id}/runs?per_page=1"
        resp = requests.get(url, headers=self.headers)
        resp.raise_for_status()
        runs = resp.json().get("workflow_runs", [])
        return runs[0] if runs else None
