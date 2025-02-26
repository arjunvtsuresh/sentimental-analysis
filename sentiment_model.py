from transformers import pipeline

# Load the sentiment analysis model
sentiment_analyzer = pipeline("sentiment-analysis")

def analyze_sentiment(text: str) -> str:
    result = sentiment_analyzer(text)[0]
    return result['label']
