// Popup script - handles the extension popup UI

let currentGameId = null;

let sentimentState = {
  perReviewWithMeta: []
};

// When popup opens, check if we're on a Steam game page
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const currentTab = tabs[0];

  if (currentTab && currentTab.url) {
    const url = currentTab.url;
    const match = url.match(/\/app\/(\d+)/);

    if (match) {
      currentGameId = match[1];
      document.getElementById("gameId").textContent = currentGameId;
      document.getElementById("gameInfo").style.display = "block";
      document.getElementById("analyzeBtn").disabled = false;
      document.getElementById("status").textContent = "Ready to analyze reviews";
      document.getElementById("status").className = "status waiting";

      // Try to get game name from Steam API
      fetchGameName(currentGameId);
    } else {
      showError("Not on a Steam game page");
    }
  }
});

// Fetch game name from Steam API
async function fetchGameName(gameId) {
  try {
    const response = await fetch(
      `https://store.steampowered.com/api/appdetails?appids=${gameId}`
    );
    const data = await response.json();

    if (data[gameId] && data[gameId].success) {
      const gameName = data[gameId].data.name;
      document.getElementById("gameName").textContent = gameName;
    }
  } catch (error) {
    console.error("Error fetching game name:", error);
    document.getElementById("gameName").textContent = "Unknown Game";
  }
}

// Handle analyze button click
document.getElementById("analyzeBtn").addEventListener("click", () => {
  if (!currentGameId) return;

  // UI to analyzing state
  const statusEl = document.getElementById("status");
  statusEl.innerHTML =
    '<span class="loading"></span> Fetching reviews & running sentiment analysis…';
  statusEl.className = "status analyzing";
  document.getElementById("analyzeBtn").disabled = true;

  // Ask content script to fetch reviews for this game
  chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    if (!tabs[0]) return;

    chrome.tabs.sendMessage(
      tabs[0].id,
      { action: "analyzeReviews", gameId: currentGameId },
      () => {
        const err = chrome.runtime.lastError;
        if (err) {
          console.warn("sendMessage warning:", err.message);
        }
      }
    );
  });
});

// Listen for messages from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  console.log("Popup received message:", request);

  if (request.action === "reviewsAnalyzed") {
    displayResults(request.data);
  } else if (request.action === "analysisFailed") {
    showError(request.error);
  }

  return true;
});

// Display results in popup
function displayResults(data) {
  const statusEl = document.getElementById("status");
  statusEl.textContent = "✓ Analysis Complete!";
  statusEl.className = "status complete";
  document.getElementById("analyzeBtn").disabled = false;

  // --- Steam stats ---
  document.getElementById("totalReviews").textContent =
    data.summary.total_reviews ?? "-";
  document.getElementById("fetchedReviews").textContent =
    (data.reviews && data.reviews.length) || "-";
  document.getElementById("positiveCount").textContent =
    data.summary.total_positive ?? "-";
  document.getElementById("negativeCount").textContent =
    data.summary.total_negative ?? "-";

  document.getElementById("results").classList.add("visible");

  // --- VADER sentiment from Flask ---
  const report = data.report;
  if (!report) {
    console.warn("No sentiment report found in data:", data);
    return;
  }

  // Core text fields
  document.getElementById("overallSentiment").textContent =
    report.overall_sentiment;
  document.getElementById("avgScore").textContent =
    report.average_score.toFixed(3);

  const countsText = `${report.positive_count} positive · ${report.neutral_count} neutral · ${report.negative_count} negative`;
  document.getElementById("sentimentCounts").textContent = countsText;

  // Percent labels
  document.getElementById("posPctLabel").textContent =
    report.positive_percentage + "%";
  document.getElementById("neuPctLabel").textContent =
    report.neutral_percentage + "%";
  document.getElementById("negPctLabel").textContent =
    report.negative_percentage + "%";

  // Bar widths
  document.getElementById("barPos").style.width =
    report.positive_percentage + "%";
  document.getElementById("barNeu").style.width =
    report.neutral_percentage + "%";
  document.getElementById("barNeg").style.width =
    report.negative_percentage + "%";

  // Badge styling
  const badge = document.getElementById("sentimentBadge");
  badge.classList.remove("positive", "negative", "mixed");

  if (report.overall_sentiment === "Positive") {
    badge.classList.add("positive");
    badge.textContent = "POSITIVE";
  } else if (report.overall_sentiment === "Negative") {
    badge.classList.add("negative");
    badge.textContent = "Negative".toUpperCase();
  } else {
    badge.classList.add("mixed");
    badge.textContent = "MIXED";
  }

    // Fun tagline based on average score + spread
  const taglineEl = document.getElementById("sentimentTagline");
  const avg = report.average_score;
  const pos = report.positive_percentage;
  const neg = report.negative_percentage;

  if (avg > 0.6 && pos > 70) {
    taglineEl.textContent =
      "Players are overwhelmingly happy with this title 💚";
  } else if (avg < -0.3 && neg > 50) {
    taglineEl.textContent = "Warning: reviews are strongly negative 💔";
  } else if (Math.abs(avg) < 0.1) {
    taglineEl.textContent =
      "Community is split — this game is pretty divisive 🎭";
  } else {
    taglineEl.textContent =
      "Mixed feedback with a slight lean — scroll reviews for details.";
  }

  // --- Build per-review state with metadata for top reviews section ---
  const per = data.perReview || [];
  const rawReviews = data.reviews || [];

  sentimentState.perReviewWithMeta = per.map((r, index) => {
    const raw = rawReviews[index] || {};
    return {
      text: r.text,
      compound: r.compound,
      sentiment: r.sentiment,
      pos: r.pos,
      neu: r.neu,
      neg: r.neg,
      timestamp: raw.timestamp_created || null,
      voted_up: raw.voted_up,
      votes_up: raw.votes_up,
      votes_down: raw.votes_down
    };
  });

  // Trend analysis: lifetime vs recent windows
  updateTrends(sentimentState.perReviewWithMeta);

  // Default view: top positive
  updateTopReviews("mostPositive");
  document.getElementById("reviewSort").value = "mostPositive";

  // Finally, reveal the whole sentiment block
  document.getElementById("sentimentResults").style.display = "block";
}

// Draw glowing sentiment trend line on canvas
function updateTrends(items) {
  const canvas = document.getElementById("trendCanvas");
  const dirEl = document.getElementById("trendDirection");

  if (!canvas || !dirEl) return;

  const ctx = canvas.getContext("2d");

  if (!items || !items.length) {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    dirEl.textContent = "Not enough data to compute trends.";
    dirEl.className = "trend-direction";
    return;
  }

  // Sort reviews by time (oldest → newest)
  const sorted = [...items].sort(
    (a, b) => (a.timestamp || 0) - (b.timestamp || 0)
  );

  // Sample down to at most 40 points so the line stays clean
  const maxPoints = 40;
  let points = sorted;
  if (sorted.length > maxPoints) {
    const step = sorted.length / maxPoints;
    points = [];
    for (let i = 0; i < maxPoints; i++) {
      const idx = Math.floor(i * step);
      points.push(sorted[idx]);
    }
  }

  const width = canvas.width;
  const height = canvas.height;
  const padding = 8;

  // Clear
  ctx.clearRect(0, 0, width, height);

  // Neutral midline (compound = 0)
  ctx.strokeStyle = "rgba(139,168,196,0.35)";
  ctx.lineWidth = 1;
  ctx.setLineDash([4, 4]);
  ctx.beginPath();
  ctx.moveTo(padding, height / 2);
  ctx.lineTo(width - padding, height / 2);
  ctx.stroke();
  ctx.setLineDash([]);

  // Determine trend direction from first → last point
  const start = points[0].compound;
  const end = points[points.length - 1].compound;
  const diff = end - start;

  let lineColor = "#3cf3a8"; // green
  let trendClass = "trend-direction positive";
  let trendText =
    "📈 Sentiment is trending upward compared to earlier reviews.";

  const IMPROVE_THRESH = 0.05;

  if (diff < -IMPROVE_THRESH) {
    lineColor = "#ff8c7a"; // red
    trendClass = "trend-direction negative";
    trendText =
      "📉 Sentiment is trending downward compared to earlier reviews.";
  } else if (Math.abs(diff) <= IMPROVE_THRESH) {
    lineColor = "#f9e076"; // yellow-ish
    trendClass = "trend-direction stable";
    trendText = "⚖️ Sentiment is relatively stable over the sampled reviews.";
  }

  // Map compound [-1, 1] to canvas y
  const minVal = -1;
  const maxVal = 1;

  const toXY = (p, idx, total) => {
    const x =
      padding +
      (total === 1 ? 0 : (idx / (total - 1)) * (width - 2 * padding));
    const norm = (p.compound - minVal) / (maxVal - minVal);
    const y =
      height - padding - norm * (height - 2 * padding); // invert y axis
    return { x, y };
  };

  // Draw glowing line
  ctx.lineWidth = 2;
  ctx.strokeStyle = lineColor;
  ctx.shadowBlur = 10;
  ctx.shadowColor = lineColor;

  ctx.beginPath();
  points.forEach((p, i) => {
    const { x, y } = toXY(p, i, points.length);
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.stroke();

  // Remove glow for future drawings
  ctx.shadowBlur = 0;

  // Caption under chart
  dirEl.className = trendClass;
  dirEl.textContent = trendText;
}

// Update the "Top reviews" section based on sort mode
function updateTopReviews(mode) {
  const container = document.getElementById("topReviewsList");
  container.innerHTML = "";

  const items = [...sentimentState.perReviewWithMeta];
  if (!items.length) {
    container.textContent = "No reviews available for highlights.";
    return;
  }

  // Sort copy based on selected mode
  if (mode === "mostPositive") {
    items.sort((a, b) => b.compound - a.compound);
  } else if (mode === "mostNegative") {
    items.sort((a, b) => a.compound - b.compound);
  } else if (mode === "newest") {
    items.sort((a, b) => (b.timestamp || 0) - (a.timestamp || 0));
  } else if (mode === "oldest") {
    items.sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0));
  }

  const top = items.slice(0, 3);

  top.forEach((item) => {
    const div = document.createElement("div");
    div.className = "review-item";

    const header = document.createElement("div");
    header.className = "review-item-header";

    const tag = document.createElement("span");
    tag.className = "review-item-tag";

    if (item.sentiment === "Positive") {
      tag.classList.add("pos");
      tag.textContent = "POSITIVE";
    } else if (item.sentiment === "Negative") {
      tag.classList.add("neg");
      tag.textContent = "NEGATIVE";
    } else {
      tag.classList.add("neu");
      tag.textContent = "NEUTRAL";
    }

    const score = document.createElement("span");
    score.className = "review-item-score";
    score.textContent = `Score: ${item.compound.toFixed(3)}`;

    header.appendChild(tag);
    header.appendChild(score);

    const text = document.createElement("div");
    text.className = "review-item-text";
    const shortText =
      item.text.length > 180 ? item.text.slice(0, 177) + "…" : item.text;
    text.textContent = `"${shortText}"`;

    const meta = document.createElement("div");
    meta.className = "review-item-meta";

    const recLabel =
      item.voted_up === true
        ? "Player verdict: 👍 Recommended"
        : item.voted_up === false
        ? "Player verdict: 👎 Not recommended"
        : "Player verdict: —";

    meta.textContent = recLabel;

    div.appendChild(header);
    div.appendChild(text);
    div.appendChild(meta);

    container.appendChild(div);
  });
}

// Show error message
function showError(errorMsg) {
  const statusEl = document.getElementById("status");
  statusEl.textContent = "✗ " + errorMsg;
  statusEl.className = "status error";
  document.getElementById("analyzeBtn").disabled = false;
}

// Change handler for sort dropdown
const sortSelect = document.getElementById("reviewSort");
if (sortSelect) {
  sortSelect.addEventListener("change", (e) => {
    updateTopReviews(e.target.value);
  });
}
