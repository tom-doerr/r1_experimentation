from typing import Dict
from .config import DEFAULT_MODEL, global_settings

def _normalize_model_name(model: str) -> str:
    """Normalize model name to include proper provider prefix."""
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Model must be a non-empty string")
        
    model = model.strip().lower()
    
    # Handle flash alias
    if model == "flash":
        return "openrouter/google/gemini-2.0-flash-001"
        
    # Handle deepseek models
    if model == "deepseek":
        return "deepseek/deepseek-chat"
    if model.startswith("deepseek/"):
        return model
        
    # Handle openrouter models
    if model.startswith("openrouter/"):
        return model
        
    # Handle other models
    if "/" in model:
        return f"openrouter/{model}"
        
    return f"openrouter/{model}"
