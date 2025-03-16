import pytest
from src.envs import *


def test_env_1():
    env_1 = Env1(target_char="a", char_count_penalty_start=10)
    assert env_1("aaa") == 3
    assert env_1("abajdfaa") == 4
    assert env_1("abjkldfa") == 2
    assert env_1("bjkldf") == 0
    assert env_1("bjkldfjdfdjj") == -2
    assert env_1("bjkldfjdfdj") == -1
    assert env_1("bakldfjdfdj") == 0
    assert env_1("bakldfjdfda") == 0
    assert env_1("isjfsjjdlfdfel") == -4
    assert env_1("isjfsjjdlfdfela") == -5

def test_env_1_defaults():
    env_1 = Env1()
    assert env_1.target_char == "a"
    assert env_1.char_count_penalty_start == 23

def test_env_2():
    env_2 = Env2(max_char_count=5)
    assert env_2("aaa") == 0
    assert env_2("aba") == 1
    assert env_2("abcba") == 2
    assert env_2("aacaa") == 1
    assert env_2("bjklacalkjb") == 5
    assert env_2("abjklacalkjba") == 4



