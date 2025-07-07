import json
from datetime import datetime, timedelta

class BottleneckDetector:
    def __init__(self, commit_data, deployment_data):
        self.commit_data = commit_data
        self.deployment_data = deployment_data

    def detect_high_lead_time(self, lead_times, threshold_hours=24):
        high_lead = [entry for entry in lead_times if entry["lead_time"] > threshold_hours]
        return high_lead

    def detect_change_failure_rate(self):
        if not self.deployment_data:
            return 0.0
        failed = [d for d in self.deployment_data if d["status"] == "failed"]
        return (len(failed) / len(self.deployment_data)) * 100

    def analyze_commit_vs_deployment(self):
        commit_counts = sum(count for _, count in self.commit_data)
        deploy_counts = len(self.deployment_data)
        return (commit_counts, deploy_counts)

if __name__ == "__main__":
    # Load from data files
    with open("data_collection/deployment_metrics.json") as f:
        deployments = json.load(f)

    commit_data = [("2025-06-20", 5), ("2025-06-22", 3), ("2025-06-24", 2)]  # Simulated
    lead_times = [{"commit": "abc123", "lead_time": 30}, {"commit": "def456", "lead_time": 10}]

    detector = BottleneckDetector(commit_data, deployments)

    print("⚠️ High Lead Time Commits:", detector.detect_high_lead_time(lead_times))
    print("❌ Change Failure Rate (%):", detector.detect_change_failure_rate())
    print("📊 Commit vs Deployment:", detector.analyze_commit_vs_deployment())
