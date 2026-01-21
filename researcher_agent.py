import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import aragbot_config as config
import evaluation.ragas_like
from evaluation.ragas_like import ragas_eval
from typing import Dict, List
from retrieval.arxiv_client import search_arxiv
from models.weaviate_store import WeaviateStore
from models.llm_local import LocalLLM
from aragbot_config import retrieval_config

class ResearcherAgent:
    def __init__(self, llm: LocalLLM, store: WeaviateStore | None):
        self.llm = llm
        self.store = store


    def answer_simple(self, query: str) -> Dict:
        papers = search_arxiv(query)[:3]  # metadata only|context size cap
        context = "\n\n".join(
            f"Title: {p['title']}\nAbstract: {p['summary']}\nDOI: {p.get('doi')}"
            for p in papers
        )
        system_prompt = (
            "You are a professional research assistant. "
            "Answer concisely and with a professional tone. "
            "Use the provided arXiv abstracts. "
            "At the end, list cited papers with arXiv ID and DOI when available."
        )
        msg = f"User question: {query}\n\nContext:\n{context}"
        answer = self.llm.chat(system_prompt, msg)
        return {"answer": answer, "source_papers": papers}


    def answer_full_rag(self, query: str) -> Dict:
        # 1) retrieve from Weaviate, fallback to simple if disabled
        if not (self.store and retrieval_config.use_weaviate):
            return self.answer_simple(query)

        hits = self.store.query(query)
        context = "\n\n".join(
            f"[{h['arxiv_id']}] {h['title']}\n{h['text']}\nDOI: {h.get('doi')}"
            for h in hits
        )
        system_prompt = (
            "You are a professional research assistant answering with high accuracy. "
            "Use ONLY the provided context from arXiv. "
            "Cite specific papers inline as [arXiv:ID]. "
            "Prefer correctness over brevity."
        )
        msg = f"Question: {query}\n\nContext:\n{context}"
        answer = self.llm.chat(system_prompt, msg)
        eval_scores = ragas_eval(
            question=query,
            answer=answer,
            contexts=[h["text"] for h in hits]
        )
        return {"answer": answer, 
                "source_chunks": hits, 
                "evaluation": eval_scores}
    

    def _format_memory(self, memory_turns: List[Dict[str, str]]) -> str:
         if not memory_turns:
              return ""
         return "\n".join(
             f"User: {t['user']}\nAssistant: {t['assistant']}"
             for t in memory_turns
         )