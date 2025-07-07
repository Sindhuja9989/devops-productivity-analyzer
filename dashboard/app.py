from flask import Flask, render_template
import json
import os
import sys

# Add parent directory to module path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from bottleneck_detection.bottleneck_detector import BottleneckDetector
from recommendation_engine.recommendation_engine import RecommendationEngine

app = Flask(__name__)

@app.route('/')
def index():
    # Load PR metrics
    pr_metrics_path = os.path.join("workflow_analysis", "pr_metrics.json")
    if os.path.exists(pr_metrics_path):
        with open(pr_metrics_path, "r") as f:
            pr_metrics = json.load(f)
    else:
        pr_metrics = {"review_times": [], "merge_frequency": 0, "stale_prs": []}

    # Load deployment metrics
    deployment_metrics_path = os.path.join("data_collection", "deployment_metrics.json")
    if os.path.exists(deployment_metrics_path):
        with open(deployment_metrics_path, "r") as f:
            deployment_data = json.load(f)
    else:
        deployment_data = []

    # Simulated commit/deploy frequency (for bottleneck detection)
    commit_data = [('2025-07-01', 5), ('2025-07-02', 3)]
    deployment_summary = [('2025-07-01', 2), ('2025-07-02', 1)]

    # Generate recommendations
    detector = BottleneckDetector(commit_data, deployment_data)  # ✅ Correct
    engine = RecommendationEngine(detector)
    recommendations = engine.generate_recommendations(pr_metrics.get("review_times", []))


    return render_template(
        "index.html",
        pr_metrics=pr_metrics,
        deployment_data=deployment_data,
        recommendations=recommendations
    )

if __name__ == '__main__':
    app.run(debug=True)
