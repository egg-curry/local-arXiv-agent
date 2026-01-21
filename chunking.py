import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import aragbot_config as config

from typing import List, Dict
from textwrap import wrap
from aragbot_config import retrieval_config

def chunk_metadata(paper: Dict) -> List[Dict]:
    text = f"Title: {paper['title']}\n\nAbstract: {paper['summary']}\n\n" \
           f"DOI: {paper.get('doi')}\nJournal: {paper.get('journal_ref')}\n" \
           f"Categories: {', '.join(paper.get('categories', []))}"

    chunks = []

    size = retrieval_config.chunk_size # type: ignore
    for i, chunk in enumerate(wrap(text, size)):
        chunks.append({
            "chunk_id": f"{paper['arxiv_id']}_{i}",
            "arxiv_id": paper["arxiv_id"],
            "text": chunk,
            "meta": {
                "title": paper["title"],
                "doi": paper.get("doi"),
                "journal_ref": paper.get("journal_ref"),
                "published": paper.get("published"),
                "url_abs": paper["url_abs"],
                "url_pdf": paper["url_pdf"],
            },
        })
    return chunks
