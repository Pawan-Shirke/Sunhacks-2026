# 🛡️ RegIntel AI — Regulatory Intelligence Platform

A full-stack, multi-agent AI system for automated compliance monitoring of **RBI**, **SEBI**, and **MCA** regulations. Features an intelligent chatbot, multilingual voice assistant, 3D-animated dashboard, and real-time regulatory change detection.

---

## ✨ Key Features

| Feature | Description |
|--------|-------------|
| 📡 **Live Regulatory Feed** | Auto-scrapes RBI, SEBI, MCA for new circulars |
| 🔍 **AI Analysis Engine** | LangChain-powered impact analysis + draft amendments |
| 💬 **RAG Chatbot** | Ask regulatory questions in natural language |
| 🔊 **Voice Assistant** | Multilingual audio explanations (8 Indian languages) |
| 📊 **Reports Dashboard** | Structured JSON/Markdown compliance reports |
| 🏛️ **Policy Mapping** | ChromaDB vector search matches regs to your policies |

---

## 🚀 Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/your-org/regulatory-intelligence.git
cd regulatory-intelligence

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables (optional — needed for GPT-4)
export OPENAI_API_KEY="sk-..."

# 5. Run the app
streamlit run app.py
```

---

## 🏗️ Architecture

```
regulatory-intelligence/
├── app.py                    # Main Streamlit dashboard
├── requirements.txt
├── README.md
│
├── agents/
│   ├── scraper.py            # BeautifulSoup + requests — scrapes RBI/SEBI/MCA
│   ├── parser.py             # PyMuPDF — extracts text from PDFs
│   ├── diff_agent.py         # difflib — detects regulatory changes
│   ├── kb_agent.py           # ChromaDB — vector search for policy mapping
│   ├── reasoning_agent.py    # LangChain + GPT-4 — impact analysis
│   ├── report_agent.py       # JSON/Markdown report generation
│   ├── voice_agent.py        # gTTS — multilingual audio explanations
│   └── chatbot_agent.py      # RAG chatbot — regulatory Q&A
│
├── data/
│   ├── sample_data.py        # Rich RBI/SEBI/MCA sample datasets
│   ├── raw_docs/             # Downloaded PDFs (created at runtime)
│   └── text/                 # Extracted text files (created at runtime)
│
├── db/
│   └── chroma_data/          # ChromaDB vector store (created at runtime)
│
└── prompts/
    ├── impact_prompt.txt
    ├── amendment_prompt.txt
    └── explanation_prompt.txt
```

---

## 🤖 Agent Pipeline

```
Regulatory Sites (RBI/SEBI/MCA)
         │
    [Scraper Agent]         ← BeautifulSoup, requests
         │ PDF URLs
    [Parser Agent]          ← PyMuPDF
         │ Extracted Text
    [Diff Agent]            ← difflib
         │ Change List
    [KB Agent]              ← ChromaDB vector search
         │ Relevant Policies
    [Reasoning Agent]       ← LangChain + GPT-4
         │ Impact Analysis
    [Report Agent]          ← JSON / Markdown
         │
    [Dashboard / Voice / Chatbot]
```

---

## 🌐 Voice Languages Supported

| Language | Code | Native Script |
|---------|------|---------------|
| English | en | English |
| Hindi | hi | हिंदी |
| Tamil | ta | தமிழ் |
| Telugu | te | తెలుగు |
| Bengali | bn | বাংলা |
| Marathi | mr | मराठी |
| Gujarati | gu | ગુજરાતી |
| Kannada | kn | ಕನ್ನಡ |

---

## ⚙️ Configuration

### Environment Variables
```
OPENAI_API_KEY=sk-...    # Optional: enables GPT-4 analysis
```

### Streamlit Secrets (for Streamlit Cloud deployment)
```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "sk-..."
```

---

## 🚢 Deployment

### Streamlit Community Cloud
1. Push to GitHub
2. Visit [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect repo → select `app.py`
4. Add `OPENAI_API_KEY` in Secrets
5. Deploy!

### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

---

## 📊 Sample Datasets Included

| ID | Source | Topic |
|----|--------|-------|
| RBI-2024-001 | RBI | KYC Amendment 2024 |
| SEBI-2024-002 | SEBI | IPO Enhanced Disclosures |
| MCA-2024-003 | MCA | Annual Filing Rules |
| RBI-2024-004 | RBI | Stressed Assets Framework |
| SEBI-2024-005 | SEBI | Cybersecurity Framework (CSCRF) |
| MCA-2024-006 | MCA | PPIRP Amendment (MSME) |

Internal policies indexed: KYC, Loan Origination, IPO Compliance, NPA Management, Cybersecurity, CSR, MSME Lending, AML/CFT.

---

## 🧪 Testing

```bash
# Run unit tests
python -m pytest tests/ -v

# Test individual agents
python agents/scraper.py
python agents/parser.py
python agents/diff_agent.py
```

---

## 📝 License
MIT License — Free to use, modify, and distribute.

---

*Built with ❤️ using Python, Streamlit, LangChain, ChromaDB, PyMuPDF, BeautifulSoup, and gTTS.*
