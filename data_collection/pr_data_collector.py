import requests
from datetime import datetime, timedelta

import requests

class PRDataCollector:
    def __init__(self, repo, token):
        self.repo = repo
        self.token = token
        self.headers = {'Authorization': f'token {self.token}'}

    def get_pull_requests(self):
        url = f'https://api.github.com/repos/{self.repo}/pulls?state=all&per_page=100'
        response = requests.get(url, headers=self.headers)

        try:
            data = response.json()
            if isinstance(data, list):
                return data
            else:
                print("❌ Error fetching PRs:", data.get("message", "Unknown error"))
                return []
        except Exception as e:
            print("❌ JSON parsing failed:", str(e))
            return []



    def analyze_pr_data(self, pr_data):
        review_times = []
        stale_prs = []
        merge_count = 0
        now = datetime.utcnow()

        for pr in pr_data:
            created_at = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            if pr["merged_at"]:
                merged_at = datetime.strptime(pr["merged_at"], "%Y-%m-%dT%H:%M:%SZ")
                diff = merged_at - created_at
                review_times.append({"pr": pr["number"], "hours": round(diff.total_seconds() / 3600, 2)})
                if (now - merged_at).days <= 30:
                    merge_count += 1
            else:
                # Stale PR = older than 7 days and still open
                if (now - created_at).days > 7:
                    stale_prs.append({"pr": pr["number"], "created_at": pr["created_at"]})

        return review_times, merge_count, stale_prs
