from typing import Any, Dict, Optional
import xml.etree.ElementTree as ET
from .tools import Tool, ShellCodeExecutor
from .interface import UserInterface, ConsoleInterface
from .reflection import python_reflection_test 
from .agent import Agent, ConcreteAgent, AgentAssert
from .config import DEFAULT_MODEL, global_settings
from .utils import normalize_model_name
from .envs import Env1, Env2
from .isolation import IsolatedEnvironment, run_container
from .llm_utils import litellm_completion, litellm_streaming







def parse_xml(xml_string: str) -> Dict[str, Any]:
    """Parse XML string into dictionary.
    
    Args:
        xml_string: XML content to parse
        
    Returns:
        Dict[str, Any]: Parsed XML content as dictionary
        
    Raises:
        ValueError: If input is invalid or XML is malformed
        TypeError: If XML structure is invalid
    """
    if not isinstance(xml_string, str) or not xml_string.strip():
        raise ValueError("Input must be a non-empty string")
    
    try:
        def parse_element(element):
            if len(element) == 0:
                return element.text
            return {child.tag: parse_element(child) for child in element}
            
        root = ET.fromstring(xml_string)
        if not root:
            raise ValueError("Empty XML document")
        return {root.tag: parse_element(root)}
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}") from e
    except AttributeError as e:
        raise TypeError(f"Invalid XML structure: {e}") from e
    except Exception as e:
        raise ValueError(f"Error parsing XML: {e}") from e



def _validate_global_settings(settings: Dict[str, float]) -> None:
    """Validate global settings values."""
    required_keys = {'starting_cash', 'max_net_worth', 'min_net_worth', 'cash_penalty'}
    if not isinstance(settings, dict):
        raise TypeError("settings must be a dictionary")
    if not all(key in settings for key in required_keys):
        raise ValueError(f"settings must contain all required keys: {required_keys}")
    if not all(isinstance(v, (int, float)) for v in settings.values()):
        raise TypeError("All settings values must be numeric")
































































__all__ = [
    "parse_xml", "Tool", "ShellCodeExecutor", "python_reflection_test",
    "litellm_completion", "litellm_streaming", "DEFAULT_MODEL", "global_settings",
    "IsolatedEnvironment", "run_container", "UserInterface", "ConsoleInterface",
    "Agent", "AgentAssert", "ConcreteAgent", "Env1", "Env2"
]



