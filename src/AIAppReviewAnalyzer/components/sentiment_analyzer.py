import pandas as pd
from transformers import pipeline, DistilBertTokenizer, DistilBertForSequenceClassification


def initialize_sentiment_model():
    tokenizer = DistilBertTokenizer.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased-finetuned-sst-2-english")
    return pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)


def analyze_sentiment(df, text_column='content', batch_size=32):
    nlp = initialize_sentiment_model()

    texts = list(df[text_column].values)
    results = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        results.extend(nlp(batch))

    df['sentiment'] = [result['label'] for result in results]
    df['sentiment_score'] = [result['score'] for result in results]

    return df


def get_sentiment_summary(df):
    sentiment_counts = df['sentiment'].value_counts()
    sentiment_percentages = sentiment_counts / len(df) * 100

    summary_df = pd.DataFrame({
        'Count': sentiment_counts,
        'Percentage': sentiment_percentages
    })

    return summary_df


if __name__ == "__main__":
    # Example usage
    sample_df = pd.DataFrame({
        'content': [
            "This app is amazing!",
            "I hate this app, it's terrible.",
            "It's okay, could be better."
        ]
    })

    result_df = analyze_sentiment(sample_df)
    print(result_df)

    summary = get_sentiment_summary(result_df)
    print("\nSentiment Analysis Summary:")
    print(summary)