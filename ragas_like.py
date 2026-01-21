from typing import Dict, List, Optional, Any
import pandas as pd

RAGAS_AVAILABLE = False
evaluate = None

faithfulness: Any = None
answer_relevancy: Any = None
context_relevancy: Any = None
evaluate: Any = None

try:
    from ragas.metrics import faithfulness, answer_relevancy, context_relevancy
    from ragas import evaluate  
    RAGAS_AVAILABLE = True
except ImportError:
    RAGAS_AVAILABLE = False

def ragas_eval(question: str, answer: str, contexts: List[str]) -> Optional[Dict[str, float]]:
    """Simplified RAGAS eval - safe against API changes."""
    if not RAGAS_AVAILABLE or evaluate is None:
        return {"faithfulness": 0.0, 
                "answer_relevancy": 0.0, 
                "context_relevancy": 0.0}
    
    try:
        dataset = {
            "question": [question],
            "answer": [answer],
            "contexts": [[contexts]],  # ragas expects list of list[str]
        }
        # Filter None metrics + type cast
        metrics = [m for m in [faithfulness, answer_relevancy, context_relevancy] if m is not None]
        if not metrics:
            return None
            
        result = evaluate(dataset, metrics=metrics)
        
        # Handle Executor → DataFrame (newer ragas API)
        if hasattr(result, 'to_pandas'):
            df = result.to_pandas()
        else:
            df = pd.DataFrame(result)
            
        scores = df.iloc[0].to_dict()
        return {
            "faithfulness": float(scores.get("faithfulness", 0.0)),
            "answer_relevancy": float(scores.get("answer_relevancy", 0.0)),
            "context_relevancy": float(scores.get("context_relevancy", 0.0)),
        }
    except Exception:
        return None
