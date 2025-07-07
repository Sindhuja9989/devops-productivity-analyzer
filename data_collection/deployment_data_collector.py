import json
from datetime import datetime, timedelta
import os

class DeploymentDataCollector:
    def __init__(self):
        # Simulated deployment data
        self.deployments = [
            {"deployment": "deploy1", "status": "success", "timestamp": "2025-06-20T10:00:00"},
            {"deployment": "deploy2", "status": "failed",  "timestamp": "2025-06-22T13:30:00"},
            {"deployment": "deploy3", "status": "success", "timestamp": "2025-06-24T15:00:00"},
            {"deployment": "deploy4", "status": "success", "timestamp": "2025-06-27T18:45:00"},
        ]

    def get_deployment_frequency(self, days=30):
        now = datetime.now()
        threshold = now - timedelta(days=days)
        recent = [
            d for d in self.deployments
            if datetime.fromisoformat(d["timestamp"]) >= threshold
        ]
        return len(recent)

    def get_failure_rate(self):
        if not self.deployments:
            return 0.0
        failed = [d for d in self.deployments if d["status"].lower() == "failed"]
        return (len(failed) / len(self.deployments)) * 100

    def save_to_file(self, output_path="data_collection/deployment_metrics.json"):
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(self.deployments, f, indent=4)
        print(f"✅ Simulated deployment data saved to {output_path}")

# Only run this block when executing the script directly
if __name__ == "__main__":
    collector = DeploymentDataCollector()
    print("📦 Deployment Frequency (last 30 days):", collector.get_deployment_frequency())
    print("❌ Change Failure Rate (%):", collector.get_failure_rate())
    collector.save_to_file()
