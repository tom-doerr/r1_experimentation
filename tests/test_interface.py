import pytest
from src.interface import *


from src.reflection import python_reflection_test

def test_reflection():
    reflection_test_var = python_reflection_test()
    assert isinstance(reflection_test_var, str)
    assert "Functions:" in reflection_test_var
    assert "Classes:" in reflection_test_var
