# ⚡ TaskChain AI — Hackathon Setup Guide

## Files
```
index.html       ← Person 1's file (Frontend)
app.py           ← Person 2's file (Backend)
TaskLogger.sol   ← Optional: real Solidity contract
README.md        ← This file
```

---

## 🚀 Running in 5 Minutes

### Person 2 — Start the Backend First

```bash
# 1. Install dependencies (once)
pip install flask flask-cors

# 2. Run the server
python app.py
```

You should see:
```
TaskChain AI Backend — Running on port 5000
  POST /analyze
  POST /log_blockchain
  GET  /ledger
```

Test it works:
```bash
curl http://localhost:5000/health
# → {"status": "ok", "service": "TaskChain AI Backend"}
```

---

### Person 1 — Open the Frontend

```bash
# Just open index.html in your browser
# On Mac:
open index.html

# On Windows:
start index.html

# Or drag index.html into Chrome/Firefox
```

> ⚠️ Make sure the backend is running before clicking Analyze!

---

## 🧪 Test Inputs to Demo

| Message | Expected Result |
|---|---|
| "I have an urgent issue with my account" | High / Support |
| "What's the price of your premium plan?" | Medium / Sales |
| "Just wanted to say hello!" | Low / General |
| "URGENT: payment broken, need fix asap" | High / Support |
| "Can you give me a discount on the annual plan?" | Medium / Sales |

---

## 👥 Team Division of Work

### Person 1 — Frontend (index.html)
**Time: ~2.5 hours**

| Task | Time |
|---|---|
| HTML structure + layout | 30 min |
| CSS styling + dark theme | 45 min |
| Analyze button + API call | 30 min |
| Display AI results (badges, reply box) | 30 min |
| Log to Blockchain button + TX display | 30 min |
| Activity log + polish | 15 min |

**Files to edit:** `index.html` only
**Key code:** `analyze()` and `logToChain()` functions in `<script>`

---

### Person 2 — Backend (app.py)
**Time: ~2.5 hours**

| Task | Time |
|---|---|
| Flask setup + CORS | 20 min |
| Keyword AI engine | 45 min |
| Reply templates | 30 min |
| Blockchain simulation | 40 min |
| API routes + testing | 30 min |
| (Optional) Solidity contract | 30 min |

**Files to edit:** `app.py` (and optionally `TaskLogger.sol`)
**Key code:** `analyze_message()` and `simulate_blockchain_log()` functions

---

## 🔌 API Reference

### POST /analyze
```json
Request:  { "message": "I have an urgent billing issue" }
Response: {
  "priority": "High",
  "category": "Support",
  "confidence": 87,
  "suggested_reply": "Thank you for reaching out urgently...",
  "keywords_detected": 3
}
```

### POST /log_blockchain
```json
Request:  { "message": "...", "priority": "High", "category": "Support" }
Response: {
  "tx_hash": "0xabc123...",
  "block_number": 10042,
  "network": "Shardeum Testnet (simulated)",
  "gas_used": "21,000",
  "timestamp": 1700000000
}
```

### GET /ledger
Returns all logged transactions (useful for demo).

---

## 🔗 Optional: Real Shardeum Integration

1. Open [remix.ethereum.org](https://remix.ethereum.org)
2. Paste `TaskLogger.sol`
3. Compile + Deploy to Shardeum Sphinx Testnet
   - RPC: `https://sphinx.shardeum.org/`
   - Chain ID: `8082`
4. Replace `simulate_blockchain_log()` in `app.py` with `web3.py` calls

---

## 🎯 Demo Flow (for judges)

1. Type a customer message in the textarea
2. Click **Analyze** — AI detects priority, category, suggests reply
3. Click **Log to Blockchain** — TX hash appears with block number
4. Check the **Session Log** at the bottom
5. (Bonus) Hit `GET /ledger` to show all stored entries

---

## 🐛 Common Issues

| Problem | Fix |
|---|---|
| CORS error in browser | Make sure `flask-cors` is installed and `app.py` is running |
| `fetch` fails | Check that backend is on port 5000 and running |
| Module not found | Run `pip install flask flask-cors` |
| Port 5000 in use | Change `port=5000` to `port=5001` in `app.py` AND update `API_BASE` in `index.html` |
