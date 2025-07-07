class BottleneckDetector:
       def __init__(self, commit_data, deployment_data):
           self.commit_data = commit_data
           self.deployment_data = deployment_data

       def detect_high_lead_time(self, lead_times):
           high_lead_time_commits = [commit for commit in lead_times if commit['lead_time'] > 24]  # Example threshold
           return high_lead_time_commits

       def detect_change_failure_rate(self, failure_data):
           total_deployments = len(failure_data)
           failed_deployments = sum(1 for result in failure_data if result['status'] == 'failed')
           failure_rate = (failed_deployments / total_deployments) * 100 if total_deployments > 0 else 0
           return failure_rate

       def analyze_commit_vs_deployment(self):
           commit_counts = [count for _, count in self.commit_data]
           deployment_counts = [count for _, count in self.deployment_data]
           discrepancies = [(commit, deploy) for commit, deploy in zip(commit_counts, deployment_counts) if commit > deploy]
           return discrepancies

if __name__ == "__main__":
       commit_data = [('2023-10-01', 5), ('2023-10-02', 3), ('2023-10-03', 2)]
       deployment_data = [('2023-10-01', 2), ('2023-10-02', 1), ('2023-10-03', 1)]
       lead_times = [{'commit': 'abc123', 'lead_time': 30}, {'commit': 'def456', 'lead_time': 10}]
       failure_data = [{'deployment': 'deploy1', 'status': 'success'}, {'deployment': 'deploy2', 'status': 'failed'}]

       detector = BottleneckDetector(commit_data, deployment_data)
       high_lead_time_commits = detector.detect_high_lead_time(lead_times)
       failure_rate = detector.detect_change_failure_rate(failure_data)
       discrepancies = detector.analyze_commit_vs_deployment()

       print("High Lead Time Commits:", high_lead_time_commits)
       print("Change Failure Rate (%):", failure_rate)
       print("Commit vs Deployment Discrepancies:", discrepancies)
   