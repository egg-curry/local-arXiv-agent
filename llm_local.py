import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import aragbot_config as config
from aragbot_config import llm_config
from typing import List, Dict
import requests
import json

class LocalLLM:
    def __init__(self):
        self.model = llm_config.model_name
        self.base_url = "http://localhost:11434"

    def chat(self, system_prompt: str, user_msg: str) -> str:
        if not isinstance(user_msg, str):
            user_msg = "\n".join(map(str, user_msg))

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_msg},
            ],
            "options": {
                "num_predict": llm_config.max_tokens,
                "temperature": llm_config.temperature,
                "top_p": llm_config.top_p,
            },
            "stream": False,
        }

        resp = requests.post(
            f"{self.base_url}/api/chat",
            json=payload,
            stream=False,
            timeout=120
        )

        if not resp.ok:
            raise RuntimeError(
                f"Ollama error {resp.status_code}: {resp.text}"
            )

        return resp.json()["message"]["content"]