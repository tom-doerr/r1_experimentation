import pytest
from src.agent import *

def test_memory():
    agent = Agent()
    assert agent.memory == ''

def test_agent_model():
    agent = Agent()
    assert agent.model


