import pytest


@pytest.fixture(scope='module')
def test_constructor():
    assert 'foo'.endswith('oo')
