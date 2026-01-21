import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import torch
import aragbot_config as config
from typing import List
from sentence_transformers import SentenceTransformer

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import aragbot_config as config
os.environ["CUDA_VISIBLE_DEVICES"] = ""  # Hide GPU from PyTorch
class Embedder:
    def __init__(self, embedder_config=config.embedder_config):  # Pass config
        # Force CPU - fixes OOM
        self.device = "cpu"
        self.model = SentenceTransformer(
            embedder_config.model_name, 
            device=self.device
        )

    def encode(self, text: str | List[str]):
        return self.model.encode(text, convert_to_numpy=True)
