# Week 2: Text Analysis & Statistics

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, movie_reviews
from collections import Counter
import string
import random

# Make sure data is downloaded
nltk.download('movie_reviews')
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')

print("=== Week 2: Text Analysis & Statistics ===\n")

# 1. WORD FREQUENCY ANALYSIS
print("1. WORD FREQUENCY ANALYSIS")
print("-" * 50)

review = "This game is amazing! The graphics are amazing and the gameplay is amazing too. I love the amazing story."

# Preprocess the text
tokens = word_tokenize(review.lower())
tokens = [token for token in tokens if token not in string.punctuation]
stop_words = set(stopwords.words('english'))
tokens = [token for token in tokens if token not in stop_words]

# Count word frequencies
word_freq = Counter(tokens)
print("Review:", review)
print("Word frequencies:", word_freq)
print("Most common words:", word_freq.most_common(3))
print()

# 2. REVIEW LENGTH ANALYSIS
print("2. REVIEW LENGTH ANALYSIS")
print("-" * 50)

review1 = "Great game! Love it."
review2 = "This game has amazing graphics, incredible gameplay, and a fantastic story that keeps you engaged for hours."

tokens1 = word_tokenize(review1)
tokens2 = word_tokenize(review2)

print("Review 1:", review1)
print("Review 1 length:", len(tokens1), "tokens")
print("\nReview 2:", review2)
print("Review 2 length:", len(tokens2), "tokens")
print()

# 3. UNIQUE WORD COUNT (VOCABULARY RICHNESS)
print("3. VOCABULARY RICHNESS")
print("-" * 50)

review = "The game is good. The graphics are good. The gameplay is good too."
tokens = word_tokenize(review.lower())
tokens = [token for token in tokens if token.isalpha()]

total_words = len(tokens)
unique_words = len(set(tokens))
vocabulary_richness = unique_words / total_words

print("Review:", review)
print("Total words:", total_words)
print("Unique words:", unique_words)
print("Vocabulary richness:", round(vocabulary_richness, 2))
print()

# 4. AVERAGE WORD LENGTH
print("4. AVERAGE WORD LENGTH")
print("-" * 50)

tokens = ['amazing', 'good', 'incredible', 'ok']
avg_length = sum(len(word) for word in tokens) / len(tokens)

print("Words:", tokens)
print("Average word length:", round(avg_length, 2), "characters")
print()

# 5. LOADING MOVIE REVIEWS DATASET
print("5. MOVIE REVIEWS DATASET")
print("-" * 50)

positive_reviews = movie_reviews.fileids('pos')
negative_reviews = movie_reviews.fileids('neg')

print("Total positive reviews:", len(positive_reviews))
print("Total negative reviews:", len(negative_reviews))

random_pos_id = random.choice(positive_reviews)
pos_review_text = movie_reviews.raw(random_pos_id)
print("\nSample positive review (first 200 chars):")
print(pos_review_text[:200])
print()

# 6. ANALYZING A SINGLE REVIEW
print("6. SINGLE REVIEW ANALYSIS")
print("-" * 50)

review_id = movie_reviews.fileids('pos')[0]
review_text = movie_reviews.raw(review_id)

# Preprocess
tokens = word_tokenize(review_text.lower())
tokens = [t for t in tokens if t not in string.punctuation]
stop_words = set(stopwords.words('english'))
filtered_tokens = [t for t in tokens if t not in stop_words]

print("Review ID:", review_id)
print("Total tokens:", len(tokens))
print("After removing stop words:", len(filtered_tokens))
print("Unique words:", len(set(filtered_tokens)))
print("\nTop 5 most common words:")
word_freq = Counter(filtered_tokens)
for word, count in word_freq.most_common(5):
    print(f"  {word}: {count}")
print()

# 7. COMPARING POSITIVE VS NEGATIVE REVIEWS - LENGTH
print("7. AVERAGE REVIEW LENGTH BY SENTIMENT")
print("-" * 50)

# Analyze positive reviews
pos_lengths = []
for fileid in movie_reviews.fileids('pos')[:100]:
    tokens = word_tokenize(movie_reviews.raw(fileid))
    tokens = [t for t in tokens if t not in string.punctuation]
    pos_lengths.append(len(tokens))

# Analyze negative reviews
neg_lengths = []
for fileid in movie_reviews.fileids('neg')[:100]:
    tokens = word_tokenize(movie_reviews.raw(fileid))
    tokens = [t for t in tokens if t not in string.punctuation]
    neg_lengths.append(len(tokens))

avg_pos_length = sum(pos_lengths) / len(pos_lengths)
avg_neg_length = sum(neg_lengths) / len(neg_lengths)

print("Average positive review length:", round(avg_pos_length, 2), "words")
print("Average negative review length:", round(avg_neg_length, 2), "words")
print()

# 8. MOST COMMON WORDS IN POSITIVE VS NEGATIVE
print("8. TOP WORDS BY SENTIMENT")
print("-" * 50)

def get_top_words(category, num_reviews=100):
    """Get most common words for a category"""
    all_tokens = []
    stop_words = set(stopwords.words('english'))
    
    for fileid in movie_reviews.fileids(category)[:num_reviews]:
        tokens = word_tokenize(movie_reviews.raw(fileid).lower())
        tokens = [t for t in tokens if t not in string.punctuation]
        tokens = [t for t in tokens if t not in stop_words]
        all_tokens.extend(tokens)
    
    return Counter(all_tokens).most_common(10)

print("Top 10 words in POSITIVE reviews:")
for word, count in get_top_words('pos'):
    print(f"  {word}: {count}")

print("\nTop 10 words in NEGATIVE reviews:")
for word, count in get_top_words('neg'):
    print(f"  {word}: {count}")
print()

# 9. COMPLETE ANALYSIS FUNCTION
print("9. COMPLETE ANALYSIS FUNCTION")
print("-" * 50)

def analyze_review(review_text):
    """Complete analysis of a single review"""
    # Preprocess
    tokens = word_tokenize(review_text.lower())
    tokens_no_punct = [t for t in tokens if t not in string.punctuation]
    stop_words = set(stopwords.words('english'))
    filtered_tokens = [t for t in tokens_no_punct if t not in stop_words]
    
    # Calculate statistics
    total_words = len(tokens_no_punct)
    unique_words = len(set(filtered_tokens))
    vocab_richness = unique_words / total_words if total_words > 0 else 0
    avg_word_length = sum(len(w) for w in filtered_tokens) / len(filtered_tokens) if filtered_tokens else 0
    
    # Get top words
    word_freq = Counter(filtered_tokens)
    top_words = word_freq.most_common(5)
    
    # Return analysis
    return {
        'total_words': total_words,
        'unique_words': unique_words,
        'vocabulary_richness': round(vocab_richness, 2),
        'avg_word_length': round(avg_word_length, 2),
        'top_words': top_words
    }

sample = "This game is absolutely amazing! The graphics are stunning and the gameplay is fantastic."
analysis = analyze_review(sample)

print("Sample review:", sample)
print("\nReview Analysis:")
for key, value in analysis.items():
    print(f"  {key}: {value}")
print()

# 10. PRACTICE EXERCISE
print("10. PRACTICE EXERCISE - COMPARE REVIEWS")
print("-" * 50)

pos_review = movie_reviews.raw(movie_reviews.fileids('pos')[0])
neg_review = movie_reviews.raw(movie_reviews.fileids('neg')[0])

pos_analysis = analyze_review(pos_review)
neg_analysis = analyze_review(neg_review)

print("Positive Review Analysis:")
for key, value in pos_analysis.items():
    print(f"  {key}: {value}")

print("\nNegative Review Analysis:")
for key, value in neg_analysis.items():
    print(f"  {key}: {value}")
print()

print("=== Week 2 Complete! ===")
print("Next week: Introduction to sentiment analysis!")