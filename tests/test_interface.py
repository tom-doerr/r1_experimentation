import pytest
from src.interface import *


def test_reflection():
    reflection_test_var = python_reflection_test()
    assert reflection_test_var == "reflection_test_var"
