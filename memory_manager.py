import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import aragbot_config as config

from collections import deque
from typing import Deque, Dict, List
from aragbot_config import agent_config

class MemoryManager:
    def __init__(self):
        self.history: Deque[Dict] = deque(maxlen=agent_config.memory_turns)

    def add_turn(self, user_msg: str, assistant_msg: str):
        self.history.append({"user": user_msg, "assistant": assistant_msg})

    def get_context(self) -> List[Dict]:
        return list(self.history)
