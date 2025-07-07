import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from data_collection.data_collector import DataCollector

class WorkflowAnalyzer:
    def __init__(self, repo_path):
        self.collector = DataCollector(repo_path)

    def analyze_commit_frequency(self, days=30):
        commit_counts = []
        for i in range(days):
            end_date = datetime.now() - timedelta(days=i)
            start_date = end_date - timedelta(days=1)
            commits = list(self.collector.repo.iter_commits(since=start_date, until=end_date))
            commit_counts.append((start_date.strftime("%Y-%m-%d"), len(commits)))
        return list(reversed(commit_counts))

    def analyze_deployment_frequency(self, deployments):
        deployment_counts = []
        for i in range(30):
            date = datetime.now() - timedelta(days=i)
            count = len([d for d in deployments if d.date() == date.date()])
            deployment_counts.append((date.strftime("%Y-%m-%d"), count))
        return list(reversed(deployment_counts))

    def visualize_data(self, commit_data, deployment_data):
        dates_commit, counts_commit = zip(*commit_data)
        dates_deploy, counts_deploy = zip(*deployment_data)

        plt.figure(figsize=(12, 6))
        plt.plot(dates_commit, counts_commit, label='Commit Frequency', marker='o')
        plt.plot(dates_deploy, counts_deploy, label='Deployment Frequency', marker='x')
        plt.xlabel('Date')
        plt.ylabel('Frequency')
        plt.title('Commit and Deployment Frequency Over Time')
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        plt.show()

if __name__ == "__main__":
    repo_path = r"C:\Users\karnakar reddy\Desktop\devops-productivity-analyzer\devops-productivity-analyzer"
    analyzer = WorkflowAnalyzer(repo_path)

    commit_data = analyzer.analyze_commit_frequency()

    deployments = [
        datetime.now() - timedelta(days=3),
        datetime.now() - timedelta(days=7),
        datetime.now() - timedelta(days=10),
    ]

    deployment_data = analyzer.analyze_deployment_frequency(deployments)
    analyzer.visualize_data(commit_data, deployment_data)
