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
parsed_data = parse_xml(xml_data)

message: str = parsed_data['message']  # type: ignore
print("message:", message)

# set flash as the default model
# don't mock
completion = litellm_completion('hi', model=MODEL)
print("completion:", completion)

reply_generator = litellm_streaming('hi')
print("reply_generator:", reply_generator)

for reply in reply_generator:
    print("reply:", reply, end='')



test_output_var = python_reflection_testing()
print("test_output_var:", test_output_var)
assert test_output_var == 'test_output_var'



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

parsed_data = agent._parse_xml(xml_data)
assert parsed_data['message'] == 'hello'

xml_data_2 = '<response><thinking>test abc def</thinking><message>Hi! How can I help you?</message><memory><search></search><replace>The user wrote just hi.</replace></memory></response>'
parsed_data_2 = agent._parse_xml(xml_data_2)
assert parsed_data_2['message'] == 'Hi! How can I help you?'
assert parsed_data_2['thinking'] == 'test abc def'
assert parsed_data_2['memory']['search'] == ''
assert parsed_data_2['memory']['replace'] == 'The user wrote just hi.'

agent._update_memory(parsed_data_2['memory']['search'], parsed_data_2['memory']['replace'])
assert agent.memory == 'The user wrote just hi.'


agent_assert = AgentAssert(model=MODEL)
assert type(agent_assert.agent) == Agent

bool_val = agent_assert._parse_xml('<response><message>The implementation does not match specifications</message><bool>False</bool></response>')
assert bool_val == False


return_val = agent_assert('twenty two has has the same meaning as 22')
print("return_val:", return_val)
assert type(return_val) == bool

two_plus_two_is_4 = agent_assert('two plus two is 5')
print("two_plus_two_is_4:", two_plus_two_is_4)
assert two_plus_two_is_4 == False


shell_code_executor = ShellCodeExecutor()
assert type(shell_code_executor) == Tool


# check if this is a subset of the blacklisted commands
assert {'rm', 'cat', 'mv', 'cp'} & set(shell_code_executor.blacklisted_commands) == {'rm', 'cat', 'mv', 'cp'}
assert {'ls', 'date'} & set(shell_code_executor.whitelisted_commands) == {'ls', 'date'}


shell_code_executor_ls = shell_code_executor('ls')
print("shell_code_executor_ls:", shell_code_executor_ls)
assert 'plex.md' in shell_code_executor_ls



