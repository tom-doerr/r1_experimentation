import os

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


FLASH = 'openrouter/google/gemini-2.0-flash-001'
OR1 = 'openrouter/deepseek/deepseek-r1'
MODEL = FLASH

XML_DATA = '<response><message>hello</message></response>'
parsed_data = parse_xml(XML_DATA)

message = parsed_data['message']
print("message:", message)
assert message == 'hello'

completion = litellm_completion(prompt="hello", model=OR1)
print("completion:", completion)
assert "Hello" in completion

TEST_OUTPUT_VAR = python_reflection_testing()
print("test_output_var:", TEST_OUTPUT_VAR)
assert TEST_OUTPUT_VAR == 'test_output_var'

REWARD = test_env_1('aaa')
assert REWARD == 3

REWARD = test_env_1('aabbjadfa')
assert REWARD == 4


reply_generator = litellm_streaming('hi', model=OR1, max_tokens=40)
print("reply_generator:", reply_generator)
for reply in reply_generator:
    print("-", reply, end='')

agent = Agent(model=MODEL)

output = agent.reply('hi')
print("output:", output)
print("last_completion:", agent.last_completion)

XML_DATA_2 = '<response><thinking>test abc def</thinking><message>Hi! How can I help you?</message><memory><search></search><replace>The user wrote just hi.</replace></memory></response>'
parsed_data_2 = agent.parse_xml(XML_DATA_2)
assert parsed_data_2['message'] == 'Hi! How can I help you?'
assert parsed_data_2['thinking'] == 'test abc def'
assert parsed_data_2['memory']['search'] == ""
assert parsed_data_2['memory']['replace'] == 'The user wrote just hi.'
# the agent returns None sometimes, but the tests expect empty string, fixed in code
agent._update_memory(parsed_data_2['memory']['search'], parsed_data_2['memory']['replace'])

agent_assert = AgentAssert(model=MODEL)
assert isinstance(agent_assert.agent, Agent)

bool_val = agent_assert.parse_xml('<response><message>The implementation does not match specifications</message><bool>False</bool></response>')
assert bool_val is False

return_val = agent_assert('twenty two has has the same meaning as 22')
print("return_val:", return_val)
assert isinstance(return_val, bool)

two_plus_two_is_4 = agent_assert('two plus two is 5')
print("two_plus_two_is_4:", two_plus_two_is_4)
assert two_plus_two_is_4 is False


shell_code_executor = ShellCodeExecutor()
shell_code_executor_pwd = shell_code_executor('pwd')
print("shell_code_executor_pwd:", shell_code_executor_pwd)
assert 'r1_experimentation' in shell_code_executor_pwd

shell_code_executor_ls = shell_code_executor('ls')
print("shell_code_executor_ls:", shell_code_executor_ls)
assert 'plex.md' in shell_code_executor_ls
