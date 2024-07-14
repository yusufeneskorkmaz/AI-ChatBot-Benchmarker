from setuptools import setup, find_packages

setup(
    name="AIAppReviewAnalyzer",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "google-play-scraper",
        "pandas",
        "numpy",
        "matplotlib",
        "seaborn",
        "dash",
        "plotly",
        "transformers",
        "torch",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "analyze-reviews=AIAppReviewAnalyzer.main:main",
        ],
    },
    author="yusufeneskorkmaz",
    author_email="yusufeneskorkmaz@outlook.com",
    description="A tool for analyzing sentiment of AI chat app reviews from Google Play Store",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yusufeneskorkmaz/AIAppReviewAnalyzer",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)