import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import aragbot_config as config

from typing import List, Dict
import weaviate
from weaviate.classes.config import Property, DataType
from aragbot_config import retrieval_config
from models.embedder import Embedder

class WeaviateStore:
    def __init__(self, embedder: Embedder):
        self.client = weaviate.connect_to_local(
            host="localhost", 
            port=retrieval_config.http_port, 
            grpc_port=retrieval_config.grpc_port)
        self.embedder = embedder
        self.index = retrieval_config.weaviate_index  # type: ignore
        self._ensure_schema()

    def _ensure_schema(self):
        if self.index in self.client.collections.list_all():
            return
        self.client.collections.create(
            self.index,
            properties=[
                Property(name="text", data_type=DataType.TEXT),
                Property(name="arxiv_id", data_type=DataType.TEXT),
                Property(name="title", data_type=DataType.TEXT),
                Property(name="doi", data_type=DataType.TEXT),
                Property(name="journal_ref", data_type=DataType.TEXT),
                Property(name="published", data_type=DataType.TEXT),
                Property(name="url_abs", data_type=DataType.TEXT),
                Property(name="url_pdf", data_type=DataType.TEXT),
            ],
            vectorizer_config=None,  # use external embeddings
        )

    def index_chunks(self, chunks: List[Dict]):
        collection = self.client.collections.get(self.index)
        with collection.batch.dynamic() as batch:
            for c in chunks:
                vec = self.embedder.encode(c["text"]).tolist()
                batch.add_object(
                    properties={
                        "text": c["text"],
                        "arxiv_id": c["arxiv_id"],
                        "title": c["meta"]["title"],
                        "doi": c["meta"]["doi"],
                        "journal_ref": c["meta"]["journal_ref"],
                        "published": str(c["meta"]["published"]),
                        "url_abs": c["meta"]["url_abs"],
                        "url_pdf": c["meta"]["url_pdf"],
                    },
                    vector=vec,
                )

    def query(self, query: str, top_k: int | None = None) -> List[Dict]:
        if top_k is None:
            top_k = retrieval_config.top_k
        collection = self.client.collections.get(self.index)
        query_vec = self.embedder.encode(query)
        res = collection.query.near_vector(
            _query_vector=query_vec.tolist(),
            limit=top_k,
        ) # type: ignore
        
        hits = []
        for o in res.objects:
            props = o.properties
            hits.append({
                "text": props["text"],
                "arxiv_id": props["arxiv_id"],
                "title": props["title"],
                "doi": props.get("doi"),
                "journal_ref": props.get("journal_ref"),
                "published": props.get("published"),
                "url_abs": props.get("url_abs"),
                "url_pdf": props.get("url_pdf"),
                "score": o.metadata.distance,
            })
        return hits
