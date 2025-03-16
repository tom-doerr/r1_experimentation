from .config import DEFAULT_MODEL, global_settings

def normalize_model_name(model: str) -> str:
    if not isinstance(model, str) or not model.strip():
        return DEFAULT_MODEL
        
    model = model.strip().lower()
    
    if model == "flash":
        return "openrouter/google/gemini-2.0-flash-001"
    if model == "deepseek":
        return "deepseek/deepseek-chat"
    if "/" not in model:
        return f"openrouter/{model}"
    return model
