# Week 1: NLP Fundamentals for Sentiment Analysis

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import string

# Download required NLTK data packages
nltk.download("movie_reviews")
nltk.download('vader_lexicon')
nltk.download('punkt')
nltk.download("punkt_tab")
nltk.download('stopwords')

print("=== Week 1: NLP Preprocessing Techniques ===\n")

# 1. TOKENIZATION EXAMPLE
print("1. TOKENIZATION")
print("-" * 30)

text = "This game is absolutely amazing! I love the graphics and gameplay."
tokens = word_tokenize(text)
print("Original text:", text)
print("Tokens:", tokens)
print()

# 2. LOWERCASING EXAMPLE
print("2. LOWERCASING")
print("-" * 30)

text = "The GRAPHICS are Amazing and the gameplay is EXCELLENT!"
tokens = word_tokenize(text)

# Before lowercasing
print("Original tokens:", tokens)

# After lowercasing
lowercase_tokens = [token.lower() for token in tokens]
print("Lowercase tokens:", lowercase_tokens)
print()

# 3. STOP WORDS REMOVAL EXAMPLE
print("3. STOP WORDS REMOVAL")
print("-" * 30)

# Get English stop words
stop_words = set(stopwords.words('english'))
print("Sample stop words:", list(stop_words)[:10])

# Example text
text = "The game is really good and I think the graphics are amazing"
tokens = word_tokenize(text.lower())

# Remove stop words
filtered_tokens = [token for token in tokens if token not in stop_words]

print("Original tokens:", tokens)
print("After removing stop words:", filtered_tokens)
print()

# 4. PUNCTUATION REMOVAL EXAMPLE
print("4. PUNCTUATION REMOVAL")
print("-" * 30)

text = "This game is amazing!!! The graphics are top-notch, and the story is incredible."
tokens = word_tokenize(text.lower())

# Remove punctuation
no_punct_tokens = [token for token in tokens if token not in string.punctuation]

print("Original tokens:", tokens)
print("After removing punctuation:", no_punct_tokens)
print("Punctuation characters:", string.punctuation)
print()

# 5. COMPLETE PREPROCESSING PIPELINE
print("5. COMPLETE PREPROCESSING PIPELINE")
print("-" * 30)

def preprocess_text(text):
    """Complete text preprocessing pipeline"""
    # Step 1: Tokenize
    tokens = word_tokenize(text)
    
    # Step 2: Convert to lowercase
    tokens = [token.lower() for token in tokens]
    
    # Step 3: Remove punctuation
    tokens = [token for token in tokens if token not in string.punctuation]
    
    # Step 4: Remove stop words
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]
    
    return tokens

# Test the complete pipeline
review_text = "This game is absolutely incredible! The graphics are stunning and the gameplay is super engaging. I highly recommend it to everyone!"

original_tokens = word_tokenize(review_text)
processed_tokens = preprocess_text(review_text)

print("Original text:", review_text)
print("Original tokens:", original_tokens)
print("Processed tokens:", processed_tokens)
print()

# 6. PRACTICE EXERCISE
print("6. PRACTICE EXERCISE")
print("-" * 30)

practice_review = "OMG!!! This game is SO BAD. The controls are terrible, the story makes no sense, and I wasted my money. Don't buy this game!"

print("Practice review:", practice_review)
print("Processed tokens:", preprocess_text(practice_review))
print()
