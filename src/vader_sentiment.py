# Week 4: VADER Sentiment Analysis

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import movie_reviews

# Download required data
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('movie_reviews')

print("=== Week 4: VADER Sentiment Analysis ===\n")

# 1. SETTING UP VADER
print("1. SETTING UP VADER")
print("-" * 50)

sia = SentimentIntensityAnalyzer()
print("VADER is ready!")
print()

# 2. UNDERSTANDING VADER SCORES
print("2. UNDERSTANDING VADER SCORES")
print("-" * 50)

text = "This game is good."
scores = sia.polarity_scores(text)

print("Text:", text)
print("Scores:", scores)
print()
print("Score Breakdown:")
print(f"  Negative: {scores['neg']}")
print(f"  Neutral: {scores['neu']}")
print(f"  Positive: {scores['pos']}")
print(f"  Compound: {scores['compound']}")
print()

# 3. HANDLING NEGATIONS
print("3. HANDLING NEGATIONS")
print("-" * 50)

sentences = [
    "This game is good.",
    "This game is not good.",
    "This game is not bad.",
    "I don't hate this game."
]

for sentence in sentences:
    scores = sia.polarity_scores(sentence)
    compound = scores['compound']
    
    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    print(f"Text: {sentence}")
    print(f"Compound: {compound:.3f} → {sentiment}")
    print()

# 4. HANDLING EMPHASIS AND PUNCTUATION
print("4. HANDLING EMPHASIS AND PUNCTUATION")
print("-" * 50)

emphasis_tests = [
    "This game is good",
    "This game is GOOD",
    "This game is good!",
    "This game is GOOD!",
    "This game is GOOD!!!",
    "This game is gooood"
]

for text in emphasis_tests:
    compound = sia.polarity_scores(text)['compound']
    print(f"{text:30} → Compound: {compound:.3f}")
print()

# 5. HANDLING DEGREE MODIFIERS
print("5. HANDLING DEGREE MODIFIERS")
print("-" * 50)

modifiers = [
    "The game is good.",
    "The game is very good.",
    "The game is extremely good.",
    "The game is somewhat good.",
    "The game is barely good."
]

for text in modifiers:
    compound = sia.polarity_scores(text)['compound']
    print(f"{text:35} → {compound:.3f}")
print()

# 6. COMPLETE VADER ANALYZER FUNCTION
print("6. COMPLETE VADER ANALYZER FUNCTION")
print("-" * 50)

def analyze_sentiment_vader(text):
    """Analyze sentiment using VADER"""
    
    sia = SentimentIntensityAnalyzer()
    scores = sia.polarity_scores(text)
    
    # Get compound score
    compound = scores['compound']
    
    # Classify based on compound score
    if compound >= 0.05:
        classification = "Positive"
    elif compound <= -0.05:
        classification = "Negative"
    else:
        classification = "Neutral"
    
    return {
        'compound': compound,
        'classification': classification,
        'positive': scores['pos'],
        'neutral': scores['neu'],
        'negative': scores['neg']
    }

# Test the function
test_reviews = [
    "This game is absolutely AMAZING!!!",
    "Terrible game. Complete waste of money.",
    "The game is okay, nothing special.",
    "Not bad, but not great either."
]

for review in test_reviews:
    result = analyze_sentiment_vader(review)
    print(f"Review: {review}")
    print(f"Result: {result['classification']} (compound: {result['compound']:.3f})")
    print()

# 7. COMPARING BASIC VS VADER ANALYZERS
print("7. BASIC VS VADER COMPARISON")
print("-" * 60)

# Our basic analyzer from Week 3
def analyze_sentiment_basic(text):
    positive_words = ['good', 'great', 'excellent', 'amazing', 'love']
    negative_words = ['bad', 'terrible', 'awful', 'hate', 'worst']
    
    tokens = word_tokenize(text.lower())
    pos_count = sum(1 for token in tokens if token in positive_words)
    neg_count = sum(1 for token in tokens if token in negative_words)
    
    score = pos_count - neg_count
    if score > 0:
        return "Positive"
    elif score < 0:
        return "Negative"
    else:
        return "Neutral"

# VADER analyzer
def analyze_vader(text):
    compound = sia.polarity_scores(text)['compound']
    if compound >= 0.05:
        return "Positive"
    elif compound <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Tricky test cases
tricky_reviews = [
    "This game is not good.",
    "The game is AMAZING!!!",
    "I really, really love this game!",
    "It's not terrible.",
    "Very bad game."
]

print("Basic vs VADER Comparison")
print("=" * 60)
for review in tricky_reviews:
    basic = analyze_sentiment_basic(review)
    vader = analyze_vader(review)
    match = "✓" if basic == vader else "✗"
    print(f"Review: {review}")
    print(f"  Basic: {basic:8} | VADER: {vader:8} {match}")
    print()

# 8. TESTING VADER ON MOVIE REVIEWS
print("8. VADER ACCURACY ON MOVIE REVIEWS")
print("-" * 50)

# Test on positive reviews
correct_pos = 0
total_pos = 100

for fileid in movie_reviews.fileids('pos')[:total_pos]:
    text = movie_reviews.raw(fileid)
    compound = sia.polarity_scores(text)['compound']
    if compound >= 0.05:
        correct_pos += 1

# Test on negative reviews
correct_neg = 0
total_neg = 100

for fileid in movie_reviews.fileids('neg')[:total_neg]:
    text = movie_reviews.raw(fileid)
    compound = sia.polarity_scores(text)['compound']
    if compound <= -0.05:
        correct_neg += 1

# Calculate accuracy
accuracy_pos = (correct_pos / total_pos) * 100
accuracy_neg = (correct_neg / total_neg) * 100
overall = (correct_pos + correct_neg) / (total_pos + total_neg) * 100

print("VADER Accuracy on Movie Reviews:")
print(f"  Positive reviews: {accuracy_pos:.1f}%")
print(f"  Negative reviews: {accuracy_neg:.1f}%")
print(f"  Overall accuracy: {overall:.1f}%")
print()

# 9. GAME REVIEW ANALYSIS
print("9. GAME REVIEW SENTIMENT ANALYSIS")
print("-" * 70)

game_reviews = [
    "This game is absolutely incredible! The graphics are STUNNING and gameplay is super smooth. Highly recommend!!!",
    "Buggy mess. Game crashes every 10 minutes. Not worth the money at all.",
    "It's okay. Graphics are decent but gameplay gets repetitive after a while. Not bad but not great.",
    "I didn't think I would like this game, but I was wrong! It's actually pretty fun.",
    "WORST GAME EVER! Total waste of time and money. Extremely disappointing."
]

for i, review in enumerate(game_reviews, 1):
    result = analyze_sentiment_vader(review)
    print(f"Review {i}: {review[:60]}...")
    print(f"Sentiment: {result['classification']}")
    print(f"Compound Score: {result['compound']:.3f}")
    print(f"Positive: {result['positive']:.2f} | Neutral: {result['neutral']:.2f} | Negative: {result['negative']:.2f}")
    print()

print("=== Week 4 Complete! ===")
print("VADER is much more accurate than basic word counting!")
print("Next week: Analyzing multiple reviews and building reports")