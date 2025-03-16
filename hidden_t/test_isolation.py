import pytest
from src.isolation import *

def test_test_docker_run():
    output = run_container('hello-world')
    assert 'Hello from Docker!' in output

