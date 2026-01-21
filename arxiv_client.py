import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import aragbot_config as config

import arxiv
from typing import List, Dict
from aragbot_config import arxiv_config

def search_arxiv(query: str, max_results: int | None = None) -> List[Dict]:
    if max_results is None:
        max_results = arxiv_config.max_results

    client = arxiv.Client()
    search = arxiv.Search(
        query=query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.Relevance,
    )
    results = []
    for result in client.results(search):
        # result has metadata incl. doi, published, journal_ref etc.[web:11][web:13]
        results.append({
            "arxiv_id": result.entry_id.split("/")[-1],
            "title": result.title,
            "summary": result.summary,
            "authors": [a.name for a in result.authors],
            "doi": getattr(result, "doi", None),
            "published": result.published,   # datetime
            "updated": result.updated,
            "journal_ref": getattr(result, "journal_ref", None),
            "primary_category": result.primary_category,
            "categories": result.categories,
            "comment": getattr(result, "comment", None),
            "url_abs": result.entry_id,
            "url_pdf": result.pdf_url,
        })
    return results
