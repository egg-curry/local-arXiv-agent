# local-arXiv-agent
A locally run agentic Retrieval-Augmented Generation (RAG) system for academic research over the arXiv API running over Docker. This project is built only on open-source models and tools, with optional evaluation hooks .

##Tech Stack

Language: Python 3.10+

LLMs: LLaMA / Qwen / Mistral (via Ollama)

Embeddings: Sentence-Transformers

Vector DB: Weaviate

UI: Streamlit

Evaluation: RAGAS-like heuristics

Infra: Docker, Docker Compose


## ▶️ How to Run (Local)

### Prerequisites

* Python 3.10+
* Docker & Docker Compose
* Ollama installed and running
* 8 GB RAM (16 GB recommended)

---

### Step 1: Clone the repository

```bash
git clone https://github.com/<your-username>/egg-curry.git
cd egg-curry
```

---

### Step 2: Create environment file

```bash
cp .env.example .env
```

Edit `.env` if you want to change models or retrieval settings.

---

### Step 3: Start required services

```bash
docker-compose up -d
```

Ensure:

* Weaviate → [http://localhost:8080](http://localhost:8080)
* Ollama → [http://localhost:11434](http://localhost:11434)

---

### Step 4: Pull the LLM model (once)

```bash
ollama pull llama3.1:8b
```

(You may replace the model name with any supported Ollama model.)

---

### Step 5: Run the Streamlit application

```bash
streamlit run app_streamlit.py
```

---

### Step 6: Open in browser

```
http://localhost:8501
```

---

### Notes

* First run may be slow due to model loading and arXiv ingestion
* After ingestion, the system can run fully offline
* CPU-only execution is supported (slower)

---


System Requirements (Local Execution)

OS: Linux (Ubuntu 20.04+ recommended) or Windows 10/11 64-bit (WSL2 supported)

CPU: Intel Core i5 (11th Gen or equivalent AMD Ryzen 5)

RAM: 8 GB RAM (16 GB recommended for smoother multi-agent execution)

Storage: 20 GB free disk space (excluding model weights)

Dependencies: Docker & Docker Compose & Ollama (for local LLM inference)

Network: Broadband Internet connection (for arXiv ingestion only)

Notes:

-Designed to run fully offline after ingestion

-Trades latency for higher factual accuracy

-No proprietary API keys required



Structure

├── app_streamlit.py        # Streamlit UI

├── aragbot_config.py       # Central configuration

├── arxiv_client.py         # arXiv API client

├── chunking.py             # Text chunking logic

├── embedder.py             # Embedding model wrapper

├── llm_local.py            # Local LLM interface (Ollama)

├── weaviate_store.py       # Vector DB operations

│

├── router_agent.py         # Query routing agent

├── researcher_agent.py    # Main reasoning agent

├── citation_agent.py      # Citation generation

├── evaluator_agent.py     # Answer evaluation

├── memory_manager.py      # Conversation memory

├── ragas_like.py           # RAGAS-style heuristics
│

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

├── .env.example

├── .gitignore

├── LICENSE

└── README.md


