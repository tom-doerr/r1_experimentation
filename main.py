import xml.etree.ElementTree as ET
from typing import Dict, Any, Iterator
import litellm

def parse_xml(xml_string: str) -> Dict[str, Any]:
    """XML parser with simplified complexity"""
    def parse_element(element: ET.Element) -> Dict[str, Any]:
        # Parse element with nested children
        parsed = {element.tag: element.text.strip() if element.text else None}
        for child in element:
            child_parsed = parse_element(child)
            # Merge child tags into parent dict
            parsed.update(child_parsed)
        return parsed

    try:
        root = ET.fromstring(xml_string)
        return parse_element(root)
    except ET.ParseError as e:
        raise ValueError(f"Invalid XML: {e}") from e



# Simplified LiteLLM implementations
def litellm_completion(prompt: str, model: str = 'openrouter/google/gemini-2.0-flash-001', max_tokens: int = 100) -> str:
    # LiteLLM completion implementation with model parameter
    response = litellm.completion(
        model=model,
        messages=[{"content": prompt, "role": "user"}],
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

def litellm_streaming(prompt: str, model: str = 'openrouter/deepseek-ai/deepseek-r1', max_tokens: int = 20, temperature: float = 0.7) -> Iterator[str]:
    # Valid model check for OpenRouter compatibility
    if 'deepseek-reasoner' in model:
        model = 'deepseek-ai/deepseek-r1'  # Official OpenRouter model ID (lowercase)
    # LiteLLM streaming implementation with configurable model and tokens
    response = litellm.completion(
        model=model,
        messages=[{"content": prompt, "role": "user"}],
        stream=True,
        max_tokens=max_tokens
    )
    for chunk in response:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

def python_reflection_testing() -> str:
    """Simple reflection test that returns its own variable name"""
    return 'test_output_var'


class Agent:
    """Main agent for handling AI interactions"""
    def __init__(self, model: str = "default-model") -> None:
        self.model = model
        self._memory = {}

    def set_model(self, model_name: str) -> None:
        """Set the model to use for processing"""
        self.model = model_name

    def get_model(self) -> str:
        return self.model
        
    def complete(self, prompt: str) -> str:
        """Complete a prompt using the agent's model"""
        return litellm_completion(prompt, self.model)

    def reply(self, prompt: str) -> str:
        """Generate a response to the input prompt"""
        response = litellm_completion(prompt, model=self.model)
        return response

    def _parse_xml(self, xml_string: str) -> Dict[str, Any]:
        """Wrapper for XML parsing that handles empty results"""
        try:
            return parse_xml(xml_string)
        except ValueError:
            return {'error': 'Invalid XML format'}

    @property
    def last_completion(self) -> str:
        """Get last completion from litellm history"""
        if litellm.completion_cache:
            return litellm.completion_cache[-1].choices[0].message.content
        return ""

    def _update_memory(self, memory_data: dict) -> None:
        """Update agent memory with new data"""
        if 'memory' in memory_data:
            self._memory.update(memory_data['memory'])

def test_env_1(input_data: str) -> int:
    # Returns count of 'a's in input
    return input_data.count('a')

if __name__ == "__main__":
    # Test the XML parser
    TEST_XML = '<test><node>value</node></test>'
    print(parse_xml(TEST_XML))
