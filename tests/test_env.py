import pytest
from src import Env1


def test_env():
    env_1 = Env1()
    assert env_1("aaa") == 3
    assert env_1("abjkladfaa") == 4
    assert env_1("abjkldfa") == 2
