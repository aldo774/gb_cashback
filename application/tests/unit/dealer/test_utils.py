import pytest

from application.apps.dealer.utils import is_cpf_valid


@pytest.mark.parametrize(
    'input, expected_output',
    [
        ('454.408.430-00', True),
        ('28908988068', True),
        ('068.018.630-10', True),
        ('727251.070-67', True),
        ('454.40843011', False),
        ('289.089.880-62', False),
        ('068.018.630-15', False),
        ('727.251.070-69', False),
    ],
)
def test_is_cpf_valid(input, expected_output):
    assert expected_output == is_cpf_valid(input)


@pytest.mark.parametrize(
    'input',
    [
        ('454.408.430-XX'),
        ('289.089.880'),
        (28908988068),
    ],
)
def test_is_cpf_valid_should_raise_due_invalid_pattern(input):
    with pytest.raises(ValueError):
        is_cpf_valid(input)
