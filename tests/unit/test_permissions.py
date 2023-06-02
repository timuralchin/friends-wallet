import pytest
from mock import MagicMock
from rest_framework_simplejwt.tokens import RefreshToken

from server.core.auth.permissions import IsAuthenticated


@pytest.mark.django_db
def test_user_pass(user):
    request = MagicMock(
        user=user,
        auth=RefreshToken.for_user(user).access_token,
    )
    assert IsAuthenticated().has_permission(request, '')
