import requests
import json
from datetime import datetime

class PRAnalyzer:
    def __init__(self, repo, token):
        self.repo = repo
        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github+json"
        }

    def fetch_prs(self):
        url = f"https://api.github.com/repos/{self.repo}/pulls?state=all&per_page=100"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return []

    def analyze_prs(self, prs):
        review_times = []
        merge_count = 0
        stale_prs = []

        for pr in prs:
            created = datetime.strptime(pr["created_at"], "%Y-%m-%dT%H:%M:%SZ")
            if pr["merged_at"]:
                merged = datetime.strptime(pr["merged_at"], "%Y-%m-%dT%H:%M:%SZ")
                review_time = (merged - created).total_seconds() / 3600  # in hours
                review_times.append({"id": pr["number"], "hours": review_time})
                merge_count += 1
            elif (datetime.now() - created).days > 14:
                stale_prs.append(pr["number"])

        return {
            "review_times": review_times,
            "merge_frequency": merge_count,
            "stale_prs": stale_prs
        }

if __name__ == "__main__":
    import os
    repo = "your-username/your-repo"
    token = os.getenv("GITHUB_TOKEN")  # Safe way to use token
    analyzer = PRAnalyzer(repo, token)
    prs = analyzer.fetch_prs()
    results = analyzer.analyze_prs(prs)

with open("workflow_analysis/pr_metrics.json", "w") as f:
        json.dump(results, f, indent=4)

print("✅ PR metrics saved to pr_metrics.json")
