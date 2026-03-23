# Week 3: Introduction to Sentiment Analysis

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import movie_reviews
import random

# Download required data
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('movie_reviews')

print("=== Week 3: Introduction to Sentiment Analysis ===\n")

# 1. BUILDING A SENTIMENT WORD DICTIONARY
print("1. SENTIMENT WORD DICTIONARY")
print("-" * 50)

# Positive words
positive_words = [
    'good', 'great', 'excellent', 'amazing', 'wonderful',
    'fantastic', 'awesome', 'love', 'best', 'perfect',
    'beautiful', 'brilliant', 'outstanding', 'superb', 'enjoyable'
]

# Negative words
negative_words = [
    'bad', 'terrible', 'awful', 'horrible', 'worst',
    'hate', 'disappointing', 'poor', 'waste', 'boring',
    'annoying', 'frustrating', 'ugly', 'useless', 'pathetic'
]

print("Positive words:", len(positive_words))
print("Negative words:", len(negative_words))
print()

# 2. COUNTING SENTIMENT WORDS
print("2. COUNTING SENTIMENT WORDS")
print("-" * 50)

review = "This game is great! I love the graphics. The story is amazing."

# Tokenize and lowercase
tokens = word_tokenize(review.lower())

# Count positive and negative words
positive_count = 0
negative_count = 0

for token in tokens:
    if token in positive_words:
        positive_count += 1
    if token in negative_words:
        negative_count += 1

print("Review:", review)
print("Positive words found:", positive_count)
print("Negative words found:", negative_count)
print()

# 3. CALCULATING SENTIMENT SCORES
print("3. CALCULATING SENTIMENT SCORES")
print("-" * 50)

# Calculate sentiment score
sentiment_score = positive_count - negative_count

print("Sentiment score:", sentiment_score)

# Classify the sentiment
if sentiment_score > 0:
    classification = "Positive"
elif sentiment_score < 0:
    classification = "Negative"
else:
    classification = "Neutral"

print("Classification:", classification)
print()

# 4. COMPLETE SENTIMENT ANALYZER FUNCTION
print("4. COMPLETE SENTIMENT ANALYZER")
print("-" * 50)

def analyze_sentiment(text):
    """Analyze sentiment of text using word counting"""
    
    # Define sentiment word lists
    positive_words = [
        'good', 'great', 'excellent', 'amazing', 'wonderful',
        'fantastic', 'awesome', 'love', 'best', 'perfect',
        'beautiful', 'brilliant', 'outstanding', 'superb', 'enjoyable'
    ]
    
    negative_words = [
        'bad', 'terrible', 'awful', 'horrible', 'worst',
        'hate', 'disappointing', 'poor', 'waste', 'boring',
        'annoying', 'frustrating', 'ugly', 'useless', 'pathetic'
    ]
    
    # Tokenize and lowercase
    tokens = word_tokenize(text.lower())
    
    # Count sentiment words
    positive_count = sum(1 for token in tokens if token in positive_words)
    negative_count = sum(1 for token in tokens if token in negative_words)
    
    # Calculate score
    sentiment_score = positive_count - negative_count
    
    # Classify
    if sentiment_score > 0:
        classification = "Positive"
    elif sentiment_score < 0:
        classification = "Negative"
    else:
        classification = "Neutral"
    
    return {
        'score': sentiment_score,
        'classification': classification,
        'positive_words': positive_count,
        'negative_words': negative_count
    }

# Test the function
review1 = "This game is amazing! I love it."
review2 = "Terrible game. Waste of money."
review3 = "The game is okay."

print("Review 1:", review1)
print("Analysis:", analyze_sentiment(review1))
print()

print("Review 2:", review2)
print("Analysis:", analyze_sentiment(review2))
print()

print("Review 3:", review3)
print("Analysis:", analyze_sentiment(review3))
print()

# 5. TESTING ON MOVIE REVIEWS DATASET
print("5. TESTING ON REAL MOVIE REVIEWS")
print("-" * 50)

# Get a random positive review
pos_fileid = random.choice(movie_reviews.fileids('pos'))
pos_text = movie_reviews.raw(pos_fileid)

# Get a random negative review
neg_fileid = random.choice(movie_reviews.fileids('neg'))
neg_text = movie_reviews.raw(neg_fileid)

# Analyze both
print("=== POSITIVE REVIEW ===")
print("First 200 characters:", pos_text[:200])
print("Our analysis:", analyze_sentiment(pos_text))
print("Actual label: Positive")
print()

print("=== NEGATIVE REVIEW ===")
print("First 200 characters:", neg_text[:200])
print("Our analysis:", analyze_sentiment(neg_text))
print("Actual label: Negative")
print()

# 6. CHECKING ACCURACY
print("6. ACCURACY TESTING")
print("-" * 50)

# Test on first 100 positive reviews
correct = 0
total = 0

for fileid in movie_reviews.fileids('pos')[:100]:
    text = movie_reviews.raw(fileid)
    result = analyze_sentiment(text)
    if result['classification'] == 'Positive':
        correct += 1
    total += 1

accuracy_positive = (correct / total) * 100
print(f"Accuracy on positive reviews: {accuracy_positive:.1f}%")

# Test on first 100 negative reviews
correct = 0
total = 0

for fileid in movie_reviews.fileids('neg')[:100]:
    text = movie_reviews.raw(fileid)
    result = analyze_sentiment(text)
    if result['classification'] == 'Negative':
        correct += 1
    total += 1

accuracy_negative = (correct / total) * 100
print(f"Accuracy on negative reviews: {accuracy_negative:.1f}%")

overall_accuracy = (accuracy_positive + accuracy_negative) / 2
print(f"Overall accuracy: {overall_accuracy:.1f}%")
print()

# 7. ADDING DOMAIN-SPECIFIC WORDS
print("7. EXPANDING WITH GAMING VOCABULARY")
print("-" * 50)

# Gaming-specific positive words
gaming_positive = [
    'addictive', 'immersive', 'engaging', 'polished', 'smooth',
    'fun', 'exciting', 'thrilling', 'impressive', 'stunning'
]

# Gaming-specific negative words
gaming_negative = [
    'buggy', 'glitchy', 'broken', 'laggy', 'repetitive',
    'clunky', 'unfinished', 'unplayable', 'crashes', 'boring'
]

# Combine with original lists
all_positive = positive_words + gaming_positive
all_negative = negative_words + gaming_negative

print("Total positive words:", len(all_positive))
print("Total negative words:", len(all_negative))
print()

print("=== Week 3 Complete! ===")
print("You've built your first sentiment analyzer!")
print("Next week: VADER sentiment analysis and handling context")