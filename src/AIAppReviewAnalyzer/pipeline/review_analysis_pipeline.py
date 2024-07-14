from src.AIAppReviewAnalyzer.components.scraper import scrape_multiple_apps
from src.AIAppReviewAnalyzer.components.sentiment_analyzer import analyze_sentiment, get_sentiment_summary
import pandas as pd

class ReviewAnalysisPipeline:
    def __init__(self, app_ids, reviews_per_app=1000):
        self.app_ids = app_ids
        self.reviews_per_app = reviews_per_app
        self.app_reviews = {}
        self.sentiment_results = {}
        self.sentiment_summaries = {}

    def run(self):
        self._scrape_reviews()
        self._analyze_sentiment()
        self._summarize_sentiment()
        return self.sentiment_summaries

    def _scrape_reviews(self):
        print("Scraping reviews...")
        self.app_reviews = scrape_multiple_apps(self.app_ids, self.reviews_per_app)

    def _analyze_sentiment(self):
        print("Analyzing sentiment...")
        for app_id, reviews_df in self.app_reviews.items():
            self.sentiment_results[app_id] = analyze_sentiment(reviews_df)

    def _summarize_sentiment(self):
        print("Summarizing sentiment...")
        for app_id, sentiment_df in self.sentiment_results.items():
            self.sentiment_summaries[app_id] = get_sentiment_summary(sentiment_df)

    def get_all_reviews(self):
        return self.app_reviews

    def get_sentiment_results(self):
        return self.sentiment_results

    def get_sentiment_summaries(self):
        return self.sentiment_summaries

if __name__ == "__main__":
    app_ids = [
        'com.openai.chatgpt',
        'com.google.android.apps.bard',
        'com.microsoft.copilot',
        'com.microsoft.bing',
        'com.codespaceapps.aichat',
        'ai.chat.gpt.bot',
        'ai.perplexity.app.android',
        'com.mlink.ai.chat.assistant.robot',
        'co.appnation.geniechat'
    ]

    pipeline = ReviewAnalysisPipeline(app_ids)
    results = pipeline.run()

    for app_id, summary in results.items():
        print(f"\nSentiment Summary for {app_id}:")
        print(summary)