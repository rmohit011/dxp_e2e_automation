import pytest

def test_environment(name):
    assert name in ["dev", "staging", "prod"], "Invalid environment specified"

def test_exec(name):
    assert name == 'staging', 'name invalid'
