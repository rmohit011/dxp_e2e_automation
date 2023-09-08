import pytest

def test_environment(name):
    assert name in ["dev", "staging", "prod"], "Invalid environment specified"
