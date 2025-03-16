from src.main import (
    parse_xml,
    python_reflection_testing,
    test_env_1,
    Tool,
    ShellCodeExecutor,
    litellm_completion,
    litellm_streaming,
    Agent,
    AgentAssert,
    DEFAULT_MODEL,
)

# Create a class for test_env_1 to match the test_env.py expectations
"""
Wrapper class for test_env_1 function.
"""
class Env1:
    def __call__(self, input_string: str):
        return test_env_1(input_string)

__all__ = [
    "parse_xml", "python_reflection_testing", "test_env_1", "Tool", "ShellCodeExecutor",
    "litellm_completion", "litellm_streaming", "Agent", "AgentAssert", "DEFAULT_MODEL", "Env1"
]
