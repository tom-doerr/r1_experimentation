import inspect
from importlib import import_module

def python_reflection_test() -> str:
    """Test Python reflection capabilities by inspecting the current module.
    
    Returns:
        str: A string containing reflection test results
    """
    import sys
    current_module = sys.modules[__name__]
    functions = []
    classes = []
    
    for name, obj in vars(current_module).items():
        if name.startswith('_'):
            continue
        if callable(obj):
            functions.append(name)
        elif isinstance(obj, type):
            classes.append(name)
    
    return f"Functions: {sorted(functions)}\nClasses: {sorted(classes)}"
