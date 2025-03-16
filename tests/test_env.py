import pytest
from src.main import Env1


def test_env_1() -> None:
    env_1: Env1 = Env1(target_char="a", char_count_penalty_start=10)
    assert env_1("aaa") == 3  # type: ignore
    assert env_1("abjdfaa") == 4
    assert env_1("abjkldfa") == 2
    assert env_1("bjkldf") == 0
    assert env_1("bjkldfjdfdj") == -1
    assert env_1("bakldfjdfdj") == 0
    assert env_1("bakldfjdfda") == -1
