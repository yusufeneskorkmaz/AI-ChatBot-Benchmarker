import unittest
from unittest.mock import patch, MagicMock
from src.AIAppReviewAnalyzer.components.scraper import scrape_app_reviews, scrape_multiple_apps

class TestScraper(unittest.TestCase):

    @patch('AIAppReviewAnalyzer.components.scraper.reviews')
    def test_scrape_app_reviews(self, mock_reviews):
        # Mock the reviews function
        mock_reviews.return_value = (
            [
                {'reviewId': '1', 'userName': 'User1', 'content': 'Great app!', 'score': 5, 'reviewCreatedVersion': '1.0', 'at': '2023-01-01', 'appVersion': '1.0'},
                {'reviewId': '2', 'userName': 'User2', 'content': 'Needs improvement', 'score': 3, 'reviewCreatedVersion': '1.0', 'at': '2023-01-02', 'appVersion': '1.0'}
            ],
            None
        )

        # Call the function
        result = scrape_app_reviews('test.app.id', reviews_count=2)

        # Assert the results
        self.assertEqual(len(result), 2)
        self.assertEqual(result.iloc[0]['reviewId'], '1')
        self.assertEqual(result.iloc[1]['reviewId'], '2')

    @patch('AIAppReviewAnalyzer.components.scraper.scrape_app_reviews')
    def test_scrape_multiple_apps(self, mock_scrape_app_reviews):
        # Mock the scrape_app_reviews function
        mock_scrape_app_reviews.side_effect = [
            MagicMock(shape=(2, 7)),  # First app
            MagicMock(shape=(2, 7))   # Second app
        ]

        # Call the function
        app_ids = ['test.app.1', 'test.app.2']
        result = scrape_multiple_apps(app_ids, reviews_per_app=2)

        # Assert the results
        self.assertEqual(len(result), 2)
        self.assertIn('test.app.1', result)
        self.assertIn('test.app.2', result)
        self.assertEqual(mock_scrape_app_reviews.call_count, 2)

if __name__ == '__main__':
    unittest.main()