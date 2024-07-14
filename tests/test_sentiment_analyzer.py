import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from src.AIAppReviewAnalyzer.components.sentiment_analyzer import analyze_sentiment, get_sentiment_summary

class TestSentimentAnalyzer(unittest.TestCase):

    @patch('AIAppReviewAnalyzer.components.sentiment_analyzer.pipeline')
    def test_analyze_sentiment(self, mock_pipeline):
        # Mock the sentiment analysis pipeline
        mock_nlp = MagicMock()
        mock_nlp.return_value = [
            {'label': 'POSITIVE', 'score': 0.9},
            {'label': 'NEGATIVE', 'score': 0.8}
        ]
        mock_pipeline.return_value = mock_nlp

        # Create a sample DataFrame
        df = pd.DataFrame({
            'content': ['Great app!', 'Terrible experience']
        })

        # Call the function
        result = analyze_sentiment(df)

        # Assert the results
        self.assertEqual(len(result), 2)
        self.assertEqual(result['sentiment'].tolist(), ['POSITIVE', 'NEGATIVE'])
        self.assertEqual(result['sentiment_score'].tolist(), [0.9, 0.8])

    def test_get_sentiment_summary(self):
        # Create a sample DataFrame
        df = pd.DataFrame({
            'sentiment': ['POSITIVE', 'NEGATIVE', 'POSITIVE', 'NEUTRAL']
        })

        # Call the function
        result = get_sentiment_summary(df)

        # Assert the results
        self.assertEqual(result.loc['POSITIVE', 'Count'], 2)
        self.assertEqual(result.loc['NEGATIVE', 'Count'], 1)
        self.assertEqual(result.loc['NEUTRAL', 'Count'], 1)
        self.assertAlmostEqual(result.loc['POSITIVE', 'Percentage'], 50.0)
        self.assertAlmostEqual(result.loc['NEGATIVE', 'Percentage'], 25.0)
        self.assertAlmostEqual(result.loc['NEUTRAL', 'Percentage'], 25.0)

if __name__ == '__main__':
    unittest.main()