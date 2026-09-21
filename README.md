# Arcana — Financial Intelligence Web App

**A 24-hour hackathon project built by Shreyash Patidar & Hrishikesh at the Arcana Hackathon, IIT Madras TechSoc, 2023.**

Arcana was an early experiment in combining **market data, technical analysis, financial news, NLP, and AI summarization** into a single investor-facing web application.

### What We Built

- 📊 **Portfolio dashboard** — current and historical holdings
- 📈 **Stock analysis** — historical prices, moving averages and rolling volatility
- ⚠️ **Risk classification** — rule-based Low / Moderate / High risk signals
- 📰 **News sentiment** — financial headlines with TextBlob sentiment analysis
- 🤖 **Earnings intelligence** — transcript summarization using Cohere + sentiment analysis
- 🌐 **Market data APIs** — stock quotes, time series, indexes, tickers and stock metadata

### Architecture

```text
Market Data ────────┐
                    │
Financial News ─────┼──► Flask Backend ──► Investor Dashboard
                    │          │
Transcripts ────────┘          ├── Technical Analysis
                               ├── Risk Classification
                               ├── Sentiment Analysis
                               └── AI Summarization
```

### Tech Stack

**Python · Flask · Pandas · NumPy · BeautifulSoup · Requests · TextBlob · Cohere**

Historical financial data is primarily stored as CSV files and processed with Pandas. Financial news is retrieved from Finviz, while earnings transcripts are summarized through Cohere.

### Key Analytical Flow

For stock risk analysis, the application derives **20 / 50 / 100-period moving averages and rolling standard deviations**, then applies rule-based thresholds to classify volatility into Low, Moderate or High Risk.

For earnings transcripts:

```text
Transcript → Cohere Summary → TextBlob Sentiment → Investor Signal
```

### Hackathon Context

Arcana was built by a **two-person team within a 24-hour hackathon constraint**. The goal was to move quickly from financial-data exploration to a functioning web application combining multiple information sources.

IIT Madras's **2022–23 Annual Report** lists the Arcana Hackathon among TechSoc competitions.

### From Arcana to Later Work

Arcana was an early stepping stone in a broader exploration of computational finance:

```text
Arcana
   ↓
InvestmentGuide
   ↓
TradBot
   ↓
TradBot_v2
```

The later projects are **not part of this repository**. They represent subsequent evolution of ideas around financial research, automation and systematic trading.

### Repository Status

**Archived hackathon prototype · 2023**

This is a historical project rather than a production investment or trading platform.

> **Security note:** The archived source contains a hardcoded Cohere API credential. It must be revoked/rotated and replaced with an environment variable before public deployment.

### References

- [IIT Madras Annual Report 2022–23](https://www.iitm.ac.in/sites/default/files/Annual%20Reports/IITMadras-Annual-Report-22-23.pdf)
- [IIT Madras TechSoc](https://dost.iitm.ac.in/techclub)
- [Contemporary Arcana Hackathon reference](https://www.linkedin.com/posts/jayanth151002_arcanahackathon-iitmadras-ai-activity-7053962432104259584-RBHH)

**GitHub:** https://github.com/TechMafia-dev/ArcanaHackathon  
**Authors:** Shreyash Patidar & Hrishikesh
