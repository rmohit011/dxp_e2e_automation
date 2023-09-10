import pytest

@pytest.mark.skip("skip it")
def test_environment(name):
    assert name in ["dev", "staging", "prod"], "Invalid environment specified"

def test_exec(name):
    assert name == 'dev', 'name invalid'
