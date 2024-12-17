from collections import Counter
import math, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ResponseAnalyzer:
    def __init__(self):
        self.responses : list = []
        self.response_groups : list = []
        self.ripple : float = 0.0
        self.consim : float = 0.0

    def group_responses(self):
        response_counts = Counter(self.responses)
        self.response_groups = list(response_counts.values())

    def calculate_metrics(self):
        total_responses = sum(self.response_groups)
        largest_group = max(self.response_groups)
        
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(self.responses)
        cosine_similarities = cosine_similarity(tfidf_matrix)
        np.fill_diagonal(cosine_similarities, 0)
        total_similarity = np.sum(np.triu(cosine_similarities, k=1))
        num_comparisons = cosine_similarities.shape[0] * (cosine_similarities.shape[0] - 1) / 2

        self.ripple = largest_group / total_responses
        self.consim = total_similarity / num_comparisons if num_comparisons else 0
    