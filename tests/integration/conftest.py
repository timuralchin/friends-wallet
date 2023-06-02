import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from tests.factories.users import UserFactory


@pytest.fixture
def api_user():
    return UserFactory.create()


@pytest.fixture
def auth_client(api_user):
    token = RefreshToken.for_user(api_user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
    return client, token


@pytest.fixture
def authable_client():
    return _auth_client


def _auth_client(user):
    token = RefreshToken.for_user(user)
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token.access_token}')
    return client
