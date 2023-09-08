import pytest

# Fixture: Setting up test data
@pytest.fixture
def sample_data():
    return 5, 3

# Test cases for addition
def test_addition(sample_data):
    x, y = sample_data
    result = x+y
    assert result == 7

# Test cases for subtraction
def test_subtraction(sample_data):
    x, y = sample_data
    result = x-y
    assert result == 2

# Test cases for multiplication
def test_multiplication(sample_data):
    x, y = sample_data
    result = x*y
    assert result == 15

# Test cases for division
def test_division(sample_data):
    x, y = sample_data
    result = x/y
    assert result == 5/3


