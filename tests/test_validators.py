import pytest

from utils.validators import (
    validate_email,
    validate_name,
    validate_password,
    validate_score,
    validate_capacity,
    validate_pass_mark
)


def test_valid_email():
    assert validate_email("alex@example.com") == "alex@example.com"


def test_invalid_email():
    with pytest.raises(ValueError):
        validate_email("invalid-email")


def test_valid_name():
    assert validate_name("Alex") == "Alex"


def test_empty_name():
    with pytest.raises(ValueError):
        validate_name("")


def test_short_password():
    with pytest.raises(ValueError):
        validate_password("123")


def test_valid_score():
    assert validate_score("75") == 75.0


def test_invalid_score():
    with pytest.raises(ValueError):
        validate_score("abc")


def test_score_above_100():
    with pytest.raises(ValueError):
        validate_score("101")


def test_valid_capacity():
    assert validate_capacity("10") == 10


def test_invalid_capacity():
    with pytest.raises(ValueError):
        validate_capacity("0")


def test_valid_pass_mark():
    assert validate_pass_mark("50") == 50.0


def test_invalid_pass_mark():
    with pytest.raises(ValueError):
        validate_pass_mark("150")