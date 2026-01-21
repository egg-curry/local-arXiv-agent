import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
import aragbot_config as config

from typing import Dict, List, Optional
from evaluation.ragas_like import ragas_eval

class EvaluatorAgent:
    def evaluate(self, question: str, answer: str, contexts: List[str]) -> Optional[Dict]:
        return ragas_eval(question, answer, contexts)
