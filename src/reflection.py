import inspect
from importlib import import_module

def python_reflection_test() -> str:
    """Test Python reflection capabilities.
    
    Returns:
        str: A string containing reflection test results
    """
    current_module = import_module(__name__.rsplit('.', 1)[0])  # Get root package name
    functions = []
    classes = []
    
    for name in dir(current_module):
        if name.startswith('_'):
            continue
        obj = getattr(current_module, name)
        if inspect.isfunction(obj):
            functions.append(name)
        elif inspect.isclass(obj):
            classes.append(name)
    
    return f"Functions: {sorted(functions)}\nClasses: {sorted(classes)}"
