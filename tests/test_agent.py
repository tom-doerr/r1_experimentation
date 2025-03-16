import pytest
from src.agent import *

def test_memory():
    agent = Agent()
    assert agent.memory == ''

def test_agent_model():
    agent = Agent()
    assert agent.model


from src.agent import Agent, AgentAssert

def test_agent_creation():
    agent = Agent()
    assert isinstance(agent, Agent)

def test_agent_assert():
    assert_agent = AgentAssert()
    assert isinstance(assert_agent, AgentAssert)
