import pytest
from src import *


def test_env_1():
    env_1 = Env1()
    assert env_1("aaa") == 3
    assert env_1("abjkladfaa") == 4
    assert env_1("abjkldfa") == 2
    assert env_1("bjkldf") == 0
