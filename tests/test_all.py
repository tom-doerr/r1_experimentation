import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import src
from src import *
from src.main import *



FLASH = 'openrouter/google/gemini-2.0-flash-001'  
R1 = 'deepseek/deepseek-reasoner'
OR1 = 'openrouter/deepseek/deepseek-r1'
MODEL = FLASH

xml_data = '<response><message>hello</message></response>'
PARSED_DATA = parse_xml(xml_data)

MESSAGE = PARSED_DATA['message']
print("message:", MESSAGE)

# set flash as the default model
# don't mock
completion = litellm_completion('hi', model=MODEL)
print("completion:",completion)

reply_generator = litellm_streaming('hi')
print("reply_generator:", reply_generator)

for reply in reply_generator:
    print("reply:", reply, end='')



TEST_OUTPUT_VAR = python_reflection_testing()
print("test_output_var:", TEST_OUTPUT_VAR)
assert TEST_OUTPUT_VAR == 'test_output_var'



reward = test_env_1('aaa')
assert reward == 3

reward = test_env_1('aabbjadfa')
assert reward == 4



reply_generator = litellm_streaming('hi', model=OR1, max_tokens=40)
print("reply_generator:", reply_generator)
for reply in reply_generator:
    print("-", reply, end='')


agent = Agent(model=MODEL)

output = agent.reply('hi')
print("output:", output)
last_completion = agent.last_completion
print("last_completion:", last_completion)

PARSED_DATA = agent._parse_xml(xml_data)
assert PARSED_DATA['message'] == 'hello'

xml_data_2 = '<response><thinking>test abc def</thinking><message>Hi! How can I help you?</message><memory><search></search><replace>The user wrote just hi.</replace></memory></response>'
PARSED_DATA_2 = agent._parse_xml(xml_data_2)
assert PARSED_DATA_2['message'] == 'Hi! How can I help you?'
assert PARSED_DATA_2['thinking'] == 'test abc def'
assert PARSED_DATA_2['memory']['search'] == ''
assert PARSED_DATA_2['memory']['replace'] == 'The user wrote just hi.'

agent._update_memory(PARSED_DATA_2['memory']['search'], PARSED_DATA_2['memory']['replace'])
assert agent.memory == 'The user wrote just hi.'


agent_assert = AgentAssert(model=MODEL)
assert isinstance(agent_assert.agent, Agent)

bool_val = agent_assert._parse_xml('<response><message>The implementation does not match specifications</message><bool>False</bool></response>')
assert bool_val is False


return_val = agent_assert('twenty two has has the same meaning as 22')
print("return_val:", return_val)
assert isinstance(return_val, bool)

two_plus_two_is_4 = agent_assert('two plus two is 5')
print("two_plus_two_is_4:", two_plus_two_is_4)
assert two_plus_two_is_4 is False


shell_code_executor = ShellCodeExecutor()


# check if this is a subset of the blacklisted commands
assert {'rm', 'cat', 'mv', 'cp'} & set(shell_code_executor.blacklisted_commands) == {'rm', 'cat', 'mv', 'cp'}
assert {'ls', 'date'} & set(shell_code_executor.whitelisted_commands) == {'ls', 'date'}


shell_code_executor_ls = shell_code_executor('ls')
print("shell_code_executor_ls:", shell_code_executor_ls)
assert 'plex.md' in shell_code_executor_ls



