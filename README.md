# local-arXiv-agent
A locally run agentic Retrieval-Augmented Generation (RAG) system for academic research over the arXiv API running over Docker. This project is built only on open-source models and tools, with optional evaluation hooks .

ARAGBot/
├── agents/
│   ├── researcher_agent.py
│   ├── router_agent.py
│   ├── citation_agent.py
│   ├── evaluator_agent.py
│   └── memory_manager.py
├── models/
│   ├── llm_local.py
│   ├── chunking.py
│   ├── embedder.py
│   └── weaviate_store.py
├── retrieval/
│   └── arxiv_client.py
├── evaluation/
│   └── ragas_like.py
├── ui/
│   └── app_streamlit.py
│   └── Dockerfile
├── aragbot_config.py
├── docker-compose.yml
├── Dockerfile
├── README.md
├── .gitignore
└── requirements.txt (or pyproject.toml)
