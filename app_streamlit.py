import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import streamlit as st
import weaviate
import time
import aragbot_config as config
from aragbot_config import retrieval_config
from models.llm_local import LocalLLM
from models.embedder import Embedder
from models.weaviate_store import WeaviateStore
from agents.router_agent import RouterAgent
from agents.researcher_agent import ResearcherAgent
from agents.citation_agent import CitationAgent
from agents.evaluator_agent import EvaluatorAgent
from agents.memory_manager import MemoryManager

OLLAMA_URL = "http://host.docker.internal:11435"  # Ollama host port
WEAVIATE_URL = "http://host.docker.internal:8080"  # Weaviate host port

@st.cache_resource
def get_weaviate_client():
    """Safe Weaviate connection - minimal config"""
    for attempt in range(5):
        try:
            client = weaviate.connect_to_local(
                host="host.docker.internal",
                port=8080,
                grpc_port=50051
            )
            
            if client.is_ready():
                st.success("✅ Weaviate connected!")
                return client
            client.close()
            
        except Exception as e:
            st.warning(f"Weaviate attempt {attempt+1}: {str(e)[:80]}")
            time.sleep(2)
    
    st.error("❌ Cannot connect to Weaviate")
    st.stop()
    return None

def init_objects():
    if "initialized" in st.session_state:
        return
    llm = LocalLLM()
    embedder = Embedder()
    store = WeaviateStore(embedder)
    router = RouterAgent(llm)
    researcher = ResearcherAgent(llm, store)
    citation_agent = CitationAgent(llm)
    evaluator = EvaluatorAgent()
    memory = MemoryManager()

    st.session_state.llm = llm
    st.session_state.embedder = embedder
    st.session_state.store = store
    st.session_state.router = router
    st.session_state.researcher = researcher
    st.session_state.citation_agent = citation_agent
    st.session_state.evaluator = evaluator
    st.session_state.memory = memory
    st.session_state.query_count = 0
    st.session_state.initialized = True

def main():
    st.set_page_config(page_title="arXiv Agentic RAG", page_icon="📚")
    init_objects()

    st.title("arXiv Agentic RAG Assistant")
    st.caption("Local, agentic research assistant over the arXiv API.")

    user_query = st.text_area(
        "Enter your research question",
        placeholder="e.g., What are recent advances in retrieval-augmented generation evaluation?"
    )

    if st.button("Run analysis") and user_query.strip():
        router = st.session_state.router
        researcher = st.session_state.researcher
        citation_agent = st.session_state.citation_agent
        evaluator = st.session_state.evaluator
        memory = st.session_state.memory

        with st.spinner("Routing and retrieving relevant literature..."):
            route = router.route(user_query, memory.get_context())
            if route == "simple_arxiv":
                result = researcher.answer_simple(user_query)
                contexts = [p["summary"] for p in result["source_papers"]]
                papers_for_citation = result["source_papers"]
            else:
                result = researcher.answer_full_rag(user_query)
                contexts = [c["text"] for c in result["source_chunks"]]
                # de-duplicate by arxiv_id for citations
                seen = {}
                for c in result["source_chunks"]:
                    aid = c["arxiv_id"]
                    if aid not in seen:
                        seen[aid] = {
                            "arxiv_id": aid,
                            "title": c["title"],
                            "summary": c["text"],
                            "authors": [],
                            "doi": c.get("doi"),
                            "published": c.get("published"),
                            "journal_ref": c.get("journal_ref"),
                            "url_abs": c.get("url_abs"),
                            "url_pdf": c.get("url_pdf"),
                        }
                papers_for_citation = list(seen.values())

        st.subheader("Assistant response")
        st.write(result["answer"])

        with st.expander("Source citations"):
            citation_text = citation_agent.format_citations(papers_for_citation)
            st.markdown(citation_text)

        eval_scores = None
        st.session_state.query_count += 1
        if config.eval_config.enable_eval and st.session_state.query_count % config.eval_config.sample_eval_every_n_queries == 0:
            with st.spinner("Running RAG quality evaluation (RAGAS-style)..."):
                eval_scores = evaluator.evaluate(user_query, result["answer"], contexts)

        if eval_scores:
            st.subheader("Quality diagnostics (heuristic/offline)")
            st.write(eval_scores)
        

        memory.add_turn(user_query, result["answer"])

        with st.expander("Conversation memory (last 3 queries)"):
            for turn in memory.get_context():
                st.markdown(f"**User:** {turn['user']}")
                st.markdown(f"**Assistant:** {turn['assistant']}")

if __name__ == "__main__":
    main()
