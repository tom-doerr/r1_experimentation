import pytest
from src.agent import *
from src import *
from src.main import *

def test_memory():
    agent = Agent()
    assert agent.memory == ''

def test_agent_model():
    agent = Agent()
    assert agent.model

def test_inference():
    agent = Agent(max_tokens=10)
    assert 'openrouter' in agent.model
    assert len(agent('hi')) > 0

    agent = Agent(model='deepseek')
    assert agent.model == 'deepseek/deepseek-chat'

    agent = Agent(model='flash')
    assert 'openrouter' in agent.model
    assert len(agent('hi')) > 0

def test_attributes():
    agent = Agent()
    assert agent.net_worth == global_settings['initial_net_worth']

