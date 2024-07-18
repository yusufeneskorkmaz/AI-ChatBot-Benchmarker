from src.AIAppReviewAnalyzer.pipeline.review_analysis_pipeline import ReviewAnalysisPipeline
from src.AIAppReviewAnalyzer.dashboard.app import app as dashboard_app

def main():
    # Define the app IDs
    app_ids = [
        'com.openai.chatgpt',
        'com.anthropic.claude'
        'com.google.android.apps.bard',
        'com.microsoft.copilot',
        'com.microsoft.bing',
        'com.codespaceapps.aichat',
        'ai.chat.gpt.bot',
        'ai.perplexity.app.android',
        'com.mlink.ai.chat.assistant.robot',
        'co.appnation.geniechat'
    ]

    # Run the analysis pipeline
    pipeline = ReviewAnalysisPipeline(app_ids)
    results = pipeline.run()

    # Print summary results
    for app_id, summary in results.items():
        print(f"\nSentiment Summary for {app_id}:")
        print(summary)

    # Run the dashboard
    dashboard_app.run_server(debug=True)

if __name__ == "__main__":
    main()