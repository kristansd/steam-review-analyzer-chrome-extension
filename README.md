# 🎮 Steam Review Analyzer

A Chrome extension that reads Steam game reviews and tells you how players actually feel about a game — using real NLP sentiment analysis, not just the thumbs up/down count.

Built over 5 weeks as part of an AI/NLP club project, starting from scratch with basic text processing and ending with a full working Chrome extension.

![icon](extension/icon17.png)

---

## What It Does

When you visit any Steam game page, the extension lets you click one button to:

- Fetch up to 50 recent player reviews from Steam's public API
- Send them to a local Python backend for sentiment analysis
- Display a full breakdown right in the popup — no page reload needed

### What You See After Analyzing

**Steam Stats**
- Total review count for the game
- How many reviews were fetched (sample size)
- Steam's own positive/negative counts

**VADER Sentiment Snapshot**
- An overall sentiment label: `POSITIVE`, `NEGATIVE`, or `MIXED`
- An average compound score from -1.0 (very negative) to +1.0 (very positive)
- A color-coded bar showing the split between positive, neutral, and negative reviews
- A tagline summarizing the vibe (e.g. *"Players are overwhelmingly happy with this title 💚"*)

**Sentiment Over Time Chart**
- A glowing line graph drawn on a canvas element
- Shows how sentiment shifts across reviews, sorted oldest to newest
- Green = trending up, Red = trending down, Yellow = stable

**Highlighted Reviews**
- Shows the top 3 reviews based on your selected sort
- Sort options: Most Positive, Most Negative, Newest, Oldest
- Each card shows the sentiment tag, compound score, review text, and whether the player recommended the game

---

## How It Works

```
Steam Game Page
      ↓
content.js fetches reviews from Steam's API
      ↓
background.js sends review text to Flask backend
      ↓
app.py runs VADER sentiment analysis on each review
      ↓
Results sent back → popup.js displays everything
```

The Python backend uses **NLTK's VADER** (Valence Aware Dictionary and sEntiment Reasoner), which is built specifically for short, informal text like reviews. It handles things like:
- ALL CAPS ("AMAZING!!!" scores higher than "amazing")
- Negations ("not bad" is treated as mildly positive)
- Punctuation emphasis ("great!!!" vs "great")
- Degree modifiers ("very good" vs "barely good")

---

## Project Structure

```
steam-review-analyzer/
│
├── README.md
├── requirements.txt
│
├── backend/
│   └── app.py                      # Flask server + VADER logic
│
├── extension/
│   ├── manifest.json               # Chrome extension config
│   ├── popup.html                  # Extension popup UI
│   ├── popup.js                    # Popup logic + charts
│   ├── background.js               # Connects Steam data to Flask
│   ├── content.js                  # Runs on Steam pages, fetches reviews
│   └── icon17.png                  # Extension icon
│
└── src/
    ├── nlp_preprocessing.py        # Week 1: tokenization, stopwords, cleaning
    ├── text_analysis.py            # Week 2: word frequency, vocabulary stats
    ├── basic_sentiment_analyzer.py # Week 3: manual word-count sentiment
    ├── vader_sentiment.py          # Week 4: VADER deep dive + comparisons
    └── sentiment_aggregator.py     # Week 5: multi-review reports + distributions
```

---

## Setup

### What You Need

- Python 3.8+
- Google Chrome
- A terminal

---

### Step 1 — Install Python dependencies

```bash
pip install flask flask-cors nltk
```

---

### Step 2 — Start the Flask backend

```bash
cd backend
python app.py
```

You should see:

```
* Running on http://127.0.0.1:5001
```

Leave this terminal open while using the extension.

---

### Step 3 — Load the extension in Chrome

1. Open Chrome and go to `chrome://extensions`
2. Turn on **Developer mode** (toggle in the top right)
3. Click **Load unpacked**
4. Select the `extension/` folder from this repo

The extension icon will appear in your toolbar.

---

### Step 4 — Use it

1. Go to any Steam game page (example: `https://store.steampowered.com/app/570` for Dota 2)
2. Click the extension icon
3. Hit **Analyze Reviews**
4. Results appear in a few seconds

---

## Changing the Flask Host or Port

By default the backend runs on `http://127.0.0.1:5001`.

**To change the port**, edit the last line of `backend/app.py`:

```python
app.run(host="127.0.0.1", port=5001, debug=True)
#                          ^^^^ change this
```

Then update `background.js` to match:

```javascript
fetch("http://127.0.0.1:5001/analyze", {  // ← update port here too
```

And update `manifest.json` under `host_permissions`:

```json
"http://127.0.0.1:5001/*"   ← update this line
```

---

## The Learning Path (src/ folder)

The `src/` folder shows how this project was built from the ground up over 5 weeks:

| File | What It Covers |
|------|---------------|
| `nlp_preprocessing.py` | Tokenization, lowercasing, stopword removal, punctuation cleaning |
| `text_analysis.py` | Word frequency, review length, vocabulary richness, top words by sentiment |
| `basic_sentiment_analyzer.py` | Manual positive/negative word lists, accuracy testing on real movie reviews |
| `vader_sentiment.py` | VADER setup, negation handling, caps/punctuation emphasis, basic vs VADER comparison |
| `sentiment_aggregator.py` | Multi-review reports, sentiment distribution, comparing multiple games |

Each file runs on its own and prints output to the terminal — good for seeing how each concept works step by step.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Chrome Extension | HTML, CSS, JavaScript (Manifest V3) |
| Sentiment Analysis | Python, NLTK VADER |
| Backend API | Flask, Flask-CORS |
| Steam Data | Steam Web API (public, no key needed) |
| Trend Chart | HTML Canvas (vanilla JS) |

---

## Requirements

```
flask
flask-cors
nltk
```

Install with:

```bash
pip install -r requirements.txt
```

NLTK data is downloaded automatically on first run.

---

## Notes

- The Flask server must be running locally for the extension to work
- Steam's API returns up to 50 recent reviews per request
- VADER works best on English reviews; other languages may score inaccurately
- This project uses Steam's **public** API — no Steam account or API key is required
