import pytest
from src.envs import *


def test_env_1():
    env_1 = Env1(target_char="a", char_count_penalty_start=10)
    assert env_1("aaa") == 3
    assert env_1("abajdfaa") == 4
    assert env_1("abjkldfa") == 2
    assert env_1("bjkldf") == 0
    assert env_1("bjkldfjdfdj") == -1
    assert env_1("bakldfjdfdj") == 0
    assert env_1("bakldfjdfda") == -1

def test_env_1_defaults():
    env_1 = Env1()
    assert env_1.target_char == "a"
    assert env_1.char_count_penalty_start == 23
import pytest
from src.envs import Env1

def test_env_1():
    env_1 = Env1(target_char="a", char_count_penalty_start=10)
    assert env_1("aaa") == 3
    assert env_1("abajdfaa") == 4
    assert env_1("abjkldfa") == 2
    assert env_1("bjkldf") == 0

def test_env_1_defaults():
    env_1 = Env1()
    assert env_1("aaa") == 3
    assert env_1("bjkldf") == 0

def test_env_1_edge_cases():
    # Test empty string
    env_1 = Env1(target_char="a")
    assert env_1("") == 0
    
    # Test exact penalty threshold
    env_1 = Env1(target_char="a", char_count_penalty_start=3)
    assert env_1("aaa") == 3  # No penalty
    assert env_1("aaaa") == 2  # 4-2=2
    
    # Test different target character
    env_1 = Env1(target_char="z")
    assert env_1("zzzzz") == 5
    assert env_1("abc") == 0
    
    # Test very high penalty start
    env_1 = Env1(target_char="a", char_count_penalty_start=100)
    assert env_1("a" * 50) == 50

def test_env_1_invalid_input():
    env_1 = Env1()
    
    # Test non-string input
    with pytest.raises(TypeError):
        env_1(123)
        
    # Test invalid initialization
    with pytest.raises(ValueError):
        Env1(target_char="ab")  # More than one character
        
    with pytest.raises(ValueError):
        Env1(char_count_penalty_start=-1)  # Negative penalty start
