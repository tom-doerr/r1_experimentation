def python_reflection_test(obj: object) -> str:
    """Basic reflection test to inspect object properties."""
    return f"Type: {type(obj).__name__}, Attributes: {dir(obj)}"
