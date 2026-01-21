from typing import Literal, Dict, List
from models.llm_local import LocalLLM

class RouterAgent:
    def __init__(self, llm: LocalLLM):
        self.llm = llm

    def route(self, user_query: str, history: List[Dict]) -> Literal["simple_arxiv", "full_rag"]:
        system_prompt = (
            "You are an accurate routing assistant"
            "Decide whether the query needs deeper retrieval over many papers"
            "('full_rag') or a small set of recent arXiv papers ('simple_arxiv')"
            "Return only one token: simple_arxiv or full_rag"
        )
        out = self.llm.chat(system_prompt, user_query).strip().lower()
        return "full_rag" if "full" in out else "simple_arxiv"
