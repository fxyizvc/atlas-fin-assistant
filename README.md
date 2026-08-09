# 📈 Atlas AI Financial Assistant

**Atlas** is an intelligent, voice-enabled AI Financial Analyst and co-pilot living inside Telegram.

Built for finance professionals, founders, and investors, Atlas simplifies daily financial workflows by delivering real-time stock market metrics, processing voice inquiries, and analyzing complex financial documents such as earnings reports and financial statements.

---

## 🚀 Key Features

### 🎙️ Voice Note Processing

Send a native Telegram voice note to Atlas and ask questions about markets, companies, or financial documents.

Atlas uses **Groq Whisper (`whisper-large-v3`)** to transcribe speech with low latency before passing the request to the AI engine.

### 📊 Real-Time Market Data

Atlas uses **Groq's Llama 3.3 70B** model with function/tool calling to intelligently determine when market data is required.

It dynamically queries **`yfinance`** to retrieve information such as:

* Current stock prices
* Daily percentage changes
* 52-week highs and lows
* Market information
* Company-specific price data

### 📄 Financial Document Intelligence

Upload financial PDFs directly through Telegram.

Atlas can process documents such as:

* Earnings reports
* Annual reports
* Financial statements
* SEC filings
* Investor presentations
* Other financial documents

PDF text is extracted in-memory using **`pypdf`** and passed to the LLM for analysis.

Atlas can provide:

* Executive summaries
* Revenue analysis
* Financial highlights
* Risk factors
* Key business developments
* Important figures and metrics

### 💬 Natural Analyst Persona

Atlas is designed to communicate like a senior financial analyst.

Instead of relying on complicated slash commands, users can simply ask questions naturally.

For example:

> "What's happening with NVIDIA today?"

> "Compare Apple's current price with its 52-week high."

> "Summarize this earnings report."

> "What are the major risks mentioned in this document?"

---

# 🛠️ Tech Stack

| Component              | Technology                        |
| ---------------------- | --------------------------------- |
| Programming Language   | Python 3.10+                      |
| Web Framework          | FastAPI                           |
| Telegram Bot SDK       | `python-telegram-bot`             |
| AI / LLM               | Groq API — Llama 3.3 70B          |
| Speech-to-Text         | Groq Whisper — `whisper-large-v3` |
| Market Data            | `yfinance`                        |
| PDF Processing         | `pypdf`                           |
| Environment Management | `python-dotenv`                   |
| Deployment             | Render / Railway                  |

---

# 🏗️ System Architecture

Atlas follows a modular request-processing pipeline.

```text
                         ┌─────────────────────┐
                         │   Telegram User     │
                         └──────────┬──────────┘
                                    │
                    ┌───────────────┼────────────────┐
                    │               │                │
                  Text            Voice             PDF
                    │               │                │
                    │        ┌──────▼──────┐         │
                    │        │ Groq Whisper│         │
                    │        │ Transcription│        │
                    │        └──────┬──────┘         │
                    │               │                │
                    └───────────────┼────────────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │     FastAPI         │
                         │   Telegram Webhook  │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │    AI Engine        │
                         │  Llama 3.3 70B      │
                         └──────────┬──────────┘
                                    │
                     ┌──────────────┼──────────────┐
                     │              │              │
                     ▼              ▼              ▼
               Normal Query   Function Call    PDF Analysis
                                    │              │
                                    ▼              ▼
                              ┌───────────┐   ┌───────────┐
                              │ yfinance  │   │   pypdf   │
                              └─────┬─────┘   └─────┬─────┘
                                    │               │
                                    └───────┬───────┘
                                            │
                                            ▼
                                  ┌─────────────────┐
                                  │  LLM Response   │
                                  │    Formatting   │
                                  └────────┬────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │ Telegram Reply  │
                                  └─────────────────┘
```

---

# 🔄 Request Flow

## 1. User Request

The user sends one of the following through Telegram:

* Text message
* Voice note
* PDF document

---

## 2. FastAPI Webhook

The Telegram webhook sends the incoming update to the FastAPI application.

`main.py` receives and routes the request to the appropriate handler.

---

## 3. Voice Pipeline

When a voice message is received:

```text
Telegram Voice Note
        ↓
Download .ogg file
        ↓
Groq Whisper
        ↓
Transcribed Text
        ↓
AI Engine
```

The transcription is generated using:

```text
whisper-large-v3
```

The resulting text is then processed like a normal user query.

---

## 4. AI Engine & Tool Execution

`ai_engine.py` handles communication with the Groq LLM.

The model can determine when external market data is required.

For example:

```text
User:
"What is Apple's current stock price?"

        ↓

Llama 3.3 70B
        ↓
Function Call
        ↓
get_stock_quote()
        ↓
yfinance
        ↓
Market Data
        ↓
Llama
        ↓
Formatted Response
```

This allows Atlas to combine natural-language reasoning with real-time financial data.

---

## 5. PDF Pipeline

When a PDF is uploaded:

```text
Telegram PDF
      ↓
Download file
      ↓
pypdf
      ↓
Extract text in-memory
      ↓
Financial analysis
      ↓
Llama 3.3 70B
      ↓
Structured response
      ↓
Telegram
```

The PDF does not need to be permanently stored on the server for basic processing.

---

## 6. Response Generation

After processing the request, Atlas generates a concise response and sends it back to the user through Telegram.

---

# 📁 Project Structure

```text
atlas-fin-assistant/
│
├── main.py
│   └── FastAPI server, Telegram webhook,
│       application initialization and handlers
│
├── ai_engine.py
│   └── Groq LLM integration, function calling,
│       conversation context and response generation
│
├── financial_tools.py
│   └── yfinance integration and stock quote tools
│
├── document_handler.py
│   └── PDF downloading, text extraction
│       and financial document analysis
│
├── requirements.txt
│   └── Python dependencies
│
├── .env
│   └── Private API keys and configuration
│
└── README.md
    └── Project documentation
```

---

# 🏁 Quickstart Guide

## 1. Prerequisites

Before running Atlas, make sure you have:

* Python **3.10 or higher**
* A Telegram Bot Token
* A Groq API Key
* Git
* Internet access

### Create a Telegram Bot

Open Telegram and start a conversation with **@BotFather**.

Create a new bot and copy the generated bot token.

### Get a Groq API Key

Create an account and generate an API key from the Groq Console.

---

# 2. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/atlas-fin-assistant.git
cd atlas-fin-assistant
```

Replace `YOUR_USERNAME` with your GitHub username.

---

# 3. Create a Virtual Environment

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 5. Configure Environment Variables

Create a `.env` file in the root directory:

```env
TELEGRAM_BOT_TOKEN="your_telegram_bot_token"
GROQ_API_KEY="your_groq_api_key"
WEBHOOK_URL="https://your-domain.com"
```

### Environment Variables

| Variable             | Description                                  |
| -------------------- | -------------------------------------------- |
| `TELEGRAM_BOT_TOKEN` | Token generated by Telegram BotFather        |
| `GROQ_API_KEY`       | API key used to access Groq models           |
| `WEBHOOK_URL`        | Public HTTPS URL of the deployed application |

> **Important:** Never commit your `.env` file or expose your API keys publicly.

Add `.env` to `.gitignore`:

```gitignore
.env
venv/
__pycache__/
*.pyc
```

---

# 💻 Running Locally

Start the FastAPI application using Uvicorn:

```bash
uvicorn main:app --reload
```

The application will normally be available at:

```text
http://127.0.0.1:8000
```

However, Telegram webhooks require a publicly accessible **HTTPS** endpoint.

For local development, you can expose your local server using a tunneling service such as Cloudflare Tunnel or ngrok.

---

# ☁️ Deployment

Atlas can be deployed on platforms such as:

* Render
* Railway
* Other platforms capable of running Python web applications

## Render / Railway Configuration

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

Configure the following environment variables in the platform dashboard:

```text
TELEGRAM_BOT_TOKEN
GROQ_API_KEY
WEBHOOK_URL
```

---

# 🔐 Security Considerations

Atlas handles API credentials and potentially sensitive financial documents, so security should be considered carefully.

### Never commit secrets

Do not commit:

```text
.env
API keys
Telegram bot tokens
Private credentials
```

### Use environment variables

Credentials should always be loaded from environment variables rather than hard-coded into Python source files.

### Validate uploaded files

Production deployments should validate:

* File type
* File size
* Malicious uploads
* Processing limits

### Protect the webhook

The Telegram webhook endpoint should be protected against unauthorized requests where possible.

---

# 📊 Example Queries

Once Atlas is running, users can interact with it naturally.

### Stock Market

```text
What's Apple's current stock price?
```

```text
How is NVIDIA performing today?
```

```text
What is Tesla's 52-week high?
```

### Financial Analysis

```text
Give me a quick analysis of Microsoft's current position.
```

```text
What are the major risks for this company?
```

### Voice

Send a Telegram voice note such as:

```text
"What's the current price of Amazon and how much has it changed today?"
```

Atlas transcribes the voice note and processes the request automatically.

### PDF Analysis

Upload an earnings report and ask:

```text
Summarize this report.
```

or:

```text
What were the company's biggest revenue drivers?
```

or:

```text
What risks does management mention?
```

---

# 🧠 AI Tool Calling

Atlas uses Llama's function-calling capabilities to decide when external financial information is required.

Conceptually:

```text
User Question
      │
      ▼
Llama 3.3 70B
      │
      ├── No external data required
      │          │
      │          ▼
      │      Generate response
      │
      └── Market data required
                 │
                 ▼
          get_stock_quote()
                 │
                 ▼
              yfinance
                 │
                 ▼
           Return market data
                 │
                 ▼
              Llama
                 │
                 ▼
          Final response
```

This architecture allows Atlas to combine an LLM with external financial tools rather than relying exclusively on the model's training data.

---

# 📄 PDF Processing

Atlas processes uploaded financial documents using `pypdf`.

The basic pipeline is:

```text
PDF Upload
    ↓
File Download
    ↓
PDF Text Extraction
    ↓
Text Processing
    ↓
LLM Analysis
    ↓
Financial Insights
```

This makes it possible to interact with lengthy financial documents directly through Telegram.

---

# ⚡ Performance

Atlas is designed around low-latency AI interactions.

The primary performance considerations are:

* Groq inference speed
* Groq Whisper transcription speed
* Telegram API latency
* `yfinance` response time
* PDF extraction time
* LLM context size

Voice requests can therefore follow a near-real-time workflow:

```text
Voice → Transcription → AI → Tool → Response
```

---

# 🧩 Future Improvements

Potential improvements for future versions include:

* 📈 Interactive stock charts
* 📊 Portfolio tracking
* 🔔 Price alerts
* 📰 Financial news integration
* 📉 Technical indicators
* 💼 Portfolio risk analysis
* 🧮 Financial ratio analysis
* 📑 Support for multiple document formats
* 🧠 Persistent user-specific conversation memory
* 🔐 Authentication and user access control
* 🗄️ Database-backed document storage
* 📚 Vector database / advanced RAG
* 🌐 Web dashboard
* 📱 Expanded Telegram commands
* 🧪 Automated testing and CI/CD
* 📦 Docker containerization
* ☁️ AWS deployment

---

# 🛣️ Roadmap

### Phase 1 — Core Assistant

* [x] Telegram integration
* [x] Text-based financial queries
* [x] Groq LLM integration
* [x] Stock market tool
* [x] PDF processing

### Phase 2 — Multimodal Interaction

* [x] Voice message transcription
* [x] Financial document analysis
* [ ] Image/chart analysis
* [ ] Financial chart extraction

### Phase 3 — Advanced Financial Intelligence

* [ ] Portfolio tracking
* [ ] Stock comparison
* [ ] Technical analysis
* [ ] Financial ratios
* [ ] News sentiment analysis
* [ ] Automated alerts

### Phase 4 — Production Platform

* [ ] Authentication
* [ ] Database
* [ ] Persistent user memory
* [ ] Monitoring
* [ ] Automated testing
* [ ] CI/CD
* [ ] Docker deployment
* [ ] Production observability

---

# ⚠️ Disclaimer

Atlas is an AI-powered financial information and analysis tool.

Information generated by Atlas should **not be considered professional financial, investment, legal, or tax advice**.

Market data can change rapidly, and AI-generated analysis may contain inaccuracies. Users should independently verify important financial information and consult qualified professionals before making investment decisions.

---

# 📜 License

This project is intended for educational and development purposes.

Add an appropriate open-source license here if the project is released publicly.

For example:

```text
MIT License
```

---

# 👨‍💻 Author

**Muhammed Fayiz V C**

Computer Science & Engineering

GitHub: `fxyizvc`

---

## ⭐ Project Summary

**Atlas AI Financial Assistant** combines:

```text
Telegram
   +
FastAPI
   +
Groq Llama 3.3 70B
   +
Groq Whisper
   +
yfinance
   +
pypdf
   ↓
AI Financial Co-Pilot
```

The goal is to provide a fast, conversational interface for accessing market information, analyzing financial documents, and interacting with financial data directly from Telegram.
