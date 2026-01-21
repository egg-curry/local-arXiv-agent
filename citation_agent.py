import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import aragbot_config as config

from typing import List, Dict
from models.llm_local import LocalLLM

class CitationAgent:
    def __init__(self, llm: LocalLLM):
        self.llm = llm

    def format_citations(self, papers: List[Dict]) -> str:
        # papers contain doi, title, authors, published, journal_ref, url_abs
        raw = ""
        for p in papers:
            raw += (
                f"Title: {p['title']}\n"
                f"Authors: {', '.join(p['authors'])}\n"
                f"DOI: {p.get('doi')}\n"
                f"Journal_ref: {p.get('journal_ref')}\n"
                f"Published: {p.get('published')}\n"
                f"arXiv ID: {p['arxiv_id']}\n"
                f"URL: {p['url_abs']}\n\n"
            )
        system_prompt = (
            "You are a citation formatting specialist"
            "Given metadata for arXiv papers, output a citation list with:\n"
            "- Title\n- Authors\n- DOI (if available)\n- Publisher or journal (from journal_ref when present)\n"
            "- Date of publication\n- arXiv ID\n\n"
            "Be concise & use professional style, especially with the DOI"
        )
        user_msg = f"Metadata:\n{raw}\n\nFormat citations:"
        return self.llm.chat(system_prompt, user_msg)
