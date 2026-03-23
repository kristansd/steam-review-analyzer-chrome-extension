# app.py – Flask backend using your Week 5-style sentiment logic

from flask import Flask, request, jsonify
from flask_cors import CORS

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer

# --- NLTK setup (first run may download stuff) ---
nltk.download('vader_lexicon')
nltk.download('punkt')

app = Flask(__name__)
CORS(app)

# Create one global VADER analyzer (like Week 5)
sia = SentimentIntensityAnalyzer()


def generate_sentiment_report(reviews):
    """
    Week 5-style sentiment report + per-review details.
    This is adapted directly from your Week 5 file.
    """

    all_scores = []
    positive_count = 0
    negative_count = 0
    neutral_count = 0

    per_review = []

    for review in reviews:
        scores = sia.polarity_scores(review)
        compound = scores['compound']
        all_scores.append(compound)

        if compound >= 0.05:
            sentiment = "Positive"
            positive_count += 1
        elif compound <= -0.05:
            sentiment = "Negative"
            negative_count += 1
        else:
            sentiment = "Neutral"
            neutral_count += 1

        per_review.append({
            "text": review,
            "compound": round(compound, 3),
            "sentiment": sentiment,
            "pos": scores["pos"],
            "neu": scores["neu"],
            "neg": scores["neg"],
        })

    total = len(reviews) if reviews else 1
    avg_score = sum(all_scores) / total if all_scores else 0
    max_score = max(all_scores) if all_scores else 0
    min_score = min(all_scores) if all_scores else 0

    if avg_score >= 0.05:
        overall = "Positive"
    elif avg_score <= -0.05:
        overall = "Negative"
    else:
        overall = "Mixed"

    report = {
        "total_reviews": len(reviews),
        "average_score": round(avg_score, 3),
        "overall_sentiment": overall,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "neutral_count": neutral_count,
        "positive_percentage": round((positive_count / total) * 100, 1),
        "negative_percentage": round((negative_count / total) * 100, 1),
        "neutral_percentage": round((neutral_count / total) * 100, 1),
        "highest_score": round(max_score, 3),
        "lowest_score": round(min_score, 3),
    }

    return report, per_review


# --- Simple test routes (still useful) ---

@app.route("/")
def home():
    return "Flask server is running with sentiment analysis!"


@app.route("/ping")
def ping():
    return "pong"


# --- Main API your Chrome extension will call ---

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Expects JSON like:
    {
      "reviews": ["text 1", "text 2", ...]
    }
    Returns JSON with:
      - report: overall stats
      - per_review: list of each review's sentiment
    """
    data = request.get_json() or {}
    reviews = data.get("reviews", [])

    report, per_review = generate_sentiment_report(reviews)

    return jsonify({
        "report": report,
        "per_review": per_review
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001, debug=True)    
