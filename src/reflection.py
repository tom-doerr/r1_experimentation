def python_reflection_test(obj: object) -> str:
    """Inspect an object and return its type information."""
    if obj is None:
        return "None"
    return f"{type(obj).__name__}: {dir(obj)}"
