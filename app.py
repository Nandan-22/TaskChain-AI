# app.py — TaskChain AI Backend
# Person 2's file: Flask + AI logic + Blockchain simulation
# Run: pip install flask flask-cors && python app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
import hashlib
import time
import random
import string

app = Flask(__name__)
CORS(app)  # Allow frontend to call this API

# ─────────────────────────────────────────────────────────
# AI LOGIC — Keyword-based analysis engine
# ─────────────────────────────────────────────────────────

PRIORITY_KEYWORDS = {
    "High":   ["urgent", "asap", "immediately", "critical", "emergency",
               "broken", "down", "not working", "blocked", "serious"],
    "Medium": ["soon", "issue", "problem", "error", "trouble", "concern",
               "confused", "wrong", "delay", "missing"],
    "Low":    ["whenever", "just wondering", "curious", "maybe", "eventually",
               "question", "general", "info", "hello", "hi"]
}

CATEGORY_KEYWORDS = {
    "Sales":   ["price", "pricing", "cost", "buy", "purchase", "discount",
                "offer", "deal", "plan", "subscription", "upgrade", "demo",
                "trial", "quote", "invoice", "payment", "refund"],
    "Support": ["issue", "problem", "error", "not working", "broken",
                "bug", "crash", "failed", "wrong", "help", "stuck",
                "can't", "cannot", "doesn't work", "trouble", "fix"],
}

REPLY_TEMPLATES = {
    ("High", "Support"): (
        "Thank you for reaching out urgently. We understand this is critical "
        "and our support team is escalating your case immediately. "
        "You will hear from us within the next 30 minutes."
    ),
    ("High", "Sales"): (
        "Thank you for your interest! Given the urgency, I'm connecting you "
        "directly with a senior sales rep right now. Expect a call within the hour."
    ),
    ("High", "General"): (
        "We've received your urgent message and it's been flagged as high priority. "
        "Our team will respond within the next hour."
    ),
    ("Medium", "Support"): (
        "Thank you for contacting us about this issue. We've logged your case "
        "and our support team will investigate and follow up within 24 hours."
    ),
    ("Medium", "Sales"): (
        "Thanks for your inquiry! Our sales team will review your request "
        "and get back to you with a tailored offer within 1–2 business days."
    ),
    ("Medium", "General"): (
        "Thanks for reaching out! We've received your message and will "
        "respond with the relevant information within 1–2 business days."
    ),
    ("Low", "Support"): (
        "Thank you for getting in touch. We'll look into your query and "
        "provide a response within 3–5 business days."
    ),
    ("Low", "Sales"): (
        "Thank you for your interest in our products! We'll send over "
        "relevant information and pricing details soon."
    ),
    ("Low", "General"): (
        "Hi there! Thanks for your message. We'll get back to you shortly "
        "with the information you need. Have a great day!"
    ),
}


def analyze_message(message: str) -> dict:
    """Keyword-based AI analysis of a customer message."""
    msg_lower = message.lower()

    # --- Detect Priority ---
    priority = "Low"
    priority_score = 0
    for level, keywords in PRIORITY_KEYWORDS.items():
        hits = sum(1 for kw in keywords if kw in msg_lower)
        if level == "High" and hits > priority_score:
            priority_score = hits
            if hits > 0:
                priority = "High"
        elif level == "Medium" and hits > 0 and priority == "Low":
            priority = "Medium"
            priority_score = hits

    # --- Detect Category ---
    category = "General"
    cat_scores = {}
    for cat, keywords in CATEGORY_KEYWORDS.items():
        cat_scores[cat] = sum(1 for kw in keywords if kw in msg_lower)

    best_cat = max(cat_scores, key=cat_scores.get)
    if cat_scores[best_cat] > 0:
        category = best_cat

    # --- Confidence score (fake but realistic) ---
    total_signals = sum(cat_scores.values()) + priority_score
    confidence = min(95, 55 + (total_signals * 8) + random.randint(0, 5))

    # --- Suggested Reply ---
    suggested_reply = REPLY_TEMPLATES.get(
        (priority, category),
        REPLY_TEMPLATES[("Low", "General")]
    )

    return {
        "priority": priority,
        "category": category,
        "confidence": confidence,
        "suggested_reply": suggested_reply,
        "keywords_detected": total_signals
    }


# ─────────────────────────────────────────────────────────
# BLOCKCHAIN SIMULATION
# Real Shardeum integration can replace this section.
# ─────────────────────────────────────────────────────────

# In-memory ledger (simulates a blockchain)
blockchain_ledger = []


def generate_tx_hash(data: str) -> str:
    """Generate a realistic-looking transaction hash."""
    seed = data + str(time.time()) + ''.join(random.choices(string.ascii_letters, k=8))
    return "0x" + hashlib.sha256(seed.encode()).hexdigest()


def simulate_blockchain_log(message: str, priority: str, category: str) -> dict:
    """
    Simulates logging to a blockchain.
    To use real Shardeum:
      1. Deploy the Solidity contract (TaskLogger.sol)
      2. Use web3.py to call the contract's logTask() function
      3. Return the real tx hash and block number
    """
    message_hash = "0x" + hashlib.sha256(message.encode()).hexdigest()
    tx_hash = generate_tx_hash(message + priority + category)
    block_number = len(blockchain_ledger) + 10000 + random.randint(1, 99)

    entry = {
        "tx_hash": tx_hash,
        "message_hash": message_hash,
        "priority": priority,
        "category": category,
        "timestamp": int(time.time()),
        "block_number": block_number,
        "network": "Shardeum Testnet (simulated)",
        "gas_used": f"{random.randint(21000, 45000):,}"
    }

    blockchain_ledger.append(entry)
    return entry


# ─────────────────────────────────────────────────────────
# API ROUTES
# ─────────────────────────────────────────────────────────

@app.route('/analyze', methods=['POST'])
def analyze():
    """POST /analyze — Runs AI analysis on a customer message."""
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    message = data['message'].strip()
    if not message:
        return jsonify({"error": "Message cannot be empty"}), 400

    result = analyze_message(message)
    return jsonify(result), 200


@app.route('/log_blockchain', methods=['POST'])
def log_blockchain():
    """POST /log_blockchain — Logs analysis result to (simulated) blockchain."""
    data = request.get_json()
    if not data or not all(k in data for k in ['message', 'priority', 'category']):
        return jsonify({"error": "Missing required fields"}), 400

    entry = simulate_blockchain_log(
        message=data['message'],
        priority=data['priority'],
        category=data['category']
    )
    return jsonify(entry), 200


@app.route('/ledger', methods=['GET'])
def ledger():
    """GET /ledger — View all logged blockchain entries (debug)."""
    return jsonify({
        "total_entries": len(blockchain_ledger),
        "entries": blockchain_ledger
    }), 200


@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "TaskChain AI Backend"}), 200


# ─────────────────────────────────────────────────────────
if __name__ == '__main__':
    print("=" * 50)
    print("  TaskChain AI Backend — Running on port 5000")
    print("  Endpoints:")
    print("    POST /analyze")
    print("    POST /log_blockchain")
    print("    GET  /ledger")
    print("    GET  /health")
    print("=" * 50)
    app.run(debug=True, port=5000)
