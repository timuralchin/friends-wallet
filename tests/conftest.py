import pytest

from tests.factories.users import UserFactory


@pytest.fixture
def user():
    return UserFactory.create()
