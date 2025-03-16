from .config import DEFAULT_MODEL

def normalize_model_name(model: str) -> str:
    """Normalize model name to include proper provider prefix."""
    if not isinstance(model, str) or not model.strip():
        return DEFAULT_MODEL
        
    model = model.strip().lower()
    
    # Handle aliases
    if model == "flash":
        return "openrouter/google/gemini-2.0-flash-001"
    if model == "deepseek":
        return "deepseek/deepseek-chat"
        
    # Ensure proper format
    if "/" not in model:
        return f"openrouter/{model}"
    return model
