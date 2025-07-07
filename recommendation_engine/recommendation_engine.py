import json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bottleneck_detection.bottleneck_detector import BottleneckDetector

class RecommendationEngine:
    def __init__(self, bottleneck_detector):
        self.detector = bottleneck_detector

    def generate_recommendations(self, lead_times):
        recommendations = []

        # ⏱️ High lead time
        high_leads = self.detector.detect_high_lead_time(lead_times)
        if high_leads:
            recommendations.append("🧪 Optimize review/deployment pipeline — high lead time detected.")

        # ❌ Failure rate
        failure_rate = self.detector.detect_change_failure_rate()
        if failure_rate > 20:
            recommendations.append(f"🔧 Change failure rate is {failure_rate:.1f}% — improve test coverage or CI checks.")

        # ⚙️ Deployment vs Commit gap
        commit_count, deploy_count = self.detector.analyze_commit_vs_deployment()
        if deploy_count < commit_count:
            recommendations.append("⚙️ Deployment frequency lags behind commits — automate deploy triggers.")

        if commit_count == 0:
            recommendations.append("📉 No commit activity — consider reviewing developer workflows.")

        return recommendations

if __name__ == "__main__":
    # Load deployment data
    with open("data_collection/deployment_metrics.json") as f:
        deployments = json.load(f)

    # Simulated data (you can load real commit data if you want)
    commit_data = [("2025-06-20", 5), ("2025-06-22", 3), ("2025-06-24", 2)]
    lead_times = [{"commit": "abc123", "lead_time": 30}, {"commit": "def456", "lead_time": 10}]

    detector = BottleneckDetector(commit_data, deployments)
    engine = RecommendationEngine(detector)

    print("📋 Final Recommendations:")
    for rec in engine.generate_recommendations(lead_times):
        print("-", rec)
