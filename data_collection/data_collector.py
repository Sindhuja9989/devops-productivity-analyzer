import os
import re
from git import Repo
from datetime import datetime, timedelta

class DataCollector:
    def __init__(self, repo_path):
        self.repo = Repo(repo_path)

    def get_commit_frequency(self, days=30):
        since_date = datetime.now() - timedelta(days=days)
        commits = list(self.repo.iter_commits(since=since_date))
        return len(commits)

    def get_deployment_frequency(self, deployments):
        # Assuming deployments is a list of datetime objects
        return len([d for d in deployments if d >= (datetime.now() - timedelta(days=30))])

    def get_lead_time(self, commit_hash):
        commit = self.repo.commit(commit_hash)
        deployment_time = self.extract_deployment_time(commit.message)
        lead_time = deployment_time - commit.committed_datetime
        return lead_time.total_seconds() / 3600  # Convert to hours

    def extract_deployment_time(self, commit_message):
        # Example message: "Deployed at: 2025-06-27T14:30:00"
        match = re.search(r"Deployed at: (\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})", commit_message)
        if match:
            return datetime.fromisoformat(match.group(1))
        else:
            # Assume current time if no deployment timestamp found
            return datetime.now()

if __name__ == "__main__":
    # ✅ Use your actual repo path
    repo_path = r"C:\Users\karnakar reddy\desktop\devops-productivity-analyzer\devops-productivity-analyzer"

    collector = DataCollector(repo_path)

    print("✅ Commit Frequency (last 30 days):", collector.get_commit_frequency())

    # ✅ Simulated deployments — replace with real timestamps if available
    sample_deployments = [
        datetime.now() - timedelta(days=3),
        datetime.now() - timedelta(days=10),
        datetime.now() - timedelta(days=40)
    ]

    print("✅ Deployment Frequency (last 30 days):", collector.get_deployment_frequency(sample_deployments))

    # ✅ Use real commit hash from your repo
    commit_hash = "c354f94"
    print(f"✅ Lead Time for commit {commit_hash}: {collector.get_lead_time(commit_hash):.2f} hours")
