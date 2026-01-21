from dataclasses import dataclass
from typing import Literal, Dict, Any
from pydantic import BaseModel
import weaviate
from weaviate.connect import ConnectionParams
from weaviate.classes.init import AdditionalConfig, Timeout

@dataclass
class LLMConfig:
    backend: Literal["ollama"] = "ollama"
    model_name: str = "qwen2.5:3b"
    base_url: str = "http://localhost:11434"
    max_tokens: int = 1024
    temperature: float = 0.0
    top_p: float = 0.9  
llm_config = LLMConfig()

@dataclass
class RetrievalConfig:
    http_host: str = "localhost"
    http_port: int = 8080
    grpc_host: str = "localhost"  
    grpc_port: int = 50051
    http_secure: bool = False     
    grpc_secure: bool = False    
    skip_init_checks: bool = False
    weaviate_index: str = "ArxivPaper"
    use_weaviate: bool = True
    top_k: int = 6
    chunk_size: int = 512
    chunk_overlap: int = 64
    max_chunks_per_doc: int = 8
retrieval_config = RetrievalConfig()

@dataclass
class ArxivConfig:
    max_results: int = 20
arxiv_config = ArxivConfig()

@dataclass
class EmbedderConfig:
    model_name: str = "sentence-transformers/all-MiniLM-L6-v2"
    batch_size: int = 32
embedder_config = EmbedderConfig()

@dataclass
class AgentConfig:
    memory_turns: int = 3
agent_config = AgentConfig()

@dataclass
class EvalConfig:
    enable_eval: bool = True
    sample_eval_every_n_queries: int = 1
eval_config = EvalConfig()