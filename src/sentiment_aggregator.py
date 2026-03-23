# Week 5: Aggregating Sentiment & Chrome Extension Basics

import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.corpus import movie_reviews

# Download required data
nltk.download('vader_lexicon')
nltk.download('movie_reviews')
nltk.download('punkt')
nltk.download('punkt_tab')

print("=== Week 5: Aggregating Sentiment ===\n")

# 1. ANALYZING MULTIPLE REVIEWS
print("1. ANALYZING MULTIPLE REVIEWS")
print("-" * 50)

sia = SentimentIntensityAnalyzer()

# Sample game reviews
reviews = [
    "Amazing game! Love the graphics and gameplay.",
    "Pretty good, but has some bugs.",
    "Terrible experience. Waste of money.",
    "Not bad, could be better.",
    "BEST GAME EVER!!! Highly recommended!!!"
]

# Analyze each review
results = []
for review in reviews:
    scores = sia.polarity_scores(review)
    compound = scores['compound']
    
    if compound >= 0.05:
        sentiment = "Positive"
    elif compound <= -0.05:
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    results.append({
        'text': review,
        'compound': compound,
        'sentiment': sentiment
    })

# Display results
for i, result in enumerate(results, 1):
    print(f"Review {i}: {result['text']}")
    print(f"  Sentiment: {result['sentiment']} (compound: {result['compound']:.3f})")
    print()

# 2. CALCULATING OVERALL SENTIMENT
print("2. CALCULATING OVERALL SENTIMENT")
print("-" * 50)

reviews = [
    "Amazing game! Love the graphics.",
    "Pretty good, but has some bugs.",
    "Terrible experience.",
    "Not bad, could be better.",
    "BEST GAME EVER!!!"
]

# Collect all compound scores
compound_scores = []
for review in reviews:
    compound = sia.polarity_scores(review)['compound']
    compound_scores.append(compound)

# Calculate average
average_compound = sum(compound_scores) / len(compound_scores)

# Determine overall sentiment
if average_compound >= 0.05:
    overall_sentiment = "Positive"
elif average_compound <= -0.05:
    overall_sentiment = "Negative"
else:
    overall_sentiment = "Mixed/Neutral"

print(f"Total reviews: {len(reviews)}")
print(f"Average compound score: {average_compound:.3f}")
print(f"Overall sentiment: {overall_sentiment}")
print()

# 3. SENTIMENT DISTRIBUTION
print("3. SENTIMENT DISTRIBUTION")
print("-" * 50)

reviews = [
    "Amazing game! Love it.",
    "Pretty good game.",
    "Terrible experience.",
    "Not bad.",
    "BEST GAME EVER!!!",
    "Awful game.",
    "It's okay.",
    "Great graphics!",
    "Worst game.",
    "Decent game."
]

# Count sentiments
positive_count = 0
negative_count = 0
neutral_count = 0

for review in reviews:
    compound = sia.polarity_scores(review)['compound']
    
    if compound >= 0.05:
        positive_count += 1
    elif compound <= -0.05:
        negative_count += 1
    else:
        neutral_count += 1

# Calculate percentages
total = len(reviews)
positive_pct = (positive_count / total) * 100
negative_pct = (negative_count / total) * 100
neutral_pct = (neutral_count / total) * 100

print("Sentiment Distribution:")
print(f"  Positive: {positive_count} ({positive_pct:.1f}%)")
print(f"  Negative: {negative_count} ({negative_pct:.1f}%)")
print(f"  Neutral: {neutral_count} ({neutral_pct:.1f}%)")
print()

# 4. COMPLETE SENTIMENT REPORT FUNCTION
print("4. COMPLETE SENTIMENT REPORT FUNCTION")
print("-" * 50)

def generate_sentiment_report(reviews):
    """Generate comprehensive sentiment report"""
    
    sia = SentimentIntensityAnalyzer()
    
    # Analyze each review
    all_scores = []
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    for review in reviews:
        compound = sia.polarity_scores(review)['compound']
        all_scores.append(compound)
        
        if compound >= 0.05:
            positive_count += 1
        elif compound <= -0.05:
            negative_count += 1
        else:
            neutral_count += 1
    
    # Calculate statistics
    total = len(reviews)
    avg_score = sum(all_scores) / total
    max_score = max(all_scores)
    min_score = min(all_scores)
    
    # Determine overall sentiment
    if avg_score >= 0.05:
        overall = "Positive"
    elif avg_score <= -0.05:
        overall = "Negative"
    else:
        overall = "Mixed"
    
    return {
        'total_reviews': total,
        'average_score': round(avg_score, 3),
        'overall_sentiment': overall,
        'positive_count': positive_count,
        'negative_count': negative_count,
        'neutral_count': neutral_count,
        'positive_percentage': round((positive_count / total) * 100, 1),
        'negative_percentage': round((negative_count / total) * 100, 1),
        'neutral_percentage': round((neutral_count / total) * 100, 1),
        'highest_score': round(max_score, 3),
        'lowest_score': round(min_score, 3)
    }

# Test with sample reviews
sample_reviews = [
    "Amazing game!",
    "Pretty good.",
    "Terrible.",
    "Okay game.",
    "LOVE IT!!!",
    "Awful.",
    "Not bad.",
    "Great!",
    "Worst ever.",
    "Decent."
]

report = generate_sentiment_report(sample_reviews)

print("Sentiment Report:")
print("=" * 50)
for key, value in report.items():
    print(f"{key}: {value}")
print()

# 5. TESTING ON REAL MOVIE REVIEWS
print("5. TESTING ON REAL MOVIE REVIEWS")
print("-" * 50)

# Analyze first 50 positive reviews
positive_reviews_text = []
for fileid in movie_reviews.fileids('pos')[:50]:
    text = movie_reviews.raw(fileid)
    positive_reviews_text.append(text)

# Generate report for positive reviews
pos_report = generate_sentiment_report(positive_reviews_text)

print("Analysis of 50 Positive Movie Reviews:")
print(f"Average score: {pos_report['average_score']}")
print(f"Overall sentiment: {pos_report['overall_sentiment']}")
print(f"Correctly identified as positive: {pos_report['positive_percentage']}%")
print()

# Analyze first 50 negative reviews
negative_reviews_text = []
for fileid in movie_reviews.fileids('neg')[:50]:
    text = movie_reviews.raw(fileid)
    negative_reviews_text.append(text)

# Generate report for negative reviews
neg_report = generate_sentiment_report(negative_reviews_text)

print("Analysis of 50 Negative Movie Reviews:")
print(f"Average score: {neg_report['average_score']}")
print(f"Overall sentiment: {neg_report['overall_sentiment']}")
print(f"Correctly identified as negative: {neg_report['negative_percentage']}%")
print()

# 6. COMPARING DIFFERENT GAMES
print("6. COMPARING DIFFERENT GAMES (SIMULATED)")
print("-" * 50)

game1_reviews = [
    "Amazing game! Love it!",
    "Great graphics and gameplay.",
    "Best game I've played!",
    "Pretty good overall.",
    "Decent game."
]

game2_reviews = [
    "Terrible game.",
    "Waste of money.",
    "Awful experience.",
    "Not worth it.",
    "Very disappointing."
]

game3_reviews = [
    "It's okay.",
    "Not bad, not great.",
    "Average game.",
    "Could be better.",
    "Mediocre at best."
]

print("Game 1 Report:")
game1_report = generate_sentiment_report(game1_reviews)
print(f"  Overall: {game1_report['overall_sentiment']} (avg: {game1_report['average_score']})")
print(f"  Distribution: {game1_report['positive_percentage']}% pos, {game1_report['negative_percentage']}% neg")
print()

print("Game 2 Report:")
game2_report = generate_sentiment_report(game2_reviews)
print(f"  Overall: {game2_report['overall_sentiment']} (avg: {game2_report['average_score']})")
print(f"  Distribution: {game2_report['positive_percentage']}% pos, {game2_report['negative_percentage']}% neg")
print()

print("Game 3 Report:")
game3_report = generate_sentiment_report(game3_reviews)
print(f"  Overall: {game3_report['overall_sentiment']} (avg: {game3_report['average_score']})")
print(f"  Distribution: {game3_report['positive_percentage']}% pos, {game3_report['negative_percentage']}% neg")
print()

print("=== Week 5 Complete! ===")
print("You can now aggregate sentiment from multiple reviews!")
print("Next: Chrome extension integration with real Steam reviews")