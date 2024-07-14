from google_play_scraper import Sort, reviews
import pandas as pd
from tqdm import tqdm


def scrape_app_reviews(app_id, reviews_count=1000):
    result = []
    continuation_token = None

    with tqdm(total=reviews_count, position=0, leave=True) as pbar:
        while len(result) < reviews_count:
            new_result, continuation_token = reviews(
                app_id,
                continuation_token=continuation_token,
                lang='en',
                country='us',
                sort=Sort.NEWEST,
                count=500
            )
            if not new_result:
                break
            result.extend(new_result)
            pbar.update(len(new_result))

    df = pd.DataFrame(result)

    # Select relevant columns
    df = df[['reviewId', 'userName', 'content', 'score', 'reviewCreatedVersion', 'at', 'appVersion']]

    return df


def scrape_multiple_apps(app_ids, reviews_per_app=1000):
    all_reviews = {}
    for app_id in app_ids:
        print(f"Scraping reviews for app: {app_id}")
        app_reviews = scrape_app_reviews(app_id, reviews_per_app)
        all_reviews[app_id] = app_reviews
    return all_reviews


if __name__ == "__main__":
    # Example usage
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

    results = scrape_multiple_apps(app_ids)
    for app_id, df in results.items():
        print(f"App: {app_id}, Reviews scraped: {len(df)}")