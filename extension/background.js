// background.js - connects Steam reviews to Flask sentiment API
console.log("Background script loaded");

// Listen for messages from content script and others
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log("Message received in background:", request);

  // When content.js finishes fetching reviews from Steam
  if (request.action === "reviewsFetched") {
    console.log("Processing reviews for game:", request.gameId);
    console.log("Number of reviews:", request.reviews.length);
    console.log("Summary:", request.summary);

    // Extract plain text from the Steam review objects
    const reviewTexts = request.reviews.map((review) => review.review || "");
    console.log("Review texts extracted:", reviewTexts.length);

    // Call your Flask backend for sentiment analysis
    fetch("http://127.0.0.1:5001/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ reviews: reviewTexts })
    })
      .then((res) => res.json())
      .then((analysis) => {
        console.log("Sentiment analysis received from Flask:", analysis);

        // Forward combined data (Steam summary + sentiment report) to popup
        chrome.runtime
          .sendMessage({
            action: "reviewsAnalyzed",
            data: {
              // Original Steam info
              reviews: request.reviews,
              summary: request.summary,

              // New sentiment info from your Flask Week 5 logic
              report: analysis.report,        // overall stats
              perReview: analysis.per_review  // each review's sentiment
            }
          })
          .catch((err) => {
            // Popup might not be open, that's fine
            console.log("Popup not open:", err);
          });

        // Tell the sender (content script) that we succeeded
        sendResponse({ success: true });
      })
      .catch((err) => {
        console.error("Error calling Flask /analyze:", err);

        chrome.runtime
          .sendMessage({
            action: "analysisFailed",
            error: "Sentiment analysis failed. Is the Flask server running?"
          })
          .catch((e) => {
            console.log("Popup not open:", e);
          });

        sendResponse({ success: false });
      });

    // Keep the message channel open for the async fetch
    return true;
  }

  // Default: just keep the listener happy
  return true;
});