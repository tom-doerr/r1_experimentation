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
