from bottleneck_detection.bottleneck_detector import BottleneckDetector

class RecommendationEngine:
       def __init__(self, bottleneck_detector):
           self.detector = bottleneck_detector

       def generate_recommendations(self):
           recommendations = []
           if self.detector.detect_high_lead_time([]):  
               recommendations.append("Consider optimizing the review process to reduce lead times.")

           failure_rate = self.detector.detect_change_failure_rate([]) 
           if failure_rate > 20:  
               recommendations.append("Implement automated testing to reduce change failure rates.")

           discrepancies = self.detector.analyze_commit_vs_deployment()
           if discrepancies:
               recommendations.append("Increase deployment frequency to match commit frequency.")

           return recommendations

if __name__ == "__main__":
       commit_data = [('2023-10-01', 5), ('2023-10-02', 3), ('2023-10-03', 2)]
       deployment_data = [('2023-10-01', 2), ('2023-10-02', 1), ('2023-10-03', 1)]
       lead_times = [{'commit': 'abc123', 'lead_time': 30}, {'commit': 'def456', 'lead_time': 10}]
       failure_data = [{'deployment': 'deploy1', 'status': 'success'}, {'deployment': 'deploy2', 'status': 'failed'}]

       detector = BottleneckDetector(commit_data, deployment_data)
       recommendations = RecommendationEngine(detector).generate_recommendations()

       print("Recommendations:")
       for recommendation in recommendations:
           print("-", recommendation)
   