import litellm
from .utils import normalize_model_name as _normalize_model_name

def _escape_xml(text: str) -> str:
    """Escape XML special characters."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def litellm_completion(prompt: str, model: str, max_tokens: int = 100) -> str:
    """Get single completion using LiteLLM API."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Model must be a non-empty string")
    if not isinstance(max_tokens, int) or max_tokens <= 0:
        raise ValueError("max_tokens must be a positive integer")
        
    model = normalize_model_name(model)
    
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        content = response.choices[0].message.content
        escaped_content = _escape_xml(content)
        return f"<response>{escaped_content}</response>"
    except litellm.exceptions.BadRequestError as e:
        if "not a valid model ID" in str(e):
            raise ValueError(f"Invalid model: {model}") from e
        raise RuntimeError(f"Bad request: {e}") from e
    except litellm.APIError as e:
        raise RuntimeError(f"API Error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}") from e
    """Get single completion using LiteLLM API."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Model must be a non-empty string")
    if not isinstance(max_tokens, int) or max_tokens <= 0:
        raise ValueError("max_tokens must be a positive integer")
        
    model = normalize_model_name(model)
    
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        content = response.choices[0].message.content
        escaped_content = _escape_xml(content)
        return f"<response>{escaped_content}</response>"
    except litellm.exceptions.BadRequestError as e:
        if "not a valid model ID" in str(e):
            raise ValueError(f"Invalid model: {model}") from e
        raise RuntimeError(f"Bad request: {e}") from e
    except litellm.APIError as e:
        raise RuntimeError(f"API Error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}") from e
    """Get single completion using LiteLLM API."""
    if not isinstance(prompt, str) or not prompt.strip():
        raise ValueError("Prompt must be a non-empty string")
    if not isinstance(model, str) or not model.strip():
        raise ValueError("Model must be a non-empty string")
    if not isinstance(max_tokens, int) or max_tokens <= 0:
        raise ValueError("max_tokens must be a positive integer")
        
    model = _normalize_model_name(model)
    
    try:
        response = litellm.completion(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=0.7
        )
        content = response.choices[0].message.content
        escaped_content = _escape_xml(content)
        return f"<response>{escaped_content}</response>"
    except litellm.exceptions.BadRequestError as e:
        if "not a valid model ID" in str(e):
            raise ValueError(f"Invalid model: {model}") from e
        raise RuntimeError(f"Bad request: {e}") from e
    except litellm.APIError as e:
        raise RuntimeError(f"API Error: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error: {e}") from e
