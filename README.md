# AI ChatBot Benchmarker

This project analyzes the sentiment of user reviews for various AI chat applications available on the Google Play Store. It provides insights into user satisfaction and compares sentiment across different apps.

## Features

- Scrapes reviews from the Google Play Store
- Performs sentiment analysis on the reviews
- Generates a comparative analysis across multiple AI chat apps
- Provides an interactive dashboard for visualizing the results

## Screenshot from Dash App

[![capture-20240714173200842.png](https://i.postimg.cc/SRt34FT4/capture-20240714173200842.png)](https://postimg.cc/BPHM5yf7)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yusufeneskorkmaz/AIChatBotBenchmarker.git
   ```

2. Create a virtual environment and activate it:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -e .
   ```

## Usage

1. Run the main script:
   ```
   python src/AIAppReviewAnalyzer/main.py
   ```

2. Open a web browser and navigate to `http://127.0.0.1:8050/` to view the dashboard.

## Project Structure

- `src/AIAppReviewAnalyzer/`: Main package directory
  - `components/`: Core components (scraper, sentiment analyzer)
  - `pipeline/`: Analysis pipeline
  - `dashboard/`: Dash app for visualization
  - `utils/`: Utility functions
  - `config/`: Configuration files
- `tests/`: Unit tests
- `main.py`: Entry point of the application
- `setup.py`: Setup script for the package
- `requirements.txt`: List of Python dependencies

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
